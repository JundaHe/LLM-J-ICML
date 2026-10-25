"""
Pilot trainer: LoRA fine-tune a local judge on multi-annotator commit-message ratings with a configurable
training target, then evaluate under CSJE / HCA against held-out humans.

Objectives (applied at the What and Why score-token positions, restricted to the 5 level tokens):
  ce_median : cross-entropy to the pooled (rounded) median            -- the standard "pooled-label SFT"
  kl_soft   : KL(p_emp || q) to the empirical 6-rater pmf (+ optional CE-to-median mix, Chen-2025 style)
  crps      : ordinal CRPS  sum_k (CDF_q(k) - CDF_emp(k))^2
  ce_rater  : cross-entropy to ONE uniformly re-sampled rater's label each step (annotator-as-sample)
  loo_soft  : KL to the leave-one-rater-out pmf (a random rater dropped each step)  -- small-panel target
Usage:
  python train_judge.py --objective kl_soft --out results/kl_soft  [--epochs 2] [--eval_only]
"""
import argparse, json, os, sys, time, math, random
import numpy as np, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cm_data, csje_eval as E
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model

p = argparse.ArgumentParser()
p.add_argument("--model", default="Qwen/Qwen2.5-Coder-7B-Instruct")
p.add_argument("--objective", default="ce_median", choices=["ce_median", "kl_soft", "crps", "ce_rater", "loo_soft", "pp_crps", "pp_kl"])
p.add_argument("--ce_mix", type=float, default=0.0, help="weight of CE-to-median added to distributional objectives")
p.add_argument("--epochs", type=float, default=2)
p.add_argument("--lr", type=float, default=1e-4)
p.add_argument("--accum", type=int, default=8)
p.add_argument("--lora_r", type=int, default=16)
p.add_argument("--max_diff_chars", type=int, default=4000)
p.add_argument("--train_frac", type=float, default=0.7)
p.add_argument("--seed", type=int, default=0)
p.add_argument("--max_steps", type=int, default=-1)
p.add_argument("--n_eval", type=int, default=-1)
p.add_argument("--eval_only", action="store_true")
p.add_argument("--train_raters", type=int, default=6, help="number of raters (random subset) whose ratings form the TRAINING target; eval always uses all 6")
p.add_argument("--permute_within_median", action="store_true", help="placebo: permute training rating histograms among items with the same rounded median")
p.add_argument("--out", required=True)
args = p.parse_args()
os.makedirs(args.out, exist_ok=True)
random.seed(args.seed); np.random.seed(args.seed); torch.manual_seed(args.seed)

# ---------------------------------------------------------------- data
frames = [cm_data.load(pool, args.max_diff_chars) for pool in ["developer", "generated"]]
import pandas as pd
d = pd.concat(frames).reset_index(drop=True)
rng = np.random.RandomState(args.seed)
# item-level split, stratified by pool; items with the same hash (dev + gen) stay in the same split
hashes = d["hash"].unique(); rng.shuffle(hashes)
n_tr = int(len(hashes) * args.train_frac)
tr_h = set(hashes[:n_tr])
tr = d[d.hash.isin(tr_h)].reset_index(drop=True); te = d[~d.hash.isin(tr_h)].reset_index(drop=True)
if args.n_eval > 0: te = te.head(args.n_eval)
print(f"train {len(tr)} test {len(te)} (objective={args.objective})", flush=True)
LEVELS = cm_data.LEVELS

# ---------------------------------------------------------------- model
tok = AutoTokenizer.from_pretrained(args.model)
model = AutoModelForCausalLM.from_pretrained(args.model, dtype=torch.bfloat16, device_map="cuda")
level_ids = torch.tensor([tok.encode(str(l), add_special_tokens=False)[0] for l in LEVELS], device="cuda")
SEG1 = '```json\n{\n    "What": '; SEG2 = ',\n    "Why": '; SEG3 = '\n}\n```'

def build(prompt, what_ctx):
    """token ids for chat(prompt) + SEG1 + <what> + SEG2 + <why placeholder>; returns ids, idx_what, idx_why."""
    text = tok.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True)
    ids = tok(text, add_special_tokens=False).input_ids
    ids += tok(SEG1, add_special_tokens=False).input_ids
    i_what = len(ids); ids += [int(level_ids[what_ctx])]
    ids += tok(SEG2, add_special_tokens=False).input_ids
    i_why = len(ids); ids += [int(level_ids[0])]   # placeholder; never used as target beyond position
    return ids, i_what, i_why

def q_from_logits(logits, pos):
    return torch.log_softmax(logits[pos - 1, level_ids].float(), -1)   # log q over levels (predicting token at pos)

def loss_fn(logq, H_row, objective, step_rng, t_row=None):
    """logq: (5,) log-probs; H_row: (6,) int ratings."""
    H_row = np.asarray(H_row); K = len(LEVELS)
    p_emp = torch.tensor(np.bincount(H_row, minlength=K) / len(H_row), device=logq.device, dtype=torch.float32)
    med = int(np.clip(np.round(np.median(H_row)), 0, K - 1))
    ce_med = -logq[med]
    if objective == "ce_median":
        return ce_med
    if objective == "kl_soft":
        core = torch.sum(p_emp * (torch.log(p_emp + 1e-12) - logq))
    elif objective == "crps":
        core = torch.sum((torch.cumsum(logq.exp(), 0) - torch.cumsum(p_emp, 0)) ** 2)
    elif objective == "ce_rater":
        core = -logq[int(step_rng.choice(H_row))]
    elif objective in ("pp_crps", "pp_kl"):
        t = torch.tensor(t_row, device=logq.device, dtype=torch.float32)
        core = torch.sum((torch.cumsum(logq.exp(), 0) - torch.cumsum(t, 0)) ** 2) if objective == "pp_crps" else torch.sum(t * (torch.log(t + 1e-12) - logq))
    elif objective == "loo_soft":
        drop = step_rng.randint(len(H_row)); keep = np.delete(H_row, drop)
        p_loo = torch.tensor(np.bincount(keep, minlength=K) / len(keep), device=logq.device, dtype=torch.float32)
        core = torch.sum(p_loo * (torch.log(p_loo + 1e-12) - logq))
    return core + args.ce_mix * ce_med

# ---------------------------------------------------------------- train
if not args.eval_only:
    model.gradient_checkpointing_enable(); model.enable_input_require_grads()
    lcfg = LoraConfig(r=args.lora_r, lora_alpha=2 * args.lora_r, lora_dropout=0.05, task_type="CAUSAL_LM",
                      target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"])
    model = get_peft_model(model, lcfg); model.print_trainable_parameters()
    opt = torch.optim.AdamW([q for q in model.parameters() if q.requires_grad], lr=args.lr, weight_decay=0.0)
    Hw, Hy = cm_data.H(tr, "what"), cm_data.H(tr, "why")
    rs = np.random.RandomState(args.seed + 7); rsel = np.sort(rs.choice(6, args.train_raters, replace=False))
    Hw, Hy = Hw[:, rsel], Hy[:, rsel]; print("training raters:", rsel.tolist(), flush=True)
    if args.permute_within_median:
        rp = np.random.RandomState(args.seed + 11)
        for Hc in (Hw, Hy):
            med = np.round(np.median(Hc, 1)).astype(int)
            for m in np.unique(med):
                idx = np.where(med == m)[0]; Hc[idx] = Hc[rp.permutation(idx)]
        print("placebo: histograms permuted within median groups", flush=True)
    def pp_targets(Hc, K=5):
        """Dirichlet-multinomial posterior predictive: (counts + a*p0)/(k+a); a fit by leave-one-rater-out log-lik on training items."""
        k = Hc.shape[1]; p0 = np.bincount(Hc.ravel(), minlength=K) / Hc.size
        C = np.stack([np.bincount(r, minlength=K) for r in Hc]).astype(float)
        best = None
        for a in [0.1, 0.25, 0.5, 1, 2, 4, 8, 16, 32]:
            ll = 0.0
            for r in range(k):
                Cm = C - np.eye(K)[Hc[:, r]]; P = (Cm + a * p0) / (k - 1 + a); ll += np.log(P[np.arange(len(Hc)), Hc[:, r]] + 1e-12).sum()
            if best is None or ll > best[0]: best = (ll, a)
        a = best[1]; print(f"posterior-predictive alpha={a} (k={k}) p0={np.round(p0,3).tolist()}", flush=True)
        return (C + a * p0) / (k + a)
    Tw = pp_targets(Hw) if args.objective.startswith("pp_") else None
    Ty = pp_targets(Hy) if args.objective.startswith("pp_") else None
    n_steps = int(math.ceil(len(tr) * args.epochs / args.accum)) if args.max_steps < 0 else args.max_steps
    sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1.0, (s + 1) / 20) * max(0.0, 1 - s / max(1, n_steps)))
    step_rng = np.random.RandomState(args.seed + 1)
    model.train(); t0 = time.time(); order = []; micro = 0; step = 0; run_loss = 0.0
    while step < n_steps:
        if not order: order = list(step_rng.permutation(len(tr)))
        i = order.pop()
        what_ctx = int(np.clip(np.round(np.median(Hw[i])), 0, 4))      # teacher-force What context with the median
        ids, i_what, i_why = build(tr.prompt[i], what_ctx)
        x = torch.tensor([ids], device="cuda")
        logits = model(input_ids=x).logits[0]
        loss = (loss_fn(q_from_logits(logits, i_what), Hw[i], args.objective, step_rng, None if Tw is None else Tw[i])
                + loss_fn(q_from_logits(logits, i_why), Hy[i], args.objective, step_rng, None if Ty is None else Ty[i])) / args.accum
        loss.backward(); run_loss += loss.item(); micro += 1
        if micro % args.accum == 0:
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); sched.step(); opt.zero_grad(); step += 1
            if step % 5 == 0 or step == n_steps:
                print(f"step {step}/{n_steps} loss {run_loss/5:.4f} elapsed {time.time()-t0:.0f}s mem {torch.cuda.max_memory_allocated()/1e9:.1f}GB", flush=True); run_loss = 0.0
    model.save_pretrained(os.path.join(args.out, "lora"))

# ---------------------------------------------------------------- eval
model.eval(); Pw, Py = [], []
with torch.no_grad():
    for i in range(len(te)):
        ids, i_what, i_why = build(te.prompt[i], 0)
        x = torch.tensor([ids[:i_what]], device="cuda")
        qw = q_from_logits(model(input_ids=x).logits[0], i_what).exp().cpu().numpy()
        ids, i_what, i_why = build(te.prompt[i], int(np.argmax(qw)))   # Why conditioned on the model's own What
        x = torch.tensor([ids[:i_why]], device="cuda")
        qy = q_from_logits(model(input_ids=x).logits[0], i_why).exp().cpu().numpy()
        Pw.append(qw); Py.append(qy)
Pw, Py = np.array(Pw), np.array(Py)
res = {"args": vars(args), "n_test": len(te)}
for crit, P in [("what", Pw), ("why", Py)]:
    H = cm_data.H(te, crit)
    J_arg = np.array(LEVELS)[P.argmax(1)]
    J_ev = np.clip(np.round(P @ np.array(LEVELS)), 0, 4)
    res[crit] = {"argmax": E.full_report(H, J=J_arg, P=P, levels=LEVELS, B=500, name=f"{args.objective}-argmax"),
                 "expected": E.full_report(H, J=J_ev, levels=LEVELS, B=300, name=f"{args.objective}-ev")}
    o = res[crit]["argmax"]["overall"]
    print(f"[{crit}] HCA(argmax)={o['HCA']:.3f} {o['HCA_ci']}  HCA(dist)={o['HCA_dist']:.3f}  CRPS={o['CRPS']:.3f}  NLL={o['NLL']:.3f}  "
          f"disagreeAUROC={o['disagree_AUROC']:.3f}  alpha_HL={o['alpha_HL']:.3f} alpha_ref={o['alpha_ref']:.3f}", flush=True)
    for s, v in res[crit]["argmax"]["per_stratum"].items():
        print(f"   {s:8s} n={v['n']:3d} HCA={v['HCA']:.3f} HCA_dist={v['HCA_dist']:.3f} Δmatch={v['Delta_match']:+.3f} CRPS={v['CRPS']:.3f}", flush=True)
np.save(os.path.join(args.out, "P_what.npy"), Pw); np.save(os.path.join(args.out, "P_why.npy"), Py)
te[["hash", "msg_type"]].to_csv(os.path.join(args.out, "test_items.csv"), index=False)
json.dump(res, open(os.path.join(args.out, "results.json"), "w"), indent=1, default=float)
print("done", flush=True)
