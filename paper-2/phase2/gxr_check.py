"""
Prespecified G × R check of the exploratory location explanation (Codex round 6 §3, frozen before running):
  G = rho_within(mu_hat_soft, mu_train | z) − rho_within(mu_hat_pmode, mu_train | z)   measured on VALIDATION items (how much location tracking the item link buys)
  R = rho_within(mu_train, y_eval | z)                                                   measured on VALIDATION items against the held-out reference raters
Prediction, frozen: the raw RPS effect of location disruption, E = RPS(soft_pmode) − RPS(soft) on TEST items, has the same sign as G × R and its rank across
panels follows G × R. Report per panel (mean over configs): G, R, G×R, E; sign concordance; Spearman of G×R vs E across panels; leave-one-panel-out sign check.
Heads protocol identical to probe_mean2 (PCA features, 60/10/30 by group, train/reference rater split, cross-fitted targets not needed here: only soft and pmode).
Usage: python gxr_check.py --panels commit_why,commit_what,bw,dices,summeval_coherence8,summeval_relevance8,scalabrino,hs2_help5
"""
import argparse, os, sys, math, itertools, json, numpy as np, pandas as pd, torch, torch.nn as nn
from paths import LLMJ
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, LLMJ + "/paper-2/idea-stage/pilot")
from support_audit import z_label, random_max_matching
import data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--panels", default="bw,dices,summeval_coherence8,summeval_relevance8,scalabrino,hs2_help5,popquorn_off8,popquorn_pol5,dices990,csc6,emobank_reader_v5")
ap.add_argument("--seeds", type=int, default=3); ap.add_argument("--item_splits", type=int, default=3); ap.add_argument("--rater_splits", type=int, default=2); ap.add_argument("--steps", type=int, default=1500)
ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu"); args = ap.parse_args(); DEV = args.device
NEVAL = {"commit_why": 2, "commit_what": 2, "bw": 24, "dices": 24, "summeval_coherence8": 2, "summeval_relevance8": 2, "scalabrino": 3, "hs2_help5": 2, "popquorn_off8": 2, "dices990": 20, "popquorn_pol5": 1, "csc6": 1, "emobank_reader_v5": 1}
DHID = {"bw": (16, 64), "scalabrino": (16, 64)}
def within_rho(x, y, z):
    x = np.asarray(x, float); y = np.asarray(y, float); z = np.asarray(z); ex = np.zeros(len(x)); ey = np.zeros(len(y))
    for c in np.unique(z):
        m = z == c
        if m.sum() < 3: continue
        rx = pd.Series(x[m]).rank().to_numpy(); ry = pd.Series(y[m]).rank().to_numpy(); ex[m] = rx - rx.mean(); ey[m] = ry - ry.mean()
    return float((ex * ey).mean() / (ex.std() * ey.std() + 1e-12))
class MLP(nn.Module):
    def __init__(s, d, hid, K): super().__init__(); s.f = nn.Sequential(nn.Linear(d, hid), nn.GELU(), nn.Linear(hid, K))
    def forward(s, x): return s.f(x)
def train(Xtr, Ptr, Xva, Hva, K, hid, rng, steps):
    torch.manual_seed(int(rng.randint(1 << 30))); m = MLP(Xtr.shape[1], hid, K).to(DEV); opt = torch.optim.Adam(m.parameters(), 1e-3, weight_decay=1e-4)
    Xt = torch.tensor(Xtr, device=DEV); Pt = torch.tensor(Ptr, device=DEV, dtype=torch.float32); Xv = torch.tensor(Xva, device=DEV); yv = torch.tensor(Hva.ravel(), device=DEV); xv = Xv.repeat_interleave(Hva.shape[1], 0)
    best = (1e9, None); pat = 0
    for st in range(steps):
        m.train(); idx = rng.randint(Xtr.shape[0], size=256); lq = torch.log_softmax(m(Xt[idx]), -1); loss = -(Pt[idx] * lq).sum(1).mean(); opt.zero_grad(); loss.backward(); opt.step()
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
rows = []
for panel in args.panels.split(","):
    PAN = data_panels.load(panel); H0 = PAN["H"]; N, M = H0.shape; K = PAN["K"]; LV = np.arange(K); E = np.load(f"{HERE}/features/{panel}/{PAN['model'].split('/')[-1]}.npz", allow_pickle=True)["E_last"].astype(np.float32)
    d, hid = DHID.get(panel, (64, 128)); n_eval = NEVAL[panel]
    def rps(P, y): cdf = np.cumsum(P, 1); step = (LV[None, :] >= y[:, None]).astype(float); return ((cdf - step) ** 2).sum(1) / (K - 1)
    for seed, isplit, rsplit in itertools.product(range(args.seeds), range(args.item_splits), range(args.rater_splits)):
        rng = np.random.RandomState(seed * 1000 + isplit * 10 + rsplit)
        G = PAN.get("groups", PAN["item_ids"]); ug = np.unique(G); ug = ug[np.random.RandomState(isplit).permutation(len(ug))]
        g_tr, g_va = set(ug[: int(.6 * len(ug))]), set(ug[int(.6 * len(ug)): int(.7 * len(ug))])
        tr = np.array([i for i in range(N) if G[i] in g_tr]); va = np.array([i for i in range(N) if G[i] in g_va]); te = np.array([i for i in range(N) if G[i] not in g_tr and G[i] not in g_va])
        rp = np.random.RandomState(100 + rsplit).permutation(M); R_eval = np.sort(rp[:n_eval]); R_train = np.sort(rp[n_eval:])
        dd = min(d, len(tr) // 4); mu_e = E[tr].mean(0); U, Sv, Vt = np.linalg.svd(E[tr] - mu_e, full_matrices=False); W = Vt[:dd].T / (Sv[:dd] / math.sqrt(len(tr)) + 1e-6); X = ((E - mu_e) @ W).astype(np.float32)
        Htr = H0[np.ix_(tr, R_train)]; Hva = H0[np.ix_(va, R_train)]; Hva_eval = H0[np.ix_(va, R_eval)]; Hte_eval = H0[np.ix_(te, R_eval)]
        z = np.array([z_label(r) for r in Htr]); hist = np.stack([np.bincount(r, minlength=K) / len(R_train) for r in Htr])
        cells = {}
        for i in range(len(tr)): cells.setdefault(int(z[i]), []).append(i)
        mp = {}
        for items in cells.values(): mp.update(random_max_matching(items, [tuple(np.bincount(Htr[i], minlength=K)) for i in items], rng))
        T = hist.copy()
        for a, b in mp.items(): T[a] = hist[b]
        m_soft = train(X[tr], hist, X[va], Hva, K, hid, rng, args.steps); m_pm = train(X[tr], T, X[va], Hva, K, hid, rng, args.steps)
        z_va = np.array([z_label(r) for r in Hva]); mu_va = Hva.mean(1)
        Gv = within_rho(pmf(m_soft, X[va]) @ LV, mu_va, z_va) - within_rho(pmf(m_pm, X[va]) @ LV, mu_va, z_va)
        Rv = float(np.mean([within_rho(mu_va, Hva_eval[:, j], z_va) for j in range(n_eval)]))
        Ev = float(np.mean([rps(pmf(m_pm, X[te]), Hte_eval[:, j]).mean() - rps(pmf(m_soft, X[te]), Hte_eval[:, j]).mean() for j in range(n_eval)]))
        rows.append(dict(panel=panel, seed=seed, isplit=isplit, rsplit=rsplit, G=Gv, R=Rv, GR=Gv * Rv, E=Ev)); print(f"  {panel:20s} s{seed} i{isplit} r{rsplit} G {Gv:+.3f} R {Rv:+.3f} GxR {Gv*Rv:+.4f} E(pmode−soft RPS) {Ev:+.4f}", flush=True)
    pd.DataFrame(rows).to_json(f"{HERE}/results/gxr_check.jsonl", orient="records", lines=True)
df = pd.DataFrame(rows); agg = df.groupby("panel")[["G", "R", "GR", "E"]].agg(["mean", "sem"]).round(4); print(agg.to_string())
m = df.groupby("panel")[["GR", "E"]].mean(); conc = float((np.sign(m.GR) == np.sign(m.E)).mean()); rho = spearmanr(m.GR, m.E).correlation
loo = {p: bool(np.sign(m.GR[p]) == np.sign(m.E[p])) for p in m.index}
out = dict(sign_concordance=conc, spearman_GR_E=float(rho), per_panel=m.round(4).to_dict(), sign_match=loo); print(json.dumps(out, indent=1))
json.dump(out, open(f"{HERE}/results/gxr_check.json", "w"), indent=1)
