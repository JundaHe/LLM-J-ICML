"""
Probes 2 + 3 (user 2026-10-11: "先做几个探针… 试一下 Novelty 到底行不行"): is a soft label worth more than (mode, mean)?

Item-only heads on frozen features (same PCA / split / rater protocol as stage_a_heads.py). Training targets:
  hard        one-hot mode
  smooth      label smoothing around the mode, eps tuned on the validation items (Kohli's comparator)
  proto       mode-conditional prototype: mean train histogram of items sharing the mode (class-conditional smoothing)
  mean2       prototype exponentially tilted so the item's mean is matched exactly: p(y) ∝ proto_z(y) exp(lam*y)   -> carries exactly (mode, mean)
  soft        the item's empirical histogram over the training raters (Chen-style target, no adversary)
  soft_pmode  soft with histograms permuted across items within mode cells        (breaks mean + shape)
  soft_pmm    soft with histograms permuted within (mode, mean-bucket) cells        (breaks residual shape only)
Positive control (--inject): a semi-synthetic world where beyond-mean shape IS item-linked: for train AND reference raters, items with
  PCA-component-1 above the train median get their ratings pushed to the extremes (dispersed), below median pulled to the centre (concentrated),
  with mode and mean preserved per item (greedy pairwise moves y-1/y+1 <-> y,y). If the assay is sensitive, soft > mean2 and soft_pmm < soft here.
Metrics on test items vs the 24 held-out reference raters: population RPS, KL to reference histogram, disagreement D Spearman and partial given mean.
Usage: python probe_mean.py --panel dices [--inject] [--seeds 5 --item_splits 3 --rater_splits 2]
"""
import argparse, os, sys, math, itertools, numpy as np, pandas as pd, torch, torch.nn as nn
from paths import LLMJ
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, LLMJ + "/paper-2/idea-stage/pilot")
from support_audit import z_label, random_max_matching
import data_panels
ap = argparse.ArgumentParser()
ap.add_argument("--panel", required=True); ap.add_argument("--feat_key", default="E_last"); ap.add_argument("--d", type=int, default=64); ap.add_argument("--hid", type=int, default=128)
ap.add_argument("--steps", type=int, default=1500); ap.add_argument("--seeds", type=int, default=5); ap.add_argument("--item_splits", type=int, default=3); ap.add_argument("--rater_splits", type=int, default=2)
ap.add_argument("--n_eval_raters", type=int, default=24); ap.add_argument("--tau", type=float, default=0.1); ap.add_argument("--inject", action="store_true"); ap.add_argument("--inject_frac", type=float, default=0.5)
ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu"); ap.add_argument("--tag", default="")
args = ap.parse_args(); DEV = args.device
PAN = data_panels.load(args.panel); H0 = PAN["H"]; N, M = H0.shape; K = PAN["K"]; LV = np.arange(K)
F = np.load(f"{HERE}/features/{args.panel}/{PAN['model'].split('/')[-1]}.npz", allow_pickle=True); E = F[args.feat_key].astype(np.float32)
OUT = f"{HERE}/results/probe_mean/{args.panel}{'_inject' if args.inject else ''}{args.tag}"; os.makedirs(OUT, exist_ok=True)
ARMS = ["hard", "smooth", "proto", "mean2", "soft", "soft_pmode", "soft_pmm"]

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
def tilt(proto, target_mean):
    """exponential tilting of proto to hit target_mean (bisection on lam)"""
    lo, hi = -20.0, 20.0
    for _ in range(60):
        lam = (lo + hi) / 2; p = proto * np.exp(lam * LV); p /= p.sum(); m = p @ LV
        if m < target_mean: lo = lam
        else: hi = lam
    return p

def inject_shape(H, rng, disperse_mask):
    """semi-synthetic shape signal: per item, move pairs of ratings (y, y) -> (y-1, y+1) [disperse] or (y-1, y+1) -> (y, y) [concentrate]; mode & mean preserved."""
    Hn = H.copy()
    for i in range(H.shape[0]):
        r = Hn[i]; z = z_label(r); moves = int(args.inject_frac * len(r) / 2)
        for _ in range(moves):
            if disperse_mask[i]:
                cand = [y for y in range(1, K - 1) if y != z and np.sum(r == y) >= 3]   # keep the mode count untouched (never move the mode level)
                if not cand: break
                y = rng.choice(cand); idx = np.where(r == y)[0][:2]; r[idx[0]], r[idx[1]] = y - 1, y + 1
                if z_label(r) != z: r[idx[0]], r[idx[1]] = y, y; break
            else:
                cand = [y for y in range(1, K - 1) if np.any(r == y - 1) and np.any(r == y + 1) and (y - 1 != z and y + 1 != z)]
                if not cand: break
                y = rng.choice(cand); a = np.where(r == y - 1)[0][0]; b = np.where(r == y + 1)[0][0]; r[a] = r[b] = y
                if z_label(r) != z: r[a], r[b] = y - 1, y + 1; break
        Hn[i] = r
    assert (Hn.mean(1) - H.mean(1)).__abs__().max() < 1e-9
    return Hn

class MLP(nn.Module):
    def __init__(s, d, hid): super().__init__(); s.f = nn.Sequential(nn.Linear(d, hid), nn.GELU(), nn.Linear(hid, K))
    def forward(s, x): return s.f(x)
def train(Xtr, Ptr, Xva, Hva_raters, rng, steps):
    """KL(P_target || q) on train items; early stop on val NLL of the train raters' ratings"""
    torch.manual_seed(int(rng.randint(1 << 30))); m = MLP(Xtr.shape[1], args.hid).to(DEV); opt = torch.optim.Adam(m.parameters(), 1e-3, weight_decay=1e-4)
    Xt = torch.tensor(Xtr, device=DEV); Pt = torch.tensor(Ptr, device=DEV, dtype=torch.float32); Xv = torch.tensor(Xva, device=DEV)
    yv = torch.tensor(Hva_raters.ravel(), device=DEV); xv_rep = Xv.repeat_interleave(Hva_raters.shape[1], 0)
    best = (1e9, None); pat = 0
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
    z = np.array([z_label(r) for r in Htr]); mu = Htr.mean(1); cells = {}
    for i in range(len(Htr)): cells.setdefault((int(z[i]), int(math.floor(mu[i] / args.tau)) if kind == "mm" else 0), []).append(i)
    mp = {}
    for items in cells.values(): mp.update(random_max_matching(items, [tuple(np.bincount(Htr[i], minlength=K)) for i in items], rng))   # histogram classes (Hour-19 dose audit; was rater-vector classes)
    return mp

def run(seed, isplit, rsplit):
    rng = np.random.RandomState(seed * 1000 + isplit * 10 + rsplit)
    G = PAN.get("groups", PAN["item_ids"]); ug = np.unique(G); ug = ug[np.random.RandomState(isplit).permutation(len(ug))]
    g_tr, g_va = set(ug[: int(.6 * len(ug))]), set(ug[int(.6 * len(ug)): int(.7 * len(ug))])
    tr = np.array([i for i in range(N) if G[i] in g_tr]); va = np.array([i for i in range(N) if G[i] in g_va]); te = np.array([i for i in range(N) if G[i] not in g_tr and G[i] not in g_va])
    rp = np.random.RandomState(100 + rsplit).permutation(M); R_eval = np.sort(rp[: args.n_eval_raters]); R_train = np.sort(rp[args.n_eval_raters:])
    dd = min(args.d, len(tr) // 4); mu_e = E[tr].mean(0); U, Sv, Vt = np.linalg.svd(E[tr] - mu_e, full_matrices=False); W = Vt[:dd].T / (Sv[:dd] / math.sqrt(len(tr)) + 1e-6); X = ((E - mu_e) @ W).astype(np.float32)
    H = H0
    if args.inject:   # same shape rule for every rater (train and reference): disperse where PCA-1 is above the train median.
        # Codex round 14: inject SEPARATELY within the realised training-position panel and the evaluation-position panel, so that mode and mean are preserved within each subset (v8); earlier runs injected on the full row.
        disperse = X[:, 0] > np.median(X[tr, 0]); H = H0.copy(); irng = np.random.RandomState(seed)
        H[:, R_train] = inject_shape(H0[:, R_train], irng, disperse); H[:, R_eval] = inject_shape(H0[:, R_eval], irng, disperse)
        assert all(z_label(H[i, R_train]) == z_label(H0[i, R_train]) and abs(H[i, R_train].mean() - H0[i, R_train].mean()) < 1e-9 for i in range(N)), "injection must preserve mode and mean within the training panel"
        assert all(z_label(H[i, R_eval]) == z_label(H0[i, R_eval]) and abs(H[i, R_eval].mean() - H0[i, R_eval].mean()) < 1e-9 for i in range(N)), "injection must preserve mode and mean within the evaluation panel"
    Htr = H[np.ix_(tr, R_train)]; Hva = H[np.ix_(va, R_train)]; Hte = H[np.ix_(te, R_eval)]
    z = np.array([z_label(r) for r in Htr]); mu = Htr.mean(1); hist = np.stack([np.bincount(r, minlength=K) / len(R_train) for r in Htr])
    proto = {c: hist[z == c].mean(0) if (z == c).any() else np.full(K, 1 / K) for c in range(K)}
    ref_hist = np.stack([np.bincount(r, minlength=K) for r in Hte]) / len(R_eval); Dref = D_ref(Hte); mean_ref = Hte.mean(1)
    targets = {"hard": np.eye(K)[z], "proto": np.stack([proto[c] for c in z]), "mean2": np.stack([tilt(proto[c] + 1e-6, m_) for c, m_ in zip(z, mu)]), "soft": hist}
    for kind, name in (("mode", "soft_pmode"), ("mm", "soft_pmm")):
        mp = permute(Htr, kind, rng); T = hist.copy()
        for a, b in mp.items(): T[a] = hist[b]
        targets[name] = T; targets[name + "_cert"] = dict(changed_fraction=len(mp) / len(tr), mean_shift=float(np.mean([abs(mu[a] - mu[b]) for a, b in mp.items()])) if mp else 0.0)
    # tuned label smoothing: pick eps on validation NLL
    best = None
    for eps in (0.02, 0.05, 0.1, 0.2, 0.3, 0.4):
        T = (1 - eps) * np.eye(K)[z] + eps / K; m_, vl = train(X[tr], T, X[va], Hva, rng, args.steps)
        if best is None or vl < best[0]: best = (vl, eps, m_)
    rows = []
    def score(name, P, extra=None):
        Dh = D_pmf(P); row = dict(seed=seed, isplit=isplit, rsplit=rsplit, arm=name, pop_rps=float(np.mean([rps(P, Hte[:, j]).mean() for j in range(len(R_eval))])),
                                  kl_ref=float(np.mean(np.sum(ref_hist * (np.log(ref_hist + 1e-9) - np.log(P + 1e-9)), 1))), D_spearman=float(spearmanr(Dh, Dref).correlation),
                                  D_partial=partial_spearman(Dh, Dref, mean_ref), mean_spearman=float(spearmanr(P @ LV, mean_ref).correlation))
        if extra: row.update(extra)
        rows.append(row); print(f"  s{seed} i{isplit} r{rsplit} {name:11s} popRPS {row['pop_rps']:.4f} KL {row['kl_ref']:.4f} D_rho {row['D_spearman']:+.3f} partial {row['D_partial']:+.3f} mean_rho {row['mean_spearman']:+.3f}", flush=True)
    score("smooth", pmf(best[2], X[te]), dict(eps=best[1]))
    for name in ("hard", "proto", "mean2", "soft", "soft_pmode", "soft_pmm"):
        m_, vl = train(X[tr], targets[name], X[va], Hva, rng, args.steps); score(name, pmf(m_, X[te]), targets.get(name + "_cert"))
    # oracle references on the same test items: what the 2-number target and the full histogram would score if predicted perfectly from the TRAIN raters' panel
    Htr_te = H[np.ix_(te, R_train)]; z_te = np.array([z_label(r) for r in Htr_te]); mu_te = Htr_te.mean(1)
    score("oracle_mean2", np.stack([tilt(proto[c] + 1e-6, m_) for c, m_ in zip(z_te, mu_te)])); score("oracle_soft", np.stack([np.bincount(r, minlength=K) / len(R_train) for r in Htr_te]) + 1e-6)
    score("ref_meanonly_D", np.tile(np.bincount(Htr.ravel(), minlength=K) / Htr.size, (len(te), 1)), dict(D_spearman_meanfit=float(spearmanr(np.polyval(np.polyfit(mu, D_ref(Htr), 2), mean_ref), Dref).correlation)))
    return rows

if __name__ == "__main__":
    rows = []
    for seed, isplit, rsplit in itertools.product(range(args.seeds), range(args.item_splits), range(args.rater_splits)):
        rows += run(seed, isplit, rsplit); pd.DataFrame(rows).to_json(f"{OUT}/runs.jsonl", orient="records", lines=True)
    df = pd.DataFrame(rows); cols = ["pop_rps", "kl_ref", "D_spearman", "D_partial", "mean_spearman"]
    g = df.groupby("arm")[cols].agg(["mean", "sem"]).reindex(["hard", "smooth", "proto", "mean2", "soft", "soft_pmode", "soft_pmm", "oracle_mean2", "oracle_soft"]).round(4)
    open(f"{OUT}/summary.md", "w").write(f"# probe_mean — {args.panel}{' INJECT' if args.inject else ''}: {N}x{M}, K={K}\n\n```\n{g.to_string()}\n```\n")
    print(g.to_string())
