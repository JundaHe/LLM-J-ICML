"""
probe_mean2 — heads hierarchy v2 after Codex round 2 (2026-10-11). Fixes/additions over probe_mean.py:
  * cross-fitted prototypes: the mode prototype used for item i excludes item i (leave-one-item-out)
  * shrunk-histogram arm  `shrunk`  : (n p_i + kappa * proto_z) / (n + kappa), kappa tuned on validation  -> matched denoising for the soft target
  * conditional target    `cond`    : cross-fitted E[p_i | z_i, mean-bin(mu_i)] (the natural two-number baseline; falls back to mean2 when the cell has < 3 other items)
  * SORD-mean             `sordm`   : p(y) ∝ exp(-|y - mu_i|^2 / (2 s^2)), s tuned on validation (Diaz & Marathe 2019 with the empirical mean as the centre)
  * SORD-mode             `sordz`   : same centred on the mode
  * exact-mean permutation `soft_pmmx`: donor histogram re-tilted to the recipient's exact mean (mode cell as before) -> no mean leakage through binning
  * `--d 0` uses the full frozen feature vector (capacity control for the PCA-64 bias Codex flagged)
Arms: hard, smooth, proto, mean2, cond, sordz, sordm, shrunk, soft, soft_pmode, soft_pmm, soft_pmmx. Same split / rater protocol / metrics as probe_mean.py.
Usage: python probe_mean2.py --panel commit_what --n_eval_raters 2 [--d 0]
"""
import argparse, os, sys, math, itertools, numpy as np, pandas as pd, torch, torch.nn as nn
from paths import LLMJ
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, LLMJ + "/paper-2/idea-stage/pilot")
from support_audit import z_label, random_max_matching
import data_panels
import targets as tgt
from targets import ordinal_mode_mean, certify_ordinal, assert_valid_ordinal
ap = argparse.ArgumentParser()
ap.add_argument("--panel", required=True); ap.add_argument("--feat_key", default="E_last"); ap.add_argument("--d", type=int, default=64); ap.add_argument("--hid", type=int, default=128)
ap.add_argument("--steps", type=int, default=1500); ap.add_argument("--seeds", type=int, default=5); ap.add_argument("--item_splits", type=int, default=3); ap.add_argument("--rater_splits", type=int, default=2)
ap.add_argument("--n_eval_raters", type=int, default=24); ap.add_argument("--tau", type=float, default=0.1); ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu"); ap.add_argument("--tag", default="")
args = ap.parse_args(); DEV = args.device
PAN = data_panels.load(args.panel); H0 = PAN["H"]; N, M = H0.shape; K = PAN["K"]; LV = np.arange(K)
F = np.load(f"{HERE}/features/{args.panel}/{PAN['model'].split('/')[-1]}.npz", allow_pickle=True); E = F[args.feat_key].astype(np.float32)
OUT = f"{HERE}/results/probe_mean2/{args.panel}{'_full' if args.d == 0 else ''}{args.tag}"; os.makedirs(OUT, exist_ok=True)

def rps(P, y): cdf = np.cumsum(P, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
def D_pmf(P): D = np.abs(LV[:, None] - LV[None, :]) / (K - 1); return np.einsum("nk,kl,nl->n", P, D, P)
def D_ref(Hs):
    n, m = Hs.shape; C = np.stack([np.bincount(r, minlength=K) for r in Hs]); t = np.zeros(n)
    for a in range(K):
        for b in range(K): t += C[:, a] * C[:, b] * abs(a - b)
    return t / (m * (m - 1)) / (K - 1)
def partial_spearman(x, y, z):
    rx, ry, rz = (pd.Series(v).rank().to_numpy() for v in (x, y, z)); rx, ry, rz = ((v - v.mean()) / (v.std() + 1e-12) for v in (rx, ry, rz))
    ex, ey = rx - (rx * rz).mean() * rz, ry - (ry * rz).mean() * rz; return float((ex * ey).mean() / (ex.std() * ey.std() + 1e-12))
def tilt(pr, m):
    lo, hi = -20.0, 20.0
    for _ in range(60):
        lam = (lo + hi) / 2; p = pr * np.exp(lam * LV); p /= p.sum()
        if p @ LV < m: lo = lam
        else: hi = lam
    return p
def gauss(c, s): p = np.exp(-(LV - c) ** 2 / (2 * s ** 2)); return p / p.sum()

class MLP(nn.Module):
    def __init__(s, d, hid): super().__init__(); s.f = nn.Sequential(nn.Linear(d, hid), nn.GELU(), nn.Linear(hid, K))
    def forward(s, x): return s.f(x)
def train(Xtr, Ptr, Xva, Hva, rng, steps):
    torch.manual_seed(int(rng.randint(1 << 30))); m = MLP(Xtr.shape[1], args.hid).to(DEV); opt = torch.optim.Adam(m.parameters(), 1e-3, weight_decay=1e-4 if Xtr.shape[1] <= 256 else 1e-3)
    Xt = torch.tensor(Xtr, device=DEV); Pt = torch.tensor(Ptr, device=DEV, dtype=torch.float32); Xv = torch.tensor(Xva, device=DEV)
    yv = torch.tensor(Hva.ravel(), device=DEV); xv_rep = Xv.repeat_interleave(Hva.shape[1], 0); best = (1e9, None); pat = 0
    for st in range(steps):
        m.train(); idx = rng.randint(Xtr.shape[0], size=256); lq = torch.log_softmax(m(Xt[idx]), -1); loss = -(Pt[idx] * lq).sum(1).mean(); opt.zero_grad(); loss.backward(); opt.step()
        if st % 50 == 49:
            m.eval()
            with torch.no_grad(): vl = nn.functional.cross_entropy(m(xv_rep), yv).item()
            if vl < best[0] - 1e-4: best = (vl, {k: v.clone() for k, v in m.state_dict().items()}); pat = 0
            else:
                pat += 1
                if pat >= 6: break
    m.load_state_dict(best[1]); m.eval(); return m, best[0]
def pmf(m, X):
    with torch.no_grad(): return torch.softmax(m(torch.tensor(X, device=DEV)), -1).cpu().numpy().astype(np.float64)
def permute(Htr, kind, rng):
    """randomised maximum matching within cells on HISTOGRAM classes (same as train_judge_v2): two items are only paired if their histograms differ,
    so every mapped item receives a genuinely different target (Codex round 8 dose audit: vector-based matching had paired items with identical histograms)"""
    z = np.array([z_label(r) for r in Htr]); mu = Htr.mean(1); cells = {}
    for i in range(len(Htr)): cells.setdefault((int(z[i]), int(math.floor(mu[i] / args.tau)) if kind == "mm" else 0), []).append(i)
    mp = {}
    for items in cells.values(): mp.update(random_max_matching(items, [tuple(np.bincount(Htr[i], minlength=K)) for i in items], rng))
    assert all(np.bincount(Htr[a], minlength=K).tolist() != np.bincount(Htr[b], minlength=K).tolist() for a, b in mp.items())
    return mp

def run(seed, isplit, rsplit):
    rng = np.random.RandomState(seed * 1000 + isplit * 10 + rsplit)
    G = PAN.get("groups", PAN["item_ids"]); ug = np.unique(G); ug = ug[np.random.RandomState(isplit).permutation(len(ug))]
    g_tr, g_va = set(ug[: int(.6 * len(ug))]), set(ug[int(.6 * len(ug)): int(.7 * len(ug))])
    tr = np.array([i for i in range(N) if G[i] in g_tr]); va = np.array([i for i in range(N) if G[i] in g_va]); te = np.array([i for i in range(N) if G[i] not in g_tr and G[i] not in g_va])
    rp = np.random.RandomState(100 + rsplit).permutation(M); R_eval = np.sort(rp[: args.n_eval_raters]); R_train = np.sort(rp[args.n_eval_raters:])
    if args.d > 0:
        dd = min(args.d, len(tr) // 4); mu_e = E[tr].mean(0); U, Sv, Vt = np.linalg.svd(E[tr] - mu_e, full_matrices=False); W = Vt[:dd].T / (Sv[:dd] / math.sqrt(len(tr)) + 1e-6); X = ((E - mu_e) @ W).astype(np.float32)
    else:
        mu_e, sd_e = E[tr].mean(0), E[tr].std(0) + 1e-6; X = ((E - mu_e) / sd_e).astype(np.float32)
    Htr = H0[np.ix_(tr, R_train)]; Hva = H0[np.ix_(va, R_train)]; Hte = H0[np.ix_(te, R_eval)]; n_r = len(R_train)
    z = np.array([z_label(r) for r in Htr]); mu = Htr.mean(1); hist = np.stack([np.bincount(r, minlength=K) / n_r for r in Htr])
    # cross-fitted (leave-one-item-out) prototypes and conditional targets
    proto_loo = np.zeros_like(hist); cond = np.zeros_like(hist); bins = np.floor(mu / 0.25).astype(int)
    for i in range(len(tr)):
        same = (z == z[i]); same[i] = False
        proto_loo[i] = hist[same].mean(0) if same.any() else np.full(K, 1 / K)
        cell = same & (bins == bins[i])
        cond[i] = hist[cell].mean(0) if cell.sum() >= 3 else tilt(proto_loo[i] + 1e-6, mu[i])
    ref_hist = np.stack([np.bincount(r, minlength=K) for r in Hte]) / len(R_eval); Dref = D_ref(Hte); mean_ref = Hte.mean(1)
    tgt.reset_status(); mean2_t = np.stack([ordinal_mode_mean(proto_loo[i], int(z[i]), mu[i], feasible=hist[i]) for i in range(len(tr))]); cert_m2 = assert_valid_ordinal(mean2_t, z, mu, "mean2"); cert_m2.update({f"status_{k}": v for k, v in tgt.STATUS.items()})   # hard-fail + projection-status log
    targets = {"hard": np.eye(K)[z], "proto": proto_loo, "mean2": mean2_t, "cond": cond, "soft": hist}; targets["mean2_cert"] = cert_m2
    targets["shrunk_res_base"] = mean2_t      # residual-only shrinkage: toward a target with the SAME mode and mean
    for kind, name in (("mode", "soft_pmode"), ("mm", "soft_pmm")):
        mp = permute(Htr, kind, rng); T = hist.copy()
        for a, b in mp.items(): T[a] = hist[b]
        targets[name] = T; targets[name + "_cert"] = dict(changed_fraction=len(mp) / len(tr), mean_shift=float(np.mean([abs(mu[a] - mu[b]) for a, b in mp.items()])) if mp else 0.0,
                                                          dose_tv=float(np.mean([0.5 * np.abs(hist[a] - hist[b]).sum() for a, b in mp.items()])) if mp else 0.0)
        if kind == "mm":   # exact mode-and-mean variant: project the donor's shape onto {mean = recipient mean, mode = recipient mode}
            Tx = hist.copy()
            tgt.reset_status()
            for a, b in mp.items(): Tx[a] = ordinal_mode_mean(hist[b], int(z[a]), mu[a], feasible=hist[a])
            n_unchanged = int(sum(np.allclose(Tx[a], hist[a]) for a in mp)); st = {f"status_{k}": v for k, v in tgt.STATUS.items()}
            targets["soft_pmmx"] = Tx; targets["soft_pmmx_cert"] = dict(changed_fraction=len(mp) / len(tr), changed_after_projection=(len(mp) - n_unchanged) / len(tr), mean_shift=0.0, **assert_valid_ordinal(Tx, z, mu, "soft_pmmx"), **st)
    rows = []
    def score(name, P, extra=None):
        Dh = D_pmf(P); row = dict(seed=seed, isplit=isplit, rsplit=rsplit, arm=name, pop_rps=float(np.mean([rps(P, Hte[:, j]).mean() for j in range(len(R_eval))])),
                                  kl_ref=float(np.mean(np.sum(ref_hist * (np.log(ref_hist + 1e-9) - np.log(P + 1e-9)), 1))), D_spearman=float(spearmanr(Dh, Dref).correlation),
                                  D_partial=partial_spearman(Dh, Dref, mean_ref), mean_spearman=float(spearmanr(P @ LV, mean_ref).correlation))
        if extra: row.update(extra)
        rows.append(row); print(f"  s{seed} i{isplit} r{rsplit} {name:10s} popRPS {row['pop_rps']:.4f} KL {row['kl_ref']:.4f} D_rho {row['D_spearman']:+.3f} partial {row['D_partial']:+.3f}", flush=True)
    def tuned(make, grid, label):
        best = None
        for g in grid:
            m_, vl = train(X[tr], make(g), X[va], Hva, rng, args.steps)
            if best is None or vl < best[0]: best = (vl, g, m_)
        score(label, pmf(best[2], X[te]), {"param": best[1]})
    tuned(lambda e: (1 - e) * np.eye(K)[z] + e / K, (0.02, 0.05, 0.1, 0.2, 0.3, 0.4), "smooth")
    tuned(lambda s: np.stack([gauss(c, s) for c in z]), (0.3, 0.5, 0.75, 1.0, 1.5), "sordz")
    tuned(lambda s: np.stack([gauss(c, s) for c in mu]), (0.3, 0.5, 0.75, 1.0, 1.5), "sordm")
    tuned(lambda kap: (n_r * hist + kap * proto_loo) / (n_r + kap), (0.5, 1, 2, 4, 8), "shrunk")
    tuned(lambda w: (1 - w) * hist + w * proto_loo, (0.25, 0.5, 0.75, 0.9), "shrunk_strong")          # prototype weight as a fraction (Codex: kappa <= 8 vs n = 97 was <= 7.6 %)
    tuned(lambda w: (1 - w) * hist + w * targets["shrunk_res_base"], (0.25, 0.5, 0.75, 0.9), "shrunk_res")   # residual-only shrinkage: mode and mean of the histogram are preserved exactly
    for name in ("hard", "proto", "mean2", "cond", "soft", "soft_pmode", "soft_pmm", "soft_pmmx"):
        m_, vl = train(X[tr], targets[name], X[va], Hva, rng, args.steps); score(name, pmf(m_, X[te]), targets.get(name + "_cert"))
    return rows

if __name__ == "__main__":
    rows = []
    for seed, isplit, rsplit in itertools.product(range(args.seeds), range(args.item_splits), range(args.rater_splits)):
        rows += run(seed, isplit, rsplit); pd.DataFrame(rows).to_json(f"{OUT}/runs.jsonl", orient="records", lines=True)
    df = pd.DataFrame(rows); cols = ["pop_rps", "kl_ref", "D_spearman", "D_partial"]
    order = ["hard", "smooth", "sordz", "proto", "sordm", "mean2", "cond", "shrunk", "shrunk_strong", "shrunk_res", "soft", "soft_pmode", "soft_pmm", "soft_pmmx"]
    g = df.groupby("arm")[cols].agg(["mean", "sem"]).reindex(order).round(4)
    open(f"{OUT}/summary.md", "w").write(f"# probe_mean2 — {args.panel} (d={args.d}): {N}x{M}, K={K}\n\n```\n{g.to_string()}\n```\n"); print(g.to_string())
