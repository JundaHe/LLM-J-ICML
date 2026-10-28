"""Stage 2b (PROTOCOL_STAGE2B.md) on MultiPref: per fold, (1) D-LoRA — a rater-agnostic distributional LoRA reward model trained on the training raters' ratings of the training items,
whose 5 score-token log-probabilities for every item are saved as a frozen text head for factorised_rm.py --text_logits; (2) RC-LoRA (--mode rc) — in-context personalisation: trained on
(training rater, item) prompts that contain 10 of the rater's other ratings, evaluated on new raters conditioned on k of their training-item ratings (the stage-2a draws, first draw).
Folds, validation groups and k-shot draws reproduce factorised_rm.py exactly (checked against its saved fold sizes).
Usage: python lora_rm.py --fold 0 [--mode d|rc]"""
import os, sys, json, math, time, argparse
import numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2)
import data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--panel", default="multipref_overall"); ap.add_argument("--fold", type=int, required=True); ap.add_argument("--mode", default="d", choices=("d", "rc"))
ap.add_argument("--lr", type=float, default=1e-4); ap.add_argument("--accum", type=int, default=8); ap.add_argument("--lora_r", type=int, default=16); ap.add_argument("--seed", type=int, default=2000)
ap.add_argument("--rc_pairs", type=int, default=8000); ap.add_argument("--rc_hist", type=int, default=10); ap.add_argument("--ks", default="5,20"); ap.add_argument("--max_steps", type=int, default=-1); ap.add_argument("--tag", default="")
args = ap.parse_args(); f = args.fold; OUT = f"{HERE}/results/lora_rm/{args.panel}/{args.mode}{args.tag}_f{f}"; os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- data and folds (identical to factorised_rm.py)
PAN = data_panels.load(args.panel); H = PAN["H"]; K = PAN["K"]; n, m = H.shape; ev = PAN["evaluators"]
raters = sorted({e for row in ev for e in row}); rid = {r: j for j, r in enumerate(raters)}; NR = len(raters)
I = np.repeat(np.arange(n), m); R = np.array([rid[e] for row in ev for e in row]); Y = H.reshape(-1); POS = np.tile(np.arange(m), n)
GRP = np.zeros(NR, int)
for i in range(len(R)): GRP[R[i]] = int(POS[i] >= 2)
Gp = np.asarray(PAN["groups"]); texts = PAN["texts"]
rs = np.random.RandomState(0); rfold = np.zeros(NR, int)
for g in np.unique(GRP):
    ids = np.where(GRP == g)[0]; ids = ids[rs.permutation(len(ids))]; rfold[ids] = np.arange(len(ids)) % 5
ug = np.unique(Gp); perm = np.random.RandomState(0).permutation(len(ug)); gf = {g_: perm[j] % 5 for j, g_ in enumerate(ug)}; ifold = np.array([gf[g_] for g_ in Gp])
_rv = np.random.RandomState(1).rand(len(ug)); vf = {g_: bool(_rv[j] < 0.15) for j, g_ in enumerate(ug)}
test_r = rfold == f; tr_item = ifold[I] != f; is_tr_r = ~test_r[R]; va_item = np.array([vf[g_] for g_ in Gp])[I]
idx_tr = np.where(is_tr_r & tr_item & ~va_item)[0]; idx_va = np.where(is_tr_r & tr_item & va_item)[0]
idx_ad_pool = np.where(~is_tr_r & tr_item)[0]; idx_te = np.where(~is_tr_r & ~tr_item)[0]
ref = json.load(open(f"{HERE}/results/stage2a_{args.panel}_f{f}.json"))["folds"][0]
assert ref["n_train"] == len(idx_tr) + len(idx_va) and ref["n_test"] == len(idx_te) and ref["n_test_raters"] == int(test_r.sum()), "fold mismatch with stage 2a"

# ---------------------------------------------------------------- model
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model
MODEL = PAN["model"]; tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL, dtype=torch.bfloat16, device_map="cuda")
level_ids = torch.tensor([tok.encode(s, add_special_tokens=False)[0] for s in PAN["LEVEL_STRS"]], device="cuda")
def build(prompt):
    t = tok.apply_chat_template([{"role": "user", "content": prompt}], tokenize=False, add_generation_prompt=True) + PAN["PREFIX"]
    return tok(t, add_special_tokens=False, return_tensors="pt").input_ids
def logq(ids): return torch.log_softmax(model(input_ids=ids.to("cuda")).logits[0, -1][level_ids].float(), -1)
model.gradient_checkpointing_enable(); model.enable_input_require_grads()
model = get_peft_model(model, LoraConfig(r=args.lora_r, lora_alpha=2 * args.lora_r, lora_dropout=0.05, task_type="CAUSAL_LM",
                                          target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]))
opt = torch.optim.AdamW([q for q in model.parameters() if q.requires_grad], lr=args.lr, weight_decay=0.0)
rng = np.random.RandomState(args.seed + f)

# ---------------------------------------------------------------- training examples
if args.mode == "d":
    items = np.unique(I[idx_tr]); hist = {i: np.zeros(K) for i in items}
    for j in idx_tr: hist[I[j]][Y[j]] += 1
    examples = [(int(i), hist[i] / hist[i].sum()) for i in items]
else:
    by_r = {}
    for j in idx_tr: by_r.setdefault(int(R[j]), []).append(int(j))
    pool = [j for j in idx_tr if len(by_r[int(R[j])]) > args.rc_hist]; pick = rng.choice(pool, min(args.rc_pairs, len(pool)), replace=False)
    def hist_of(r, exclude, k, rr):
        cand = [j for j in by_r[r] if j != exclude]; sel = rr.choice(cand, k, replace=False); return [(texts[I[j]], int(Y[j])) for j in sel]
    examples = [(int(j), None) for j in pick]
n_steps = int(math.ceil(len(examples) / args.accum)) if args.max_steps < 0 else args.max_steps
sched = torch.optim.lr_scheduler.LambdaLR(opt, lambda s: min(1.0, (s + 1) / 20) * max(0.0, 1 - s / max(1, n_steps)))
order = list(rng.permutation(len(examples))); model.train(); t0 = time.time(); step = micro = 0; run = 0.0; maxlen = 0
while step < n_steps and order:
    e = examples[order.pop()]
    if args.mode == "d":
        lq = logq(build(PAN["prompt"](texts[e[0]]))); pt = torch.tensor(e[1], device="cuda", dtype=torch.float32); loss = -(pt * lq).sum()
    else:
        j = e[0]; r = int(R[j]); ids = build(PAN["prompt_hist"](texts[I[j]], hist_of(r, j, args.rc_hist, rng))); maxlen = max(maxlen, ids.shape[1]); loss = -logq(ids)[int(Y[j])]
    (loss / args.accum).backward(); run += loss.item() / args.accum; micro += 1
    if micro % args.accum == 0:
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0); opt.step(); sched.step(); opt.zero_grad(); step += 1
        if step % 20 == 0 or step == n_steps: print(f"step {step}/{n_steps} loss {run:.4f} {time.time()-t0:.0f}s maxlen {maxlen} mem {torch.cuda.max_memory_allocated()/1e9:.1f}GB", flush=True)
        run = 0.0
model.eval(); meta = {"panel": args.panel, "fold": f, "mode": args.mode, "n_examples": len(examples), "n_steps": n_steps, "train_s": round(time.time() - t0), "protocol": "PROTOCOL_STAGE2B.md", "args": vars(args)}

# ---------------------------------------------------------------- outputs
with torch.no_grad():
    if args.mode == "d":
        L = np.zeros((n, K), np.float32)
        for i in range(n):
            L[i] = logq(build(PAN["prompt"](texts[i]))).cpu().numpy()
            if (i + 1) % 1000 == 0: print(f"logits {i+1}/{n} [{time.time()-t0:.0f}s]", flush=True)
        np.save(f"{OUT}/L.npy", L); np.save(f"{OUT}/item_ids.npy", np.asarray(PAN["item_ids"]).astype(str))
    else:
        rows = []; test_raters = np.unique(R[idx_te])
        for k in [int(x) for x in args.ks.split(",")]:
            rk = np.random.RandomState(10_000 * f + 100 * k + 0); ad = {}
            for r in test_raters:                                        # same draw sequence as factorised_rm.py (draw 0)
                pool_r = idx_ad_pool[R[idx_ad_pool] == r]
                if len(pool_r) < k: continue
                ad[int(r)] = rk.choice(pool_r, k, replace=False)
            for r, sel in ad.items():
                hist_r = [(texts[I[j]], int(Y[j])) for j in sel]; te_r = idx_te[R[idx_te] == r]
                lp = np.array([logq(build(PAN["prompt_hist"](texts[I[j]], hist_r))).cpu().numpy() for j in te_r])
                yy = Y[te_r]; ll = lp[np.arange(len(te_r)), yy]; pk = np.exp(lp); cdf = np.cumsum(pk, 1); step_ = (np.arange(K)[None, :] >= yy[:, None]).astype(float)
                ey = (pk * np.arange(K)).sum(1); mid = (K - 1) / 2; dirc = np.where(yy == mid, np.nan, (np.sign(ey - mid) == np.sign(yy - mid)).astype(float))
                rows.append({"fold": f, "k": k, "draw": 0, "rater": r, "n": int(len(te_r)), "RC_ll": float(ll.sum()), "RC_rps": float((((cdf - step_) ** 2).sum(1) / (K - 1)).sum()),
                             "RC_dir": float(np.nansum(dirc)), "n_dir": int(np.isfinite(dirc).sum())})
            print(f"rc eval k={k}: {len(ad)} raters [{time.time()-t0:.0f}s]", flush=True)
        meta["per_rater"] = rows
json.dump(meta, open(f"{OUT}/meta.json", "w"), indent=1); print("done", flush=True)
