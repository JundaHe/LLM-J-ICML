"""
Phase-2 trainer (v3): rater-conditioned arms on large fully-crossed panels — one (panel, evaluator fold, outer split, arm) run.

Builds on idea-stage/pilot/train_judge_v2.py (same LoRA recipe, same score-token readout, same hash-grouped 60/10/30 split,
same leave-one-rater-out exclusion: the evaluator rater is in no training target and in no calibration target).

Arms
  hard     CE(z_i)                                   z_i = mode of the target raters (ties -> closest to median, then lower)
  chen     a*KL(p'_i || q) + (1-a)*CE(z_i)           p' = adversarial worst case in simplex ∩ l2-ball(p_i, eps)   (Chen et al. 2025)
  perm     chen with p_i -> p_G(i)                   G = randomised maximum matching within cells (mode z_i, mean bucket of width tau)
  rc       rater-conditioned: for (item i, target rater r) the prompt carries r's scores on k OTHER training items; loss CE(h_ir)
  rc_perm  rc with the whole rating vector of item i replaced by that of G(i)  (same G as perm) — breaks item <-> who-disagrees link
Evaluation (calib + test items)
  hard/chen/perm : q(y|i)                                                      -> P_calib.npy, P_test.npy
  rc/rc_perm     : panel mixture  (1/|R|) sum_{r in R} q(y|i, hist_r), R = n_eval_raters target raters -> P_calib.npy, P_test.npy
                   per-rater pmfs on test (|R| x n_test x K)                   -> P_test_raters.npy
                   evaluator-conditioned q(y|i, hist_e), hist_e from CALIB items -> P_test_evalcond.npy (test only; no leakage)
Usage: python train_judge_v3.py --panel bw --fold 0 --split 0 --arm rc --out results/bw/s0/f0/rc
"""
import argparse, json, os, sys, time, math
from paths import LLMJ
import numpy as np, pandas as pd, torch
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, LLMJ + "/paper-2/idea-stage/pilot")
from support_audit import z_label, random_max_matching
import data_panels

p = argparse.ArgumentParser()
p.add_argument("--panel", required=True, choices=list(data_panels.LOADERS))
p.add_argument("--model", default=None)
p.add_argument("--fold", type=int, required=True, help="index into the seeded evaluator list (see --n_folds); that rater is excluded from targets and calibration")
p.add_argument("--n_folds", type=int, default=12, help="how many evaluator raters are drawn (seeded) for LOAO")
p.add_argument("--split", type=int, default=0)
p.add_argument("--arm", required=True, choices=["hard", "chen0", "chen", "perm", "perm_mode", "mean2", "proto", "rc", "rc_perm"])
p.add_argument("--alpha", type=float, default=0.8); p.add_argument("--eps", type=float, default=0.25)
p.add_argument("--adv_steps", type=int, default=5); p.add_argument("--adv_lr", type=float, default=0.05)
p.add_argument("--tau", type=float, default=0.1, help="mean-bucket width for the permutation cells (large panels have ~unique sums)")
p.add_argument("--hist_k", type=int, default=4, help="rater-history examples in the rc prompt")
p.add_argument("--rc_raters_per_epoch", type=int, default=20, help="target raters sampled per training item per epoch (rc arms)")
p.add_argument("--n_eval_raters", type=int, default=24, help="target raters in the evaluation mixture (rc arms)")
p.add_argument("--perm_seed", type=int, default=None); p.add_argument("--opt_seed", type=int, default=None)
p.add_argument("--lr", type=float, default=1e-4); p.add_argument("--epochs", type=float, default=None); p.add_argument("--accum", type=int, default=8)
p.add_argument("--lora_r", type=int, default=16); p.add_argument("--max_steps", type=int, default=-1); p.add_argument("--n_eval", type=int, default=-1)
p.add_argument("--eval_raters", default=None, help="comma-separated rater indices to use as evaluator folds (default: seeded permutation of all raters)")
p.add_argument("--train_pos", type=int, default=None, help="fixed-budget design: number of target positions (out of the non-evaluator raters) used per TRAINING item, drawn per item with --budget_seed; calib/test targets unchanged")
p.add_argument("--train_frac", type=float, default=None, help="fixed-budget design: fraction of the training GROUPS kept (seeded); combined with --train_pos the rating budget is n_train × train_pos")
p.add_argument("--budget_seed", type=int, default=None)
p.add_argument("--dry_run", action="store_true"); p.add_argument("--out", required=True)
args = p.parse_args(); os.makedirs(args.out, exist_ok=True)
perm_seed = args.perm_seed if args.perm_seed is not None else 1000 + args.split
opt_seed = args.opt_seed if args.opt_seed is not None else 2000 + args.split
torch.manual_seed(opt_seed); np.random.seed(opt_seed)
RC = args.arm in ("rc", "rc_perm")
if args.epochs is None: args.epochs = 2 if RC else 10            # hist arms have only n_train items per epoch; rc arms have n_train * rc_raters_per_epoch pairs

# ------------------------------------------------------------------ data
PAN = data_panels.load(args.panel); H_all = PAN["H"]; K = PAN["K"]; n_items, M_RATERS = H_all.shape; texts = PAN["texts"]
MODEL = args.model or PAN["model"]
# grouped outer split (items are their own groups on these panels)
G = PAN.get("groups", np.arange(n_items)); ug = np.unique(G); rng = np.random.RandomState(args.split); rng.shuffle(ug)       # grouped split (e.g. SummEval: by source document)
g_tr, g_ca = set(ug[: int(.6 * len(ug))]), set(ug[int(.6 * len(ug)): int(.7 * len(ug))])
part = np.array(["train" if G[i] in g_tr else "calib" if G[i] in g_ca else "test" for i in range(n_items)])
tr_idx, ca_idx, te_idx = (np.where(part == k)[0] for k in ("train", "calib", "test"))
# seeded evaluator list (LOAO folds) — same for every arm and split
EVALS = [int(x) for x in args.eval_raters.split(",")] if args.eval_raters else np.random.RandomState(777).permutation(M_RATERS)[: args.n_folds].tolist(); E = EVALS[args.fold]
T = [r for r in range(M_RATERS) if r != E]; Ht = H_all[:, T]                                  # targets exclude the evaluator
z = np.array([z_label(r) for r in Ht]); P_emp = np.stack([np.bincount(r, minlength=K) / len(T) for r in Ht])
mu = Ht.mean(1)
# evaluation-mixture raters (subset of targets), fixed per (split, fold) across arms
R_EVAL = np.random.RandomState(500 + 10 * args.split + args.fold).permutation(T)[: args.n_eval_raters].tolist()
# ------------------------------------------------------------------ fixed-budget design (SHRINKAGE_PROTOCOL.md, learner-side fixed budget — LoRA): fewer training groups and/or fewer target positions per training item
budget_cert = {}
if args.train_frac is not None or args.train_pos is not None:
    bseed = args.budget_seed if args.budget_seed is not None else 3000 + args.split * 100 + args.fold; brng = np.random.RandomState(bseed); n_tr_full = len(tr_idx)
    if args.train_frac is not None and args.train_frac < 1:
        g_keep = set(brng.permutation(sorted(g_tr))[: max(1, int(round(args.train_frac * len(g_tr))))]); tr_idx = np.array([i for i in tr_idx if G[i] in g_keep])
    if args.train_pos is not None and args.train_pos < len(T):
        for i in tr_idx:                                                                  # per-item random subset of the non-evaluator positions; targets of calib/test items untouched
            cols = brng.choice(len(T), size=args.train_pos, replace=False); sub = Ht[i, cols]
            z[i] = z_label(sub); P_emp[i] = np.bincount(sub, minlength=K) / len(sub); mu[i] = sub.mean()
    budget_cert = dict(train_frac=args.train_frac, train_pos=args.train_pos, budget_seed=bseed, n_train_full=int(n_tr_full), n_train_used=int(len(tr_idx)), rating_budget=int(len(tr_idx) * (args.train_pos or len(T))))
    print(f"[budget] train items {n_tr_full} -> {len(tr_idx)}, positions per item {args.train_pos or len(T)}, rating budget {budget_cert['rating_budget']}", flush=True)

# ------------------------------------------------------------------ permutation G on TRAIN items: cells (z_i, floor(mean/tau)); randomised maximum matching on histogram classes within cell
cert = dict(arm=args.arm, panel=args.panel, fold=args.fold, evaluator=int(E), evaluator_id=str(PAN["rater_ids"][E]), split=args.split, perm_seed=perm_seed, opt_seed=opt_seed,
            alpha=args.alpha, eps=args.eps, tau=args.tau, hist_k=args.hist_k, n_items=int(n_items), n_raters=int(M_RATERS),
            parts={k: int((part == k).sum()) for k in ("train", "calib", "test")}, model=MODEL, **budget_cert)
target_P = P_emp.copy(); Hvec = Ht.copy(); mapping = {}
if args.arm in ("perm", "perm_mode", "rc_perm"):
    from collections import defaultdict
    prng = np.random.RandomState(perm_seed); cells = defaultdict(list)
    for i in tr_idx: cells[(int(z[i]), int(math.floor(mu[i] / args.tau)) if args.arm != "perm_mode" else 0)].append(int(i))
    for key, items in cells.items():
        hk = [tuple(np.bincount(Ht[i], minlength=K)) for i in items]          # HISTOGRAM classes (dose audit 2026-10-11): vector-level classes paired items with identical histograms (TV = 0, ~21 % of perm pairs on SummEval)
        for a, b in random_max_matching(items, hk, prng).items():
            assert z[a] == z[b] and (args.arm == "perm_mode" or abs(mu[a] - mu[b]) <= args.tau + 1e-9) and hk[items.index(a)] != hk[items.index(b)]; mapping[a] = b
    assert sorted(mapping) == sorted(mapping.values())
    tv = []; dmean = []
    for a, b in mapping.items():
        target_P[a] = P_emp[b]; Hvec[a] = Ht[b]; tv.append(0.5 * np.abs(P_emp[a] - P_emp[b]).sum()); dmean.append(abs(mu[a] - mu[b]))
    assert all(t > 1e-12 for t in tv), "a matched pair left the histogram unchanged"
    import hashlib; cert["mapping_hash"] = hashlib.sha1(str(sorted((int(a), int(b)) for a, b in mapping.items())).encode()).hexdigest()
    cert["target_hash"] = hashlib.sha1(np.round(np.stack([P_emp[mapping.get(int(i), int(i))] for i in tr_idx]), 6).tobytes()).hexdigest()
    cert.update(n_train=int(len(tr_idx)), n_changed=len(mapping), changed_fraction=len(mapping) / len(tr_idx), n_tv_zero=int(sum(t <= 1e-12 for t in tv)), matching="histogram_class", dose_tv_mean=float(np.mean(tv)) if tv else 0.0,
                dose_tv_max=float(np.max(tv)) if tv else 0.0, mean_shift_mean=float(np.mean(dmean)) if dmean else 0.0, mean_shift_max=float(np.max(dmean)) if dmean else 0.0)
    print(f"[perm certificate] changed {len(mapping)}/{len(tr_idx)} = {cert['changed_fraction']:.3f}; dose TV mean {cert['dose_tv_mean']:.3f}; |Δmean| max {cert['mean_shift_max']:.3f}", flush=True)

if args.arm in ("mean2", "proto"):
    LVv = np.arange(K); proto = {c: P_emp[tr_idx][z[tr_idx] == c].mean(0) if (z[tr_idx] == c).any() else np.full(K, 1 / K) for c in range(K)}
    def tilt(pr, m):
        lo, hi = -20.0, 20.0
        for _ in range(60):
            lam = (lo + hi) / 2; q = pr * np.exp(lam * LVv); q /= q.sum()
            if q @ LVv < m: lo = lam
            else: hi = lam
        return q
    target_P = np.stack([tilt(proto[int(z[i])] + 1e-6, mu[i]) if args.arm == "mean2" else proto[int(z[i])] for i in range(n_items)])
    cert.update(target="mode-prototype tilted to item mean" if args.arm == "mean2" else "mode-conditional prototype", tv_to_hist_mean=float(np.mean(0.5 * np.abs(target_P - P_emp).sum(1))))
    print(f"[{args.arm}] mean TV(target, histogram) {cert['tv_to_hist_mean']:.3f}", flush=True)

# ------------------------------------------------------------------ rater histories (rc arms)
def history(r, exclude_item, pool_idx, seed):
    """k (text, level) examples of rater r on items from pool_idx (never the item being scored). Levels come from the (possibly permuted) Hvec for TRAIN pools."""
    cand = [i for i in pool_idx if i != exclude_item]; hr = np.random.RandomState(seed); pick = hr.choice(cand, size=min(args.hist_k, len(cand)), replace=False)
    return [(texts[i], int(Hvec[i, T.index(r)] if part[i] == "train" else H_all[i, r])) for i in pick]
def rc_prompt(i, r, pool_idx, seed): return PAN["prompt_hist"](texts[i], history(r, i, pool_idx, seed))
if args.dry_run:
    cert.update(evals=EVALS, targets=T, R_eval=R_EVAL, n_steps_planned=int(math.ceil(len(tr_idx) * (args.rc_raters_per_epoch if RC else 1) * args.epochs / args.accum)))
    if RC: cert["sample_rc_prompt_chars"] = len(rc_prompt(int(tr_idx[0]), T[0], tr_idx, 0))
    json.dump(cert, open(os.path.join(args.out, "meta.json"), "w"), indent=1); print("DRY RUN OK", json.dumps({k: v for k, v in cert.items() if k not in ('targets', 'R_eval', 'evals')})); sys.exit(0)

# ------------------------------------------------------------------ model
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model
tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map="cuda"); model.eval()
LEVEL_STRS = PAN["LEVEL_STRS"]; PREFIX = PAN["PREFIX"]
assert all(len(tok.encode(ls, add_special_tokens=False)) == 1 for ls in LEVEL_STRS), "score levels must be single tokens"
level_ids = torch.tensor([tok.encode(ls, add_special_tokens=False)[0] for ls in LEVEL_STRS], device="cuda")
def build(prompt):
    text = tok.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True) + PREFIX
    return tok(text, add_special_tokens=False, return_tensors="pt").input_ids
def logq(ids): return torch.log_softmax(model(input_ids=ids.to("cuda")).logits[0, -1][level_ids].float(), -1)
def simplex_proj(v):
    u, _ = torch.sort(v, descending=True); css = torch.cumsum(u, 0) - 1; ind = torch.arange(1, len(v) + 1, device=v.device, dtype=v.dtype)
    cond = u - css / ind > 0; rho = ind[cond][-1]; theta = css[cond][-1] / rho; return torch.clamp(v - theta, min=0)
def adversarial_p(pt, lq):
    pp = pt.clone()
    for _ in range(args.adv_steps):
        g = torch.log(pp + 1e-12) - lq.detach() + 1.0; pp = pp + args.adv_lr * g
        v = pp - pt; nv = torch.norm(v)
        if nv > args.eps: v = v * (args.eps / nv)
        pp = simplex_proj(pt + v)
    return pp.detach()
def loss_hist(lq, i):
    ce = -lq[int(z[i])]
    if args.arm == "hard": return ce
    pt = torch.tensor(target_P[i], device="cuda", dtype=torch.float32)
    if args.arm in ("chen", "perm", "perm_mode", "mean2", "proto"): pt = adversarial_p(pt, lq)
    return args.alpha * torch.sum(pt * (torch.log(pt + 1e-12) - lq)) + (1 - args.alpha) * ce

# ------------------------------------------------------------------ train
model.gradient_checkpointing_enable(); model.enable_input_require_grads()
model = get_peft_model(model, LoraConfig(r=args.lora_r, lora_alpha=2 * args.lora_r, lora_dropout=0.05, task_type="CAUSAL_LM",
                                          target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]))
opt = torch.optim.AdamW([q for q in model.parameters() if q.requires_grad], lr=args.lr, weight_decay=0.0)
per_epoch = len(tr_idx) * (args.rc_raters_per_epoch if RC else 1)
n_steps = int(math.ceil(per_epoch * args.epochs / args.accum)) if args.max_steps < 0 else args.max_steps
sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1.0, (s + 1) / 20) * max(0.0, 1 - s / max(1, n_steps)))
orng = np.random.RandomState(opt_seed); order = []; model.train(); t0 = time.time(); step = micro = 0; run = 0.0; losses = []; maxlen = 0
while step < n_steps:
    if not order:
        if RC: order = [(int(i), int(r)) for i in orng.permutation(tr_idx) for r in orng.choice(T, size=args.rc_raters_per_epoch, replace=False)]; orng.shuffle(order)
        else: order = [(int(i), -1) for i in orng.permutation(tr_idx)]
    i, r = order.pop()
    if RC:
        ids = build(rc_prompt(i, r, tr_idx, seed=opt_seed * 7919 + micro)); lq = logq(ids); loss = -lq[int(Hvec[i, T.index(r)])]
    else:
        ids = build(PAN["prompt"](texts[i])); loss = loss_hist(logq(ids), i)
    maxlen = max(maxlen, ids.shape[1]); loss = loss / args.accum; loss.backward(); run += loss.item(); micro += 1
    if micro % args.accum == 0:
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); sched.step(); opt.zero_grad(); step += 1; losses.append(run); run = 0.0
        if step % 10 == 0 or step == n_steps: print(f"step {step}/{n_steps} loss {np.mean(losses[-10:]):.4f} {time.time()-t0:.0f}s maxlen {maxlen} mem {torch.cuda.max_memory_allocated()/1e9:.1f}GB", flush=True)
model.save_pretrained(os.path.join(args.out, "lora"))

# ------------------------------------------------------------------ eval
model.eval()
with torch.no_grad():
    for name, idx in (("calib", ca_idx), ("test", te_idx)):
        if args.n_eval > 0: idx = idx[: args.n_eval]
        if not RC:
            P = np.array([logq(build(PAN["prompt"](texts[i]))).exp().cpu().numpy() for i in idx])
        else:
            PR = np.zeros((len(R_EVAL), len(idx), K))
            for a, r in enumerate(R_EVAL):
                for b, i in enumerate(idx): PR[a, b] = logq(build(rc_prompt(int(i), r, tr_idx, seed=90000 + 1000 * a + b))).exp().cpu().numpy()
            P = PR.mean(0)
            if name == "test":
                np.save(os.path.join(args.out, "P_test_raters.npy"), PR)
                PE = np.array([logq(build(rc_prompt(int(i), E, ca_idx, seed=70000 + b))).exp().cpu().numpy() for b, i in enumerate(idx)])   # evaluator history from CALIB items only
                np.save(os.path.join(args.out, "P_test_evalcond.npy"), PE)
        np.save(os.path.join(args.out, f"P_{name}.npy"), P)
        pd.DataFrame({"item_id": PAN["item_ids"][idx], "row": idx}).to_csv(os.path.join(args.out, f"items_{name}.csv"), index=False)
cert.update(n_steps=int(n_steps), final_loss=float(np.mean(losses[-10:])) if losses else None, train_time_s=time.time() - t0, max_prompt_tokens=int(maxlen),
            targets=T, R_eval=R_EVAL, evals=EVALS, lora=True, note="LoRA; rc arms condition on k rater-history examples from the train pool (evaluator: calib pool)")
json.dump(cert, open(os.path.join(args.out, "meta.json"), "w"), indent=1)
print("done", flush=True)
