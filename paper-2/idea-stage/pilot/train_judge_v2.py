"""
Final-protocol trainer (v2) for the identifiability audit — one (panel, criterion, evaluator fold, outer split, arm) run.

Protocol (refine-logs/FINAL_PROPOSAL.md, after external review round 2):
  * single-criterion prompt (Zeng WHAT_/WHY_ zero-shot non-CoT), score read from the next-token distribution over "0".."4"
  * hash-grouped outer split (seed = --split): train 60 % / calibration 10 % / test 30 %
  * evaluator fold --fold r: rater r is EXCLUDED from every target and from calibration; targets use the m_t = 5 remaining raters
  * point label z_i = mode of target ratings (ties -> level closest to target median, then lower)
  * arms: hard  = CE(z_i, q)
          chen0 = a*KL(p_i||q) + (1-a)*CE(z_i, q)                                  (matched no-adversary control)
          chen  = a*KL(p'_i||q) + (1-a)*CE(z_i, q), p' = worst case in simplex ∩ l2-ball(p_i, eps) found by 5 PGA steps of 0.05 (Chen et al.: a=0.8, eps=0.25)
          perm  = chen with p_i replaced by p_G(i): G = randomised maximum-cardinality exact matching within cells (pool, z_i, sum_y); identity elsewhere
  * LoRA (deviation from Chen's full fine-tuning — documented); lr 1e-4; 2 epochs; accum 8
  * outputs: P_calib.npy, P_test.npy (score-token pmfs), items_*.csv, meta.json (incl. permutation certificate), lora/
Usage: python train_judge_v2.py --criterion why --fold 0 --split 0 --arm perm --out results_v2/why/s0/f0/perm
"""
import argparse, json, os, sys, time, math, importlib.util
import numpy as np, pandas as pd, torch
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from support_audit import z_label, random_max_matching
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model

K = 5; LEVELS = list(range(K)); ROOT = "/mnt/hdd2/jundahe/LLM-J/code/commit_message"
p = argparse.ArgumentParser()
p.add_argument("--model", default="Qwen/Qwen2.5-Coder-7B-Instruct")
p.add_argument("--panel", default="commit", choices=["commit", "readability"])
p.add_argument("--criterion", default="why", choices=["what", "why", "readability"])
p.add_argument("--dry_run", action="store_true", help="build targets / permutation / split on CPU and exit before loading the model")
p.add_argument("--fold", type=int, required=True, help="evaluator rater index (commit 0..5, readability 0..8), excluded from targets + calibration")
p.add_argument("--split", type=int, default=0, help="outer split seed (hash-grouped 60/10/30)")
p.add_argument("--arm", required=True, choices=["hard", "chen0", "chen", "perm", "perm_mode", "perm_mode0", "mean2", "proto", "sordm"],
               help="perm_mode (added 2026-10-11, Codex review): cells = (pool, z_i) only, so the permutation also breaks the item<->mean link; perm = (pool, z_i, sum_y)")
p.add_argument("--alpha", type=float, default=0.8); p.add_argument("--eps", type=float, default=0.25)
p.add_argument("--adv_steps", type=int, default=5); p.add_argument("--adv_lr", type=float, default=0.05)
p.add_argument("--perm_seed", type=int, default=None, help="independent permutation seed (default: 1000 + split)")
p.add_argument("--sord_sigma", type=float, default=0.75, help="sordm arm: Gaussian width around the item mean (heads-tuned 0.75-1.0)")
p.add_argument("--opt_seed", type=int, default=None, help="optimiser / data-order seed (default: 2000 + split)")
p.add_argument("--lr", type=float, default=1e-4); p.add_argument("--epochs", type=float, default=2); p.add_argument("--accum", type=int, default=8)
p.add_argument("--lora_r", type=int, default=16); p.add_argument("--max_diff_chars", type=int, default=4000)
p.add_argument("--max_steps", type=int, default=-1); p.add_argument("--n_eval", type=int, default=-1)
p.add_argument("--out", required=True)
args = p.parse_args(); os.makedirs(args.out, exist_ok=True)
perm_seed = args.perm_seed if args.perm_seed is not None else 1000 + args.split
opt_seed = args.opt_seed if args.opt_seed is not None else 2000 + args.split
torch.manual_seed(opt_seed); np.random.seed(opt_seed)

# ------------------------------------------------------------------ data (panel-specific)
if args.panel == "commit":
    spec = importlib.util.spec_from_file_location("pp", f"{ROOT}/replication_package/cmeval/llm_metrics/prompts/{args.criterion}_prompts.py")
    pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
    TPL = getattr(pm, f"{args.criterion.upper()}_EVALUTE_PROMPT_TEMPLATE_ZERO_SHOT_NONCOT")
    bench = pd.read_csv(f"{ROOT}/data/CM-benchmark.csv"); src = pd.read_csv(f"{ROOT}/datasets/commits.csv")
    d = bench.merge(src[["hash", "git_diff_u3"]], on="hash", how="left").reset_index(drop=True)
    assert d.git_diff_u3.notna().all()
    d["prompt"] = [TPL.replace("{diff}", str(df_)[: args.max_diff_chars]).replace("{message}", str(msg)).replace("{{", "{").replace("}}", "}")
                   for df_, msg in zip(d.git_diff_u3, d.commit_message)]
    H_all = d[[f"{args.criterion}_{i}" for i in range(1, 7)]].to_numpy(int); M_RATERS = 6
    pools_all = d.msg_type.to_numpy(); groups_all = d.hash.to_numpy()
    SPLIT = (.6, .7); PREFIX = '```json\n{\n    "Score": '; LEVEL_STRS = [str(l) for l in LEVELS]
else:
    RD = "/mnt/hdd2/jundahe/LLM-J/code/code_readability"
    Msc = pd.read_csv(f"{RD}/data/scalabrino/scores.csv", index_col=0); ds = pd.read_csv(f"{RD}/data/coreeval_snippets/Scalabrino_java_Code.csv")
    cols = list(Msc.columns); H_all = np.array([Msc.iloc[:, cols.index(f"Snippet{int(sid)}")].to_numpy(int) for sid in ds.snippet_id]) - 1   # 1-5 -> 0-4, direct key
    M_RATERS = 9; pools_all = np.array(["rd"] * len(ds)); groups_all = ds.snippet_id.to_numpy()
    # CoReEval senior zero-shot Java template, verbatim except the scale (0-20 -> 1-5, to match the 5-level human Likert target) and the JSON prefix
    TPL = ("You are an experienced senior software engineer specialized in code quality assessment and readability evaluation. "
           "Evaluate provided Java code on a scale from 1 (unreadable) to 5 (highly readable) based on naming clarity, structure, indentation, comments, complexity, and overall clarity.\n"
           "Respond ONLY with JSON:\n{\n\"score\": \"1-5\"\n}\nPlease ensure the complete JSON format is placed between the three quotes ``` ``` for easy extraction.\n\n"
           "Evaluate the readability of the following Java source code:\n\nSOURCE_CODE\n\nEnd of the provided source code. \nPlease present your evaluation in the required JSON format.")
    d = pd.DataFrame({"snippet_id": ds.snippet_id, "prompt": [TPL.replace("SOURCE_CODE", str(c)) for c in ds.code_snippet]})
    SPLIT = (.6, .75); PREFIX = '```json\n{\n"score": "'; LEVEL_STRS = [str(l + 1) for l in LEVELS]       # tokens "1".."5" <-> levels 0..4
# grouped outer split
hashes = np.unique(groups_all); rng = np.random.RandomState(args.split); rng.shuffle(hashes)
n = len(hashes); tr_h, ca_h = set(hashes[: int(SPLIT[0] * n)]), set(hashes[int(SPLIT[0] * n): int(SPLIT[1] * n)])
part = np.where(pd.Series(groups_all).isin(tr_h), "train", np.where(pd.Series(groups_all).isin(ca_h), "calib", "test"))
# evaluator exclusion
T = [r for r in range(M_RATERS) if r != args.fold]; Ht = H_all[:, T]
z = np.array([z_label(r) for r in Ht]); P_emp = np.stack([np.bincount(r, minlength=K) / len(T) for r in Ht])
assert args.fold not in T
# permutation (perm arm): randomised maximum matching within cells on TRAIN items only
cert = {"arm": args.arm, "fold": args.fold, "split": args.split, "perm_seed": perm_seed, "opt_seed": opt_seed, "alpha": args.alpha, "eps": args.eps}
target_P = P_emp.copy()
if args.arm in ("perm", "perm_mode", "perm_mode0"):   # perm_mode0 (Codex round 10): perm_mode target under the chen0 (no-adversary) objective
    from collections import defaultdict, Counter
    prng = np.random.RandomState(perm_seed); cells = defaultdict(list); tr_idx = np.where(part == "train")[0]
    for i in tr_idx: cells[(pools_all[i], int(z[i]), int(Ht[i].sum()) if args.arm == "perm" else 0)].append(int(i))
    changed = 0; doses = []; mapping = {}
    for key, items in cells.items():
        hist = [tuple(np.bincount(Ht[i], minlength=K)) for i in items]
        pm_ = random_max_matching(items, hist, prng)
        for a, b in pm_.items():
            assert np.bincount(Ht[a], minlength=K).tolist() != np.bincount(Ht[b], minlength=K).tolist()
            assert z[a] == z[b] and pools_all[a] == pools_all[b] and (args.arm in ("perm_mode", "perm_mode0") or Ht[a].sum() == Ht[b].sum())
            mapping[a] = b
    assert sorted(mapping.keys()) == sorted(mapping.values())           # bijection on the changed set
    dmeans = []
    for a, b in mapping.items():
        target_P[a] = P_emp[b]; changed += 1; doses.append(0.5 * np.abs(P_emp[a] - P_emp[b]).sum()); dmeans.append(abs(Ht[a].mean() - Ht[b].mean()))
    import hashlib; cert["mapping_hash"] = hashlib.sha1(str(sorted((int(a), int(b)) for a, b in mapping.items())).encode()).hexdigest()   # exact donor-map identity (Codex round 10)
    cert["target_hash"] = hashlib.sha1(np.round(np.stack([P_emp[mapping.get(i, i)] for i in tr_idx]), 6).tobytes()).hexdigest()   # item -> assigned target histogram (Codex round 11: the scientifically relevant certificate)
    cert.update(n_train=int(len(tr_idx)), n_changed=int(changed), changed_fraction=changed / len(tr_idx), dose_tv_mean=float(np.mean(doses)) if doses else 0.0,
                dose_tv_max=float(np.max(doses)) if doses else 0.0, mean_shift_mean=float(np.mean(dmeans)) if dmeans else 0.0, mean_shift_max=float(np.max(dmeans)) if dmeans else 0.0)
    print(f"[perm certificate] changed {changed}/{len(tr_idx)} = {changed/len(tr_idx):.3f}; dose TV mean {cert['dose_tv_mean']:.3f}", flush=True)

if args.arm in ("mean2", "proto"):
    # mean2 (added 2026-10-11): mode-conditional prototype (mean train histogram of items with the same z) exponentially tilted to the item's own mean  -> carries (mode, mean)
    # proto: the prototype itself -> class-conditional smoothing, carries the mode only (the LoRA-level smoothing control)
    tr_idx = np.where(part == "train")[0]; LVv = np.arange(K)
    proto = {c: P_emp[tr_idx][z[tr_idx] == c].mean(0) if (z[tr_idx] == c).any() else np.full(K, 1 / K) for c in range(K)}
if args.arm == "sordm":   # SORD-style parametric target centred on the item mean (Diaz & Marathe 2019 with the empirical mean as centre)
    LVv = np.arange(K); target_P = np.stack([np.exp(-(LVv - Ht[i].mean()) ** 2 / (2 * args.sord_sigma ** 2)) for i in range(len(z))]); target_P /= target_P.sum(1, keepdims=True)
    cert.update(target=f"gaussian at item mean, sigma={args.sord_sigma}", tv_to_hist_mean=float(np.mean(0.5 * np.abs(target_P - P_emp).sum(1))))
    print(f"[sordm] mean TV(target, histogram) {cert['tv_to_hist_mean']:.3f}", flush=True)
if args.arm == "proto":
    target_P = np.stack([proto[int(z[i])] for i in range(len(z))]); cert.update(target="mode-conditional prototype", tv_to_hist_mean=float(np.mean(0.5 * np.abs(target_P - P_emp).sum(1))))
    print(f"[proto] mean TV(target, histogram) {cert['tv_to_hist_mean']:.3f}", flush=True)
if args.arm == "mean2":
    def tilt(pr, m):
        lo, hi = -20.0, 20.0
        for _ in range(60):
            lam = (lo + hi) / 2; q = pr * np.exp(lam * LVv); q /= q.sum()
            if q @ LVv < m: lo = lam
            else: hi = lam
        return q
    sys.path.insert(0, "/mnt/hdd2/jundahe/LLM-J/paper-2/phase2"); from targets import ordinal_mode_mean, assert_valid_ordinal
    target_P = np.stack([ordinal_mode_mean(proto[int(z[i])], int(z[i]), Ht[i].mean(), feasible=P_emp[i]) for i in range(len(z))])      # constrained: mean AND mode preserved, hard-fail certified
    cert.update(target="mode-prototype KL-projected to item mean with mode constraint", mean_abs_err=float(np.abs(target_P @ LVv - Ht.mean(1)).max()), tv_to_hist_mean=float(np.mean(0.5 * np.abs(target_P - P_emp).sum(1))), **assert_valid_ordinal(target_P, z, Ht.mean(1), "mean2"))
    print(f"[mean2] max |target mean - item mean| {cert['mean_abs_err']:.2e}; mean TV(target, histogram) {cert['tv_to_hist_mean']:.3f}", flush=True)
cert.update(panel=args.panel, criterion=args.criterion, n_items=int(len(d)), parts={k: int((part == k).sum()) for k in ['train','calib','test']})
if args.dry_run:
    json.dump(cert, open(os.path.join(args.out, 'meta.json'), 'w'), indent=1); print('DRY RUN OK', cert); sys.exit(0)
# ------------------------------------------------------------------ model
tok = AutoTokenizer.from_pretrained(args.model)
model = AutoModelForCausalLM.from_pretrained(args.model, dtype=torch.bfloat16, device_map="cuda"); model.eval()
level_ids = torch.tensor([tok.encode(ls, add_special_tokens=False)[0] for ls in LEVEL_STRS], device="cuda")
assert all(len(tok.encode(ls, add_special_tokens=False)) == 1 for ls in LEVEL_STRS), "score levels must be single tokens"
def build(prompt):
    text = tok.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True) + PREFIX
    return tok(text, add_special_tokens=False, return_tensors="pt").input_ids
def logq(ids):
    logits = model(input_ids=ids.to("cuda")).logits[0, -1]
    return torch.log_softmax(logits[level_ids].float(), -1)
def simplex_proj(v):
    u, _ = torch.sort(v, descending=True); css = torch.cumsum(u, 0) - 1; ind = torch.arange(1, len(v) + 1, device=v.device, dtype=v.dtype)
    cond = u - css / ind > 0; rho = ind[cond][-1]; theta = css[cond][-1] / rho; return torch.clamp(v - theta, min=0)
def adversarial_p(p, lq):
    """worst-case p' in simplex ∩ l2-ball(p, eps) maximising KL(p'||q): projected gradient ascent (Chen et al.: 5 steps, step 0.05)"""
    pp = p.clone()
    for _ in range(args.adv_steps):
        g = torch.log(pp + 1e-12) - lq.detach() + 1.0                  # d/dp' KL(p'||q)
        pp = pp + args.adv_lr * g
        v = pp - p; nv = torch.norm(v)
        if nv > args.eps: v = v * (args.eps / nv)
        pp = simplex_proj(p + v)
    return pp.detach()
def loss_fn(lq, i):
    zt = torch.tensor(int(z[i]), device="cuda"); ce = -lq[zt]
    if args.arm == "hard": return ce
    pt = torch.tensor(target_P[i], device="cuda", dtype=torch.float32)
    if args.arm in ("chen", "perm", "perm_mode", "mean2", "proto", "sordm"): pt = adversarial_p(pt, lq)     # mean2 / proto = chen's objective with the two-number / mode-only target
    kl = torch.sum(pt * (torch.log(pt + 1e-12) - lq))
    return args.alpha * kl + (1 - args.alpha) * ce

# ------------------------------------------------------------------ train
tr_idx = np.where(part == "train")[0]
model.gradient_checkpointing_enable(); model.enable_input_require_grads()
model = get_peft_model(model, LoraConfig(r=args.lora_r, lora_alpha=2 * args.lora_r, lora_dropout=0.05, task_type="CAUSAL_LM",
                                          target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]))
opt = torch.optim.AdamW([q for q in model.parameters() if q.requires_grad], lr=args.lr, weight_decay=0.0)
n_steps = int(math.ceil(len(tr_idx) * args.epochs / args.accum)) if args.max_steps < 0 else args.max_steps
sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1.0, (s + 1) / 20) * max(0.0, 1 - s / max(1, n_steps)))
orng = np.random.RandomState(opt_seed); order = []; model.train(); t0 = time.time(); step = micro = 0; run = 0.0; losses = []
while step < n_steps:
    if not order: order = list(orng.permutation(tr_idx))
    i = int(order.pop()); ids = build(d.prompt[i])
    loss = loss_fn(logq(ids), i) / args.accum; loss.backward(); run += loss.item(); micro += 1
    if micro % args.accum == 0:
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); sched.step(); opt.zero_grad(); step += 1; losses.append(run); run = 0.0
        if step % 10 == 0 or step == n_steps: print(f"step {step}/{n_steps} loss {np.mean(losses[-10:]):.4f} {time.time()-t0:.0f}s mem {torch.cuda.max_memory_allocated()/1e9:.1f}GB", flush=True)
model.save_pretrained(os.path.join(args.out, "lora"))

# ------------------------------------------------------------------ eval: calib + test pmfs
model.eval()
for name in ["calib", "test"]:
    idx = np.where(part == name)[0]
    if args.n_eval > 0: idx = idx[: args.n_eval]
    P = []
    with torch.no_grad():
        for i in idx: P.append(logq(build(d.prompt[i])).exp().cpu().numpy())
    np.save(os.path.join(args.out, f"P_{name}.npy"), np.array(P))
    (d.iloc[idx][["hash", "msg_type"]] if args.panel == "commit" else d.iloc[idx][["snippet_id"]]).assign(row=idx).to_csv(os.path.join(args.out, f"items_{name}.csv"), index=False)
cert.update(n_steps=int(n_steps), final_loss=float(np.mean(losses[-10:])) if losses else None, train_time_s=time.time() - t0,
            target_raters=T, evaluator=args.fold, model=args.model, lora=True, note="LoRA instead of Chen's full fine-tuning; no released code to parity-test")
json.dump(cert, open(os.path.join(args.out, "meta.json"), "w"), indent=1)
print("done", flush=True)
