"""
Heads-vs-LoRA bridge on the commit panels (Codex round 9 §D.3): frozen-feature heads trained on EXACTLY the LoRA partition and targets.
  * items: split-0 train/calib/test taken from the LoRA run's items_calib.csv / items_test.csv (row indices into the CM-benchmark order used by both pipelines)
  * raters: LORO fold e (evaluator e held out); targets from the other five raters, as in train_judge_v2
  * perm_mode target: re-derived with train_judge_v2's exact cell structure (msg_type pool, mode) and histogram-class randomised maximum matching, perm_seed 1000;
    the realised changed count is asserted against the LoRA meta.json so the heads receive the SAME donor assignment the LoRA judge received
  * heads: PCA-64 of Qwen2.5-Coder-7B last-token features, MLP(128), KL to the target, early stopping on calib items vs the five training raters; 5 optimizer seeds
  * metric: raw RPS against the held-out rater e on the test items; contrast pmode − soft (heads) vs perm_mode − chen (LoRA), hard − soft vs hard − chen
Differences that REMAIN between pipelines after this bridge: objective (plain KL vs Chen's KL + adversarial), representation updating (frozen vs LoRA), head capacity.
Usage: python bridge_commit.py --criterion what|why [--seeds 5] [--device cpu]
"""
import argparse, os, sys, json, math, numpy as np, pandas as pd, torch, torch.nn as nn
from paths import LLMJ
from collections import defaultdict
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, LLMJ + "/paper-2/idea-stage/pilot")
from support_audit import z_label, random_max_matching
import data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--criterion", default="what"); ap.add_argument("--seeds", type=int, default=5); ap.add_argument("--steps", type=int, default=1500)
ap.add_argument("--device", default="cpu"); ap.add_argument("--B", type=int, default=2000); args = ap.parse_args(); DEV = args.device
LORA = f"{LLMJ}/paper-2/idea-stage/pilot/results_v2/{args.criterion}/s0"
PAN = data_panels.load(f"commit_{args.criterion}"); H = PAN["H"]; K = PAN["K"]; LV = np.arange(K); pools = PAN["pools"]; N, M = H.shape
E = np.load(f"{HERE}/features/commit_{args.criterion}/Qwen2.5-Coder-7B-Instruct.npz", allow_pickle=True)["E_last"].astype(np.float32)
def rps(P, y): cdf = np.cumsum(P, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
class MLP(nn.Module):
    def __init__(s, d, hid, K): super().__init__(); s.f = nn.Sequential(nn.Linear(d, hid), nn.GELU(), nn.Linear(hid, K))
    def forward(s, x): return s.f(x)
def train(Xtr, Ptr, Xva, Hva, seed):
    torch.manual_seed(seed); rng = np.random.RandomState(seed); m = MLP(Xtr.shape[1], 128, K).to(DEV); opt = torch.optim.Adam(m.parameters(), 1e-3, weight_decay=1e-4)
    Xt = torch.tensor(Xtr, device=DEV); Pt = torch.tensor(Ptr, device=DEV, dtype=torch.float32); xv = torch.tensor(Xva, device=DEV).repeat_interleave(Hva.shape[1], 0); yv = torch.tensor(Hva.ravel(), device=DEV)
    best = (1e9, None); pat = 0
    for st in range(args.steps):
        m.train(); idx = rng.randint(Xtr.shape[0], size=256); loss = -(Pt[idx] * torch.log_softmax(m(Xt[idx]), -1)).sum(1).mean(); opt.zero_grad(); loss.backward(); opt.step()
        if st % 50 == 49:
            m.eval()
            with torch.no_grad(): vl = nn.functional.cross_entropy(m(xv), yv).item()
            if vl < best[0] - 1e-4: best = (vl, {k: v.clone() for k, v in m.state_dict().items()}); pat = 0
            else:
                pat += 1
                if pat >= 6: break
    m.load_state_dict(best[1]); m.eval(); return m
def pmf(m, X):
    with torch.no_grad(): return torch.softmax(m(torch.tensor(X, device=DEV)), -1).cpu().numpy().astype(np.float64)
rows = []; summary = []
for e in range(M):
    ref = f"{LORA}/f{e}/chen"
    if not os.path.exists(f"{ref}/P_test.npy"): print(f"fold {e}: no LoRA chen run, skipped"); continue
    it = pd.read_csv(f"{ref}/items_test.csv"); ic = pd.read_csv(f"{ref}/items_calib.csv"); te = it.row.to_numpy(); ca = ic.row.to_numpy(); tr = np.array(sorted(set(range(N)) - set(te) - set(ca)))
    T = [r for r in range(M) if r != e]; Ht = H[:, T]; z = np.array([z_label(r) for r in Ht]); P_emp = np.stack([np.bincount(r, minlength=K) / len(T) for r in Ht])
    # --- re-derive the LoRA perm_mode donor assignment (train_judge_v2 logic: cells (pool, mode), histogram classes, perm_seed 1000, cells in tr order)
    prng = np.random.RandomState(1000); cells = defaultdict(list)
    for i in tr: cells[(pools[i], int(z[i]), 0)].append(int(i))
    mapping = {}
    for key, items in cells.items():
        hk = [tuple(np.bincount(Ht[i], minlength=K)) for i in items]
        for a, b in random_max_matching(items, hk, prng).items(): assert np.bincount(Ht[a], minlength=K).tolist() != np.bincount(Ht[b], minlength=K).tolist(); mapping[a] = b
    meta_pm = json.load(open(f"{LORA}/f{e}/perm_mode/meta.json")) if os.path.exists(f"{LORA}/f{e}/perm_mode/meta.json") else None
    import hashlib; mh = hashlib.sha1(str(sorted((int(a), int(b)) for a, b in mapping.items())).encode()).hexdigest(); hash_match = (meta_pm or {}).get("mapping_hash") == mh if meta_pm and "mapping_hash" in meta_pm else None
    th = hashlib.sha1(np.round(np.stack([P_emp[mapping.get(int(i), int(i))] for i in tr]), 6).tobytes()).hexdigest(); target_hash_match = (meta_pm or {}).get("target_hash") == th if meta_pm and "target_hash" in meta_pm else None
    aligned = meta_pm is not None and meta_pm["n_changed"] == len(mapping) and abs(meta_pm["dose_tv_mean"] - float(np.mean([0.5 * np.abs(P_emp[a] - P_emp[b]).sum() for a, b in mapping.items()]))) < 1e-6
    T_pm = P_emp.copy()
    for a, b in mapping.items(): T_pm[a] = P_emp[b]
    targets = {"soft": P_emp, "pmode": T_pm, "hard": np.eye(K)[z]}
    # --- features: PCA-64 on train items
    mu_e = E[tr].mean(0); U, Sv, Vt = np.linalg.svd(E[tr] - mu_e, full_matrices=False); W = Vt[:64].T / (Sv[:64] / math.sqrt(len(tr)) + 1e-6); X = ((E - mu_e) @ W).astype(np.float32)
    y = H[te, e]; preds = {a: [] for a in targets}
    for s in range(args.seeds):
        for a, Tg in targets.items(): preds[a].append(pmf(train(X[tr], Tg[tr], X[ca], Ht[ca], 10 * s + e), X[te]))
    per_item = {a: np.mean([rps(P, y) for P in preds[a]], 0) for a in targets}                       # seed-averaged per-item losses
    seed_c = {a: [rps(P, y).mean() - rps(Ps, y).mean() for P, Ps in zip(preds[a], preds["soft"])] for a in ("pmode", "hard")}
    # --- LoRA side on the same test items / evaluator
    lora = {}
    for arm in ("chen", "perm_mode", "hard"):
        f = f"{LORA}/f{e}/{arm}/P_test.npy"
        if os.path.exists(f):
            it2 = pd.read_csv(f"{LORA}/f{e}/{arm}/items_test.csv"); assert (it2.row.to_numpy() == te).all(); lora[arm] = rps(np.load(f), y)
    # --- hash-clustered bootstrap over test items for the per-fold contrasts (seed-averaged heads; LoRA single run)
    gid = pd.factorize(it.hash)[0]; groups = [np.where(gid == g)[0] for g in np.unique(gid)]; rng = np.random.RandomState(e)
    def boot(diff):
        v = []
        for _ in range(args.B):
            idx = np.concatenate([groups[g] for g in rng.choice(len(groups), len(groups), replace=True)]); v.append(diff[idx].mean())
        return np.percentile(v, [2.5, 97.5])
    r = dict(fold=e, aligned_with_lora_meta=bool(aligned), mapping_hash=mh, mapping_hash_match=hash_match, target_hash=th, target_hash_match=target_hash_match, n_changed=len(mapping), n_train=len(tr), n_test=len(te),
             heads_pmode_minus_soft=float(per_item["pmode"].mean() - per_item["soft"].mean()), heads_pmode_ci=boot(per_item["pmode"] - per_item["soft"]).tolist(), heads_pmode_seed_sem=float(np.std(seed_c["pmode"], ddof=1) / math.sqrt(args.seeds)),
             heads_hard_minus_soft=float(per_item["hard"].mean() - per_item["soft"].mean()), heads_hard_ci=boot(per_item["hard"] - per_item["soft"]).tolist(),
             heads_soft_rps=float(per_item["soft"].mean()), lora_chen_rps=float(lora["chen"].mean()))
    if "perm_mode" in lora: r.update(lora_pmode_minus_chen=float((lora["perm_mode"] - lora["chen"]).mean()), lora_pmode_ci=boot(lora["perm_mode"] - lora["chen"]).tolist())
    if "hard" in lora: r.update(lora_hard_minus_chen=float((lora["hard"] - lora["chen"]).mean()), lora_hard_ci=boot(lora["hard"] - lora["chen"]).tolist())
    rows.append(r); print(json.dumps(r), flush=True)
df = pd.DataFrame(rows); os.makedirs(f"{HERE}/results/bridge", exist_ok=True); df.to_json(f"{HERE}/results/bridge/commit_{args.criterion}.jsonl", orient="records", lines=True)
print(f"\n### bridge commit {args.criterion}: {len(df)} folds; aligned donor assignment in {int(df.aligned_with_lora_meta.sum())}/{len(df)} folds")
for c in ("heads_pmode_minus_soft", "lora_pmode_minus_chen", "heads_hard_minus_soft", "lora_hard_minus_chen"):
    if c in df: print(f"  {c:24s} mean over folds {df[c].mean():+.4f}  (fold SEM {df[c].sem():.4f})  folds {[round(x, 4) for x in df[c]]}")
