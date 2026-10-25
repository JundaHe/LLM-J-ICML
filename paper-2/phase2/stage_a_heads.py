"""
Stage A — de-risk with frozen LLM features + small heads (Codex review 2026-10-10, "first experiment to run").

Question: does putting the RATER into the input let a judge learn item-level disagreement that an anonymous
histogram objective cannot — and is that attributable to item<->rater interactions rather than rater severity?

Design (per seed x item split x rater split)
  raters : R_train (meta-training raters) | R_eval (never used in training; each gets a support set of k ratings on TRAIN items)
  items  : train 60% | val 10% | test 30%  (seeded)
  phi(x) : PCA(d) of frozen last-layer state of the base LLM (embed_items.py), fit on train items
  models : M0 zero-shot pmf of the frozen LLM (no training)
           M1 item-only, per-rater CE          -> p(y|x)  (anonymous soft target; = histogram learning)
           M1h item-only, mode CE               -> hard baseline
           M2 history-only rater prior          -> smoothed empirical distribution of the support ratings (no item info)
           M3 additive  : f(x) + b(h_r)         -> rater severity/shift from a set-encoder over the support
           M4 interactive: MLP([phi(x), h_r])   -> can represent item x rater interactions
           M5 oracle seen-ID: f(x) + emb(r) + MLP([phi(x), emb(r)]) for R_train raters only (ceiling on held-out items)
  interventions (training data only, R_train x train items):
           itemlink_mode : permute whole rating vectors across train items within mode cells (breaks item<->distribution incl. mean)
           itemlink_mm   : ... within (mode, mean-bucket tau) cells (Phase-1 style; breaks residual shape only)
           interact      : margin-preserving 2x2 swaps (item histograms AND rater marginals preserved; destroys who-disagrees-where)
  metrics (test items)
           per-rater RPS for R_eval raters at support k in {0,4,16,64}
           population RPS: marginal over R_eval raters (k=16) scored against every R_eval rater; KL to R_eval histogram
           disagreement : D_i = E|y-y'|/(K-1) over distinct pairs of R_eval raters (reference) vs predicted D from the model's population pmf;
                          Spearman, top-quartile AUROC, partial Spearman given reference item mean; baselines: mean-only fit, M1h entropy
Usage: python stage_a_heads.py --panel dices [--features features/dices/Qwen2.5-7B-Instruct.npz] [--seeds 5] [--item_splits 3] [--rater_splits 2]
Writes results/stage_a/{panel}/runs.jsonl and summary.md
"""
import argparse, json, os, sys, math, itertools, numpy as np, pandas as pd, torch, torch.nn as nn
from paths import LLMJ
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, LLMJ + "/paper-2/idea-stage/pilot")
from support_audit import z_label, random_max_matching
import data_panels
ap = argparse.ArgumentParser()
ap.add_argument("--panel", required=True); ap.add_argument("--features", default=None); ap.add_argument("--feat_key", default="E_last")
ap.add_argument("--d", type=int, default=64); ap.add_argument("--hid", type=int, default=128); ap.add_argument("--steps", type=int, default=1500)
ap.add_argument("--seeds", type=int, default=5); ap.add_argument("--item_splits", type=int, default=3); ap.add_argument("--rater_splits", type=int, default=2)
ap.add_argument("--n_eval_raters", type=int, default=24); ap.add_argument("--tau", type=float, default=0.1); ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
ap.add_argument("--interventions", default="itemlink_mode,itemlink_mm,interact"); ap.add_argument("--tag", default="")
args = ap.parse_args(); DEV = args.device
PAN = data_panels.load(args.panel); H = PAN["H"]; N, M = H.shape; K = PAN["K"]; LV = np.arange(K)
feat_path = args.features or f"{HERE}/features/{args.panel}/{PAN['model'].split('/')[-1]}.npz"; F = np.load(feat_path, allow_pickle=True)
E = F[args.feat_key].astype(np.float32); Q0 = F["Q0"].astype(np.float64); assert E.shape[0] == N
OUT = f"{HERE}/results/stage_a/{args.panel}{args.tag}"; os.makedirs(OUT, exist_ok=True)
KS = [0, 4, 16, 64]

# ------------------------------------------------------------------ metrics
def rps(P, y):   # P (n,K) pmf, y (n,) int -> (n,)
    cdf = np.cumsum(P, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
def disagreement_from_pmf(P):   # E|y-y'|/(K-1) for y,y' ~ P independent
    D = np.abs(LV[:, None] - LV[None, :]) / (K - 1); return np.einsum("nk,kl,nl->n", P, D, P)
def disagreement_ref(Hs):       # Hs (n, m) ratings of m reference raters -> mean pairwise |y-y'| over distinct pairs
    n, m = Hs.shape; C = np.stack([np.bincount(r, minlength=K) for r in Hs]); tot = np.zeros(n)
    for a in range(K):
        for b in range(K): tot += C[:, a] * C[:, b] * abs(a - b)
    return tot / (m * (m - 1)) / (K - 1)
def auroc(score, label):
    pos, neg = score[label], score[~label]
    if len(pos) == 0 or len(neg) == 0: return float("nan")
    r = pd.Series(score).rank().to_numpy(); return float((r[label].sum() - len(pos) * (len(pos) + 1) / 2) / (len(pos) * len(neg)))
def partial_spearman(x, y, z):
    rx, ry, rz = (pd.Series(v).rank().to_numpy() for v in (x, y, z)); rx, ry, rz = ((v - v.mean()) / (v.std() + 1e-12) for v in (rx, ry, rz))
    bx = (rx * rz).mean(); by = (ry * rz).mean(); ex, ey = rx - bx * rz, ry - by * rz; return float((ex * ey).mean() / (ex.std() * ey.std() + 1e-12))
def mean_only_D(mean_tr, D_tr, mean_te):     # position-effect baseline: quadratic fit of D on item mean (train), applied to test means
    c = np.polyfit(mean_tr, D_tr, 2); return np.polyval(c, mean_te)

# ------------------------------------------------------------------ interventions on the training block Htr (n_tr x |R_train|)
def intervene(Htr, kind, rng):
    Hn = Htr.copy(); n_tr = Htr.shape[0]
    if kind.startswith("itemlink"):
        from collections import defaultdict
        z = np.array([z_label(r) for r in Htr]); mu = Htr.mean(1); cells = defaultdict(list)
        for i in range(n_tr): cells[(int(z[i]), int(math.floor(mu[i] / args.tau)) if kind == "itemlink_mm" else 0)].append(i)
        mp = {}
        for items in cells.values(): mp.update(random_max_matching(items, [tuple(Htr[i]) for i in items], rng))
        for a, b in mp.items(): Hn[a] = Htr[b]
        return Hn, dict(changed_fraction=len(mp) / n_tr, dose_tv=float(np.mean([0.5 * np.abs(np.bincount(Htr[a], minlength=K) - np.bincount(Htr[b], minlength=K)).sum() / Htr.shape[1] for a, b in mp.items()])) if mp else 0.0)
    if kind == "interact":   # 2x2 swaps preserving every item histogram and every rater marginal
        m = Htr.shape[1]; changed = np.zeros_like(Hn, bool); acc = 0; target = int(0.5 * Hn.size); tries = 0
        while acc < target and tries < 400 * target:
            tries += 1; i, j = rng.randint(n_tr, size=2); r, s = rng.randint(m, size=2)
            if i == j or r == s: continue
            a, b, c, d = Hn[i, r], Hn[i, s], Hn[j, r], Hn[j, s]
            if a == d and b == c and a != b:        # swap within item i and within item j: histograms of i and j unchanged; raters r and s keep their multisets
                Hn[i, r], Hn[i, s], Hn[j, r], Hn[j, s] = b, a, d, c; changed[i, r] = changed[i, s] = changed[j, r] = changed[j, s] = True; acc += 2
        assert (np.sort(Hn, 1) == np.sort(Htr, 1)).all() and (np.sort(Hn, 0) == np.sort(Htr, 0)).all()
        return Hn, dict(changed_fraction=float(changed.mean()), swaps=acc // 2)
    raise ValueError(kind)

# ------------------------------------------------------------------ models
class SetEnc(nn.Module):           # DeepSets over support pairs -> h_r
    def __init__(s, din, hid, dout): super().__init__(); s.phi = nn.Sequential(nn.Linear(din, hid), nn.GELU(), nn.Linear(hid, hid)); s.rho = nn.Sequential(nn.GELU(), nn.Linear(hid, dout)); s.empty = nn.Parameter(torch.zeros(dout))
    def forward(s, S, mask):       # S (B,kmax,din), mask (B,kmax) bool
        h = s.phi(S) * mask[..., None]; cnt = mask.sum(1, keepdim=True).clamp(min=1); h = s.rho(h.sum(1) / cnt); return torch.where(mask.any(1, keepdim=True), h, s.empty.expand_as(h))
class Head(nn.Module):
    """kind: item | additive | interactive | oracle"""
    def __init__(s, kind, d, hid, n_r=0):
        super().__init__(); s.kind = kind; s.f = nn.Sequential(nn.Linear(d, hid), nn.GELU(), nn.Linear(hid, K))
        if kind in ("additive", "interactive"): s.enc = SetEnc(d + K + 1 + K, hid, hid)
        if kind == "oracle": s.emb = nn.Embedding(n_r, hid)
        if kind in ("additive", "oracle"): s.b = nn.Linear(hid, K)
        if kind in ("interactive", "oracle"): s.g = nn.Sequential(nn.Linear(d + hid, hid), nn.GELU(), nn.Linear(hid, K))
    def forward(s, x, S=None, mask=None, rid=None):
        out = s.f(x)
        if s.kind == "item": return out
        h = s.enc(S, mask) if s.kind in ("additive", "interactive") else s.emb(rid)
        if s.kind == "additive": return out + s.b(h)
        if s.kind == "interactive": return out + s.g(torch.cat([x, h], -1))
        return out + s.b(h) + s.g(torch.cat([x, h], -1))

def support_tensor(X, Hblk, item_hist, item_mean, raters, items_per_rater, kmax):
    """X (n,d) features of the pool; Hblk (n, m_pool) ratings; for rater index r_j (column of Hblk) use items items_per_rater[j] -> (B,kmax,din), mask"""
    B = len(raters); din = X.shape[1] + K + 1 + K; S = np.zeros((B, kmax, din), np.float32); mask = np.zeros((B, kmax), bool)
    for j, (r, its) in enumerate(zip(raters, items_per_rater)):
        for t, i in enumerate(its[:kmax]):
            y = Hblk[i, r]; S[j, t, : X.shape[1]] = X[i]; S[j, t, X.shape[1] + y] = 1; S[j, t, X.shape[1] + K] = y - item_mean[i]; S[j, t, X.shape[1] + K + 1:] = item_hist[i]; mask[j, t] = True
    return torch.tensor(S, device=DEV), torch.tensor(mask, device=DEV)

def train_head(kind, Xtr, Htr, Xva, Hva, rng, n_r=0, steps=None, batch=256):
    """Htr/Hva: (n_tr, m_train) / (n_va, m_train) ratings of TRAIN raters. Episodic for additive/interactive (support from train items of the same rater)."""
    torch.manual_seed(int(rng.randint(1 << 30))); d = Xtr.shape[1]; m = Htr.shape[1]; model = Head(kind, d, args.hid, n_r=m).to(DEV); opt = torch.optim.Adam(model.parameters(), 1e-3, weight_decay=1e-4)
    Xt = torch.tensor(Xtr, device=DEV); Xv = torch.tensor(Xva, device=DEV); n_tr = Xtr.shape[0]
    hist_tr = np.stack([np.bincount(r, minlength=K) / m for r in Htr]); mean_tr = Htr.mean(1); kmax = 64
    def batch_fn(n_items, Hb, Xb, hist, mean, train_pool=True):
        ii = rng.randint(n_items, size=batch); rr = rng.randint(m, size=batch); y = Hb[ii, rr]
        if kind == "item": return Xb[ii], None, None, None, torch.tensor(y, device=DEV)
        if kind == "oracle": return Xb[ii], None, None, torch.tensor(rr, device=DEV), torch.tensor(y, device=DEV)
        ks = rng.choice(KS, size=batch, p=[.1, .3, .3, .3]); sup = []
        for q, (i, k) in enumerate(zip(ii, ks)):
            pool = np.delete(np.arange(n_tr), i) if train_pool else np.arange(n_tr); sup.append(rng.choice(pool, size=min(k, len(pool)), replace=False) if k > 0 else np.array([], int))
        S, mask = support_tensor(Xtr, Htr, hist_tr, mean_tr, rr, sup, kmax); return Xb[ii], S, mask, None, torch.tensor(y, device=DEV)
    best = (1e9, None); steps = steps or args.steps; patience = 0
    for st in range(steps):
        model.train(); x, S, mask, rid, y = batch_fn(n_tr, Htr, Xt, hist_tr, mean_tr); loss = nn.functional.cross_entropy(model(x, S, mask, rid), y); opt.zero_grad(); loss.backward(); opt.step()
        if st % 50 == 49:
            model.eval()
            with torch.no_grad(): x, S, mask, rid, y = batch_fn(Xva.shape[0], Hva, Xv, hist_tr, mean_tr, train_pool=False); vl = nn.functional.cross_entropy(model(x, S, mask, rid), y).item()
            if vl < best[0] - 1e-4: best = (vl, {k: v.detach().clone() for k, v in model.state_dict().items()}); patience = 0
            else:
                patience += 1
                if patience >= 6: break
    model.load_state_dict(best[1]); model.eval(); return model, dict(val_ce=best[0], steps=st + 1)

def predict(model, kind, X, Xtr, Htr, raters, sup_items, hist_tr, mean_tr):
    """pmf for each (item in X) x (rater j with support sup_items[j]) -> (len(raters), n, K)"""
    out = np.zeros((len(raters), X.shape[0], K)); Xt = torch.tensor(X, device=DEV)
    with torch.no_grad():
        if kind == "item": out[:] = torch.softmax(model(Xt), -1).cpu().numpy()[None]; return out
        for j, (r, its) in enumerate(zip(raters, sup_items)):
            if kind == "oracle": out[j] = torch.softmax(model(Xt, rid=torch.full((X.shape[0],), r, device=DEV, dtype=torch.long)), -1).cpu().numpy(); continue
            S, mask = support_tensor(Xtr, Htr, hist_tr, mean_tr, [r], [its], 64); S = S.expand(X.shape[0], -1, -1); mask = mask.expand(X.shape[0], -1)
            out[j] = torch.softmax(model(Xt, S, mask), -1).cpu().numpy()
    return out
def rater_prior(Htr_sup, k_items, r, pop):   # M2: smoothed empirical pmf of the support ratings (Dirichlet prior = population marginal, strength 2)
    if len(k_items) == 0: return pop
    c = np.bincount(Htr_sup[k_items, r], minlength=K); return (c + 2 * pop) / (c.sum() + 2)

# ------------------------------------------------------------------ one configuration
def run(seed, isplit, rsplit):
    rng = np.random.RandomState(seed * 1000 + isplit * 10 + rsplit)
    ids = np.random.RandomState(isplit).permutation(N); tr, va, te = ids[: int(.6 * N)], ids[int(.6 * N): int(.7 * N)], ids[int(.7 * N):]
    rp = np.random.RandomState(100 + rsplit).permutation(M); R_eval = np.sort(rp[: args.n_eval_raters]); R_train = np.sort(rp[args.n_eval_raters:])
    # features: PCA on train items
    dd = min(args.d, len(tr) // 4); mu_e = E[tr].mean(0); U, Sv, Vt = np.linalg.svd(E[tr] - mu_e, full_matrices=False); W = Vt[: dd].T / (Sv[: dd] / math.sqrt(len(tr)) + 1e-6)
    X = ((E - mu_e) @ W).astype(np.float32)
    Htrain_block = H[np.ix_(tr, R_train)]       # training data: train items x train raters
    res = []
    # reference quantities on test items from R_eval raters
    Hte_eval = H[np.ix_(te, R_eval)]; D_ref = disagreement_ref(Hte_eval); mean_ref = Hte_eval.mean(1); hist_ref = np.stack([np.bincount(r, minlength=K) for r in Hte_eval]) / len(R_eval)
    top = D_ref >= np.quantile(D_ref, .75); pop = np.bincount(Htrain_block.ravel(), minlength=K) / Htrain_block.size
    # support sets for R_eval raters: k train items (fixed per rater & k)
    sup = {k: [rng.choice(tr, size=min(k, len(tr)), replace=False) if k else np.array([], int) for _ in R_eval] for k in KS}
    tr_pos = {i: p for p, i in enumerate(tr)}
    D_tr_ref = disagreement_ref(H[np.ix_(tr, R_train)]); mean_tr_items = H[np.ix_(tr, R_train)].mean(1)
    def record(name, variant, P_pop, per_rater=None, extra=None):
        row = dict(seed=seed, isplit=isplit, rsplit=rsplit, model=name, variant=variant)
        if P_pop is not None:
            D_hat = disagreement_from_pmf(P_pop); row.update(pop_rps=float(np.mean([rps(P_pop, Hte_eval[:, j]).mean() for j in range(len(R_eval))])),
                pop_kl=float(np.mean(np.sum(hist_ref * (np.log(hist_ref + 1e-9) - np.log(P_pop + 1e-9)), 1))),
                D_spearman=float(spearmanr(D_hat, D_ref).correlation), D_auroc=auroc(D_hat, top), D_partial_mean=partial_spearman(D_hat, D_ref, mean_ref),
                mean_spearman=float(spearmanr(P_pop @ LV, mean_ref).correlation))
        if per_rater is not None: row.update({f"rater_rps_k{k}": float(v) for k, v in per_rater.items()})
        if extra: row.update(extra)
        res.append(row); return row
    # baselines on disagreement: mean-only, reference-mean oracle position effect
    record("meanonly_D", "none", None, extra=dict(D_spearman=float(spearmanr(mean_only_D(mean_tr_items, D_tr_ref, mean_ref), D_ref).correlation), D_auroc=auroc(mean_only_D(mean_tr_items, D_tr_ref, mean_ref), top)))
    record("M0_zeroshot", "none", Q0[te], per_rater={k: np.mean([rps(Q0[te], Hte_eval[:, j]).mean() for j in range(len(R_eval))]) for k in KS})
    # M2 history-only prior
    pr = {k: np.mean([rps(np.tile(rater_prior(H[np.ix_(tr, R_eval)], np.array([tr_pos[i] for i in sup[k][j]], int), j, pop), (len(te), 1)), Hte_eval[:, j]).mean() for j in range(len(R_eval))]) for k in KS}
    record("M2_prior", "none", np.tile(pop, (len(te), 1)), per_rater=pr)
    variants = [("none", Htrain_block, {})] + [(kind, *intervene(Htrain_block, kind, rng)) for kind in args.interventions.split(",") if kind]
    for variant, Hblk, cert in variants:
        hist_tr = np.stack([np.bincount(r, minlength=K) / Hblk.shape[1] for r in Hblk]); mean_tr = Hblk.mean(1); Hva = H[np.ix_(va, R_train)]
        for name, kind in (("M1h_hard", "item"), ("M1_item", "item"), ("M3_additive", "additive"), ("M4_interactive", "interactive"), ("M5_oracleID", "oracle")):
            if variant != "none" and name in ("M1h_hard", "M5_oracleID"): continue
            Hfit = np.repeat(np.array([z_label(r) for r in Hblk])[:, None], Hblk.shape[1], 1) if name == "M1h_hard" else Hblk
            model, info = train_head(kind, X[tr], Hfit, X[va], Hva, rng)
            sup_pos = {k: [np.array([tr_pos[i] for i in s], int) for s in sup[k]] for k in KS}
            if kind == "oracle":    # ceiling: seen raters, held-out items
                P = predict(model, kind, X[te], X[tr], Hblk, list(range(len(R_train))), [None] * len(R_train), hist_tr, mean_tr)
                Hte_train = H[np.ix_(te, R_train)]; row = record(name, variant, P.mean(0), per_rater={k: float(np.mean([rps(P[j], Hte_train[:, j]).mean() for j in range(len(R_train))])) for k in KS}, extra=dict(info, **cert))
                print(f"  seed{seed} i{isplit} r{rsplit} {variant:13s} {name:15s} popRPS {row['pop_rps']:.4f} D_rho {row['D_spearman']:+.3f} partial {row['D_partial_mean']:+.3f} seen-rater RPS {row['rater_rps_k0']:.4f} (ceiling)", flush=True); continue
            per = {}; P_pop = None
            for k in KS:
                # R_eval raters: support = their own ratings on k train items (from the ORIGINAL H, they are unseen raters), model sees train-block statistics of the (possibly intervened) block
                P = predict(model, kind, X[te], X[tr], H[np.ix_(tr, R_eval)] if kind != "item" else Hblk, list(range(len(R_eval))), sup_pos[k], hist_tr, mean_tr)
                per[k] = float(np.mean([rps(P[j], Hte_eval[:, j]).mean() for j in range(len(R_eval))]))
                if k == 16 or kind == "item": P_pop = P.mean(0)
            record(name, variant, P_pop, per_rater=per, extra=dict(info, **cert))
            print(f"  seed{seed} i{isplit} r{rsplit} {variant:13s} {name:15s} popRPS {res[-1]['pop_rps']:.4f} D_rho {res[-1]['D_spearman']:+.3f} partial {res[-1]['D_partial_mean']:+.3f} raterRPS k0/16/64 {per[0]:.4f}/{per[16]:.4f}/{per[64]:.4f}", flush=True)
    return res

if __name__ == "__main__":
    rows = []
    for seed, isplit, rsplit in itertools.product(range(args.seeds), range(args.item_splits), range(args.rater_splits)):
        rows += run(seed, isplit, rsplit)
        pd.DataFrame(rows).to_json(f"{OUT}/runs.jsonl", orient="records", lines=True)
    df = pd.DataFrame(rows)
    cols = ["pop_rps", "pop_kl", "D_spearman", "D_partial_mean", "D_auroc", "mean_spearman"] + [f"rater_rps_k{k}" for k in KS]
    g = df.groupby(["variant", "model"])[cols].agg(["mean", "sem"]).round(4)
    with open(f"{OUT}/summary.md", "w") as f:
        f.write(f"# Stage A — {args.panel} ({N} items x {M} raters, K={K}); {args.seeds} seeds x {args.item_splits} item splits x {args.rater_splits} rater splits; d={args.d}\n\n")
        f.write("```\n" + g.to_string() + "\n```\n")
    print(g.to_string())
