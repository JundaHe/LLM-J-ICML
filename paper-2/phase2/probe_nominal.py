"""
probe_nominal — the ChaosNLI analogue of the decomposition (Codex round 2, "highest-value experiment").
For NOMINAL classes a histogram p decomposes into: z = modal class, c = modal mass p_z, and the residual allocation of 1-c between the two
non-modal classes. Targets (frozen-feature heads, same protocol as probe_mean2):
  hard    one-hot z
  smooth  tuned label smoothing
  proto   cross-fitted class-conditional prototype E[p | z]                       (mode only)
  zc      prototype rescaled so that p_z = c exactly, non-modal ratio from the prototype  (mode + modal mass: the nominal "two numbers")
  cond    cross-fitted E[p | z, c-bin]                                             (two numbers, empirical)
  shrunk  (m p + kappa proto)/(m + kappa), kappa tuned                             (matched denoising)
  soft    the training-position histogram (m positions)
  soft_pmode  histograms permuted across items within z cells                       (breaks c and residual)
  soft_pzc    permuted within (z, c-bin) cells, then rescaled to the recipient's exact c (breaks residual allocation only)
Panel sizes: --m training positions per item in {5,10,20,50}; the reference = the remaining positions (>= 50) -> KL to reference, entropy Spearman,
and residual-allocation recovery: Spearman between predicted and reference share of the first non-modal class among non-modal mass (conditional on z).
Usage: python probe_nominal.py --panel chaosnli_mnli --m 10
"""
import argparse, os, sys, math, itertools, numpy as np, pandas as pd, torch, torch.nn as nn
from paths import LLMJ
from scipy.stats import spearmanr
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, LLMJ + "/paper-2/idea-stage/pilot")
from support_audit import random_max_matching
import data_panels
from targets import nominal_zc, certify_nominal, assert_valid_nominal
ap = argparse.ArgumentParser()
ap.add_argument("--panel", default="chaosnli_mnli"); ap.add_argument("--m", type=int, default=10, help="training positions per item"); ap.add_argument("--n_ref", type=int, default=50)
ap.add_argument("--d", type=int, default=64); ap.add_argument("--hid", type=int, default=128); ap.add_argument("--steps", type=int, default=1500)
ap.add_argument("--seeds", type=int, default=3); ap.add_argument("--item_splits", type=int, default=3); ap.add_argument("--cbin", type=float, default=0.1)
ap.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu"); ap.add_argument("--tag", default="")
args = ap.parse_args(); DEV = args.device
PAN = data_panels.load(args.panel); H0 = PAN["H"]; N, M = H0.shape; K = PAN["K"]
F = np.load(f"{HERE}/features/{args.panel}/{PAN['model'].split('/')[-1]}.npz", allow_pickle=True); E = F[args.feat_key if hasattr(args, 'feat_key') else "E_last"].astype(np.float32)
OUT = f"{HERE}/results/probe_nominal/{args.panel}_m{args.m}{args.tag}"; os.makedirs(OUT, exist_ok=True)

def ent(P): return -(P * np.log(P + 1e-12)).sum(1)
def hist_of(Hs): return np.stack([np.bincount(r, minlength=K) for r in Hs]) / Hs.shape[1]
def resid_share(P, z):   # share of the lowest-index non-modal class among non-modal mass
    out = np.zeros(len(P))
    for i, (p, zi) in enumerate(zip(P, z)):
        others = [k for k in range(K) if k != zi]; s = p[others].sum(); out[i] = p[others[0]] / s if s > 1e-9 else 0.5
    return out
def rescale_to_c(proto, zi, c): return nominal_zc(proto, zi, c)      # constrained: q_z = c and q_k <= c (Codex round 4)

class MLP(nn.Module):
    def __init__(s, d, hid): super().__init__(); s.f = nn.Sequential(nn.Linear(d, hid), nn.GELU(), nn.Linear(hid, K))
    def forward(s, x): return s.f(x)
def train(Xtr, Ptr, Xva, Pva, rng, steps):
    torch.manual_seed(int(rng.randint(1 << 30))); m = MLP(Xtr.shape[1], args.hid).to(DEV); opt = torch.optim.Adam(m.parameters(), 1e-3, weight_decay=1e-4)
    Xt = torch.tensor(Xtr, device=DEV); Pt = torch.tensor(Ptr, device=DEV, dtype=torch.float32); Xv = torch.tensor(Xva, device=DEV); Pv = torch.tensor(Pva, device=DEV, dtype=torch.float32)
    best = (1e9, None); pat = 0
    for st in range(steps):
        m.train(); idx = rng.randint(Xtr.shape[0], size=256); lq = torch.log_softmax(m(Xt[idx]), -1); loss = -(Pt[idx] * lq).sum(1).mean(); opt.zero_grad(); loss.backward(); opt.step()
        if st % 50 == 49:
            m.eval()
            with torch.no_grad(): vl = -(Pv * torch.log_softmax(m(Xv), -1)).sum(1).mean().item()    # CE against the validation items' training-position histograms
            if vl < best[0] - 1e-4: best = (vl, {k: v.clone() for k, v in m.state_dict().items()}); pat = 0
            else:
                pat += 1
                if pat >= 6: break
    m.load_state_dict(best[1]); m.eval(); return m, best[0]
def pmf(m, X):
    with torch.no_grad(): return torch.softmax(m(torch.tensor(X, device=DEV)), -1).cpu().numpy().astype(np.float64)

def run(seed, isplit):
    rng = np.random.RandomState(seed * 1000 + isplit)
    ids = np.random.RandomState(isplit).permutation(N); tr, va, te = ids[: int(.6 * N)], ids[int(.6 * N): int(.7 * N)], ids[int(.7 * N):]
    # fixed reference panel for every m (Codex round 3): annotation-subsample seed separate from the optimiser seed; reference = positions 50..99 of the same permutation
    pos = np.random.RandomState(900 + isplit).permutation(M); P_train, P_ref = pos[: args.m], pos[M - args.n_ref:]
    assert args.m <= M - args.n_ref
    dd = min(args.d, len(tr) // 4); mu_e = E[tr].mean(0); U, Sv, Vt = np.linalg.svd(E[tr] - mu_e, full_matrices=False); W = Vt[:dd].T / (Sv[:dd] / math.sqrt(len(tr)) + 1e-6); X = ((E - mu_e) @ W).astype(np.float32)
    Htr = H0[np.ix_(tr, P_train)]; Hva = H0[np.ix_(va, P_train)]; Hte_ref = H0[np.ix_(te, P_ref)]
    hist = hist_of(Htr); z = hist.argmax(1); c = hist.max(1); cb = np.floor(c / args.cbin).astype(int); Pva = hist_of(Hva)
    proto = np.zeros_like(hist); cond = np.zeros_like(hist)
    for i in range(len(tr)):
        same = (z == z[i]); same[i] = False; proto[i] = hist[same].mean(0) if same.any() else np.full(K, 1 / K)
        cell = same & (cb == cb[i]); cond[i] = hist[cell].mean(0) if cell.sum() >= 3 else rescale_to_c(proto[i], z[i], c[i])
    ref_hist = hist_of(Hte_ref); z_ref = ref_hist.argmax(1); ent_ref = ent(ref_hist); rs_ref = resid_share(ref_hist, z_ref)
    targets = {"hard": np.eye(K)[z], "proto": proto, "zc": np.stack([rescale_to_c(proto[i], z[i], c[i]) for i in range(len(tr))]), "cond": cond, "soft": hist}
    targets["zc_cert"] = assert_valid_nominal(targets["zc"], z, c, "zc")
    for kind, name in (("mode", "soft_pmode"), ("zc", "soft_pzc")):
        cells = {}
        for i in range(len(tr)): cells.setdefault((int(z[i]), int(cb[i]) if kind == "zc" else 0), []).append(i)
        mp = {}
        for items in cells.values(): mp.update(random_max_matching(items, [tuple(np.bincount(Htr[i], minlength=K)) for i in items], rng))   # histogram classes (Codex round 8 dose audit)
        T = hist.copy()
        for a, b in mp.items(): T[a] = rescale_to_c(hist[b], z[a], c[a]) if kind == "zc" else hist[b]
        tv_m = np.array([0.5 * np.abs(hist[a] - hist[b]).sum() for a, b in mp.items()]); tv_final = np.array([0.5 * np.abs(T[a] - hist[a]).sum() for a in mp])   # donor TV and post-rescaling TV
        hk = [tuple(np.bincount(Htr[i], minlength=K)) for i in range(len(tr))]; het = sum(len(items) for items in cells.values() if len({hk[i] for i in items}) >= 2) / len(tr)
        targets[name] = T; targets[name + "_cert"] = dict(changed_fraction=len(mp) / len(tr), support_fraction=het, n_tv_zero=int((tv_m < 1e-12).sum()), dose_tv=float(tv_m.mean()) if len(mp) else 0.0,
                                                          dose_tv_all=float(tv_m.sum() / len(tr)), dose_tv_final=float(tv_final.mean()) if len(mp) else 0.0, dose_tv_final_all=float(tv_final.sum() / len(tr)),
                                                          **(assert_valid_nominal(T, z, c, name) if kind == "zc" else {}))
    rows = []
    def score(name, P, extra=None):
        row = dict(seed=seed, isplit=isplit, m=args.m, arm=name, kl_ref=float(np.mean(np.sum(ref_hist * (np.log(ref_hist + 1e-9) - np.log(P + 1e-9)), 1))),
                   acc_mode=float((P.argmax(1) == z_ref).mean()), ent_spearman=float(spearmanr(ent(P), ent_ref).correlation),
                   resid_spearman=float(spearmanr(resid_share(P, z_ref), rs_ref).correlation), modal_mass_spearman=float(spearmanr(P[np.arange(len(te)), z_ref], ref_hist.max(1)).correlation))
        if extra: row.update(extra)
        rows.append(row); print(f"  s{seed} i{isplit} m{args.m} {name:10s} KL {row['kl_ref']:.4f} acc {row['acc_mode']:.3f} ent_rho {row['ent_spearman']:+.3f} resid_rho {row['resid_spearman']:+.3f} cmass_rho {row['modal_mass_spearman']:+.3f}", flush=True)
    best = None
    for e in (0.02, 0.05, 0.1, 0.2, 0.3, 0.4):
        m_, vl = train(X[tr], (1 - e) * np.eye(K)[z] + e / K, X[va], Pva, rng, args.steps)
        if best is None or vl < best[0]: best = (vl, e, m_)
    score("smooth", pmf(best[2], X[te]), {"param": best[1]})
    best = None
    for kap in (0.5, 1, 2, 4, 8):
        m_, vl = train(X[tr], (args.m * hist + kap * proto) / (args.m + kap), X[va], Pva, rng, args.steps)
        if best is None or vl < best[0]: best = (vl, kap, m_)
    score("shrunk", pmf(best[2], X[te]), {"param": best[1]})
    for name in ("hard", "proto", "zc", "cond", "soft", "soft_pmode", "soft_pzc"):
        m_, vl = train(X[tr], targets[name], X[va], Pva, rng, args.steps); score(name, pmf(m_, X[te]), targets.get(name + "_cert"))
    score("fidelity_zc", np.stack([rescale_to_c(proto_i, zi, ci) for proto_i, zi, ci in zip([hist_of(H0[np.ix_(tr, P_train)])[z == zz].mean(0) if (z == zz).any() else np.full(K, 1 / K) for zz in hist_of(H0[np.ix_(te, P_train)]).argmax(1)], hist_of(H0[np.ix_(te, P_train)]).argmax(1), hist_of(H0[np.ix_(te, P_train)]).max(1))]))
    score("fidelity_soft", hist_of(H0[np.ix_(te, P_train)]) + 1e-6)
    return rows

if __name__ == "__main__":
    rows = []
    for seed, isplit in itertools.product(range(args.seeds), range(args.item_splits)):
        rows += run(seed, isplit); pd.DataFrame(rows).to_json(f"{OUT}/runs.jsonl", orient="records", lines=True)
    df = pd.DataFrame(rows); cols = ["kl_ref", "acc_mode", "ent_spearman", "resid_spearman", "modal_mass_spearman"]
    g = df.groupby("arm")[cols].agg(["mean", "sem"]).reindex(["hard", "smooth", "proto", "zc", "cond", "shrunk", "soft", "soft_pmode", "soft_pzc", "fidelity_zc", "fidelity_soft"]).round(4)
    open(f"{OUT}/summary.md", "w").write(f"# probe_nominal — {args.panel}, m={args.m} training positions, {args.n_ref} reference positions\n\n```\n{g.to_string()}\n```\n"); print(g.to_string())
