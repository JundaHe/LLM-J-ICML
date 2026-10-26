"""SHRINKAGE_PROTOCOL Amendment 5: user-held-out heads on POPQUORN (real user ids). Usage: python user_heldout_heads.py --panel popquorn_off8 [--user_splits 5 --item_splits 3]"""
import os, sys, math, argparse, itertools, json, time
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"): os.environ.setdefault(_v, "3")
import numpy as np, pandas as pd, torch, torch.nn as nn
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "..", "paper-3"))
import pools, data_panels, targets as tgt
from fr_lib import Panel, folds_for
from support_audit import z_label, random_max_matching
ap = argparse.ArgumentParser(); ap.add_argument("--panel", default="popquorn_off8"); ap.add_argument("--user_splits", type=int, default=5); ap.add_argument("--item_splits", type=int, default=3); ap.add_argument("--k", type=int, default=4); ap.add_argument("--steps", type=int, default=1500); args = ap.parse_args()
torch.set_num_threads(int(os.environ["OMP_NUM_THREADS"])); PP = pools.LOADERS[args.panel](); R = PP["ratings"]; K = PP["K"]; LV = np.arange(K, dtype=float); N = len(PP["items"])
PAN = data_panels.load(args.panel); F = np.load(f"{HERE}/features/{args.panel}/{PAN['model'].split('/')[-1]}.npz", allow_pickle=True); E = F["E_last"].astype(np.float32); G = np.asarray(PAN["groups"]); P = Panel(K, False)
users = np.array(sorted(R.rater.unique())); OUT = f"{HERE}/results/user_heldout/{args.panel}"; os.makedirs(OUT, exist_ok=True)
def rps(Pm, y): cdf = np.cumsum(Pm, 1); return ((cdf - (LV[None, :] >= y[:, None])) ** 2).sum(1) / (K - 1)
class MLP(nn.Module):
    def __init__(s, d): super().__init__(); s.f = nn.Sequential(nn.Linear(d, 128), nn.GELU(), nn.Linear(128, K))
    def forward(s, x): return s.f(x)
def train(Xtr, Ptr, Xva, yva, seed):
    torch.manual_seed(seed); rng = np.random.RandomState(seed); m = MLP(Xtr.shape[1]); opt = torch.optim.Adam(m.parameters(), 1e-3, weight_decay=1e-4)
    Xt, Pt, Xv, yv = torch.tensor(Xtr), torch.tensor(Ptr, dtype=torch.float32), torch.tensor(Xva), torch.tensor(yva); best = (1e9, None); pat = 0
    for st in range(args.steps):
        idx = rng.randint(len(Xtr), size=min(256, len(Xtr))); loss = -(Pt[idx] * torch.log_softmax(m(Xt[idx]), -1)).sum(1).mean(); opt.zero_grad(); loss.backward(); opt.step()
        if st % 50 == 49:
            with torch.no_grad(): vl = nn.functional.cross_entropy(m(Xv), yv).item()
            if vl < best[0] - 1e-4: best = (vl, {k: v.clone() for k, v in m.state_dict().items()}); pat = 0
            else:
                pat += 1
                if pat >= 6: break
    m.load_state_dict(best[1]); return m
rows = []; t0 = time.time()
for us, isp in itertools.product(range(args.user_splits), range(args.item_splits)):
    u = users[np.random.RandomState(100 + us).permutation(len(users))]; U_ev = set(u[: int(.3 * len(u))]); Rtr = R[~R.rater.isin(U_ev)]; Rev = R[R.rater.isin(U_ev)]
    ug = np.unique(G); ug = ug[np.random.RandomState(isp).permutation(len(ug))]; g_tr, g_va = set(ug[: int(.6 * len(ug))]), set(ug[int(.6 * len(ug)): int(.7 * len(ug))])
    part = np.array(["tr" if G[i] in g_tr else "va" if G[i] in g_va else "te" for i in range(N)])
    gtr = Rtr.groupby("item").y.apply(lambda s: s.to_numpy()); tr = np.array([i for i in np.where(part == "tr")[0] if i in gtr.index and len(gtr[i]) >= 3])
    te_r = Rev[Rev.item.isin(np.where(part == "te")[0])]; va_r = Rtr[Rtr.item.isin(np.where(part == "va")[0])]
    if len(te_r) < 50: continue
    mu_e = E[tr].mean(0); U_, S_, Vt = np.linalg.svd(E[tr] - mu_e, full_matrices=False); dd = min(64, len(tr) // 4); W = Vt[:dd].T / (S_[:dd] / math.sqrt(len(tr)) + 1e-6); X = ((E - mu_e) @ W).astype(np.float32)
    Hl = [gtr[i] for i in tr]; h = np.stack([np.bincount(r, minlength=K) / len(r) for r in Hl]); z = np.array([z_label(r) for r in Hl]); mu = np.array([r.mean() for r in Hl])
    T = {"soft": h, "hard": np.eye(K)[z]}
    hcls = [tuple(np.bincount(r, minlength=K)) for r in Hl]; rng = np.random.RandomState(7 + us * 10 + isp)
    for kind in ("pmode", "pmmx"):
        cells = {}
        for j in range(len(tr)): cells.setdefault((int(z[j]), int(math.floor(mu[j] / 0.1)) if kind == "pmmx" else 0), []).append(j)
        mp = {}
        for items in cells.values(): mp.update(random_max_matching(items, [hcls[j] for j in items], rng))
        Tk = h.copy()
        for a, b in mp.items(): Tk[a] = tgt.ordinal_mode_mean(h[b], int(z[a]), mu[a]) if kind == "pmmx" else h[b]
        T[kind] = Tk; rows.append(dict(user_split=us, isplit=isp, arm=kind + "_changed", rps=len(mp) / len(tr)))
    # fixed budget: 1 rating on every training item vs k ratings on 1/k of the items (from training users only)
    brng = np.random.RandomState(50 + us * 10 + isp); one = np.stack([np.eye(K)[brng.choice(r)] for r in Hl])
    sub = brng.permutation(len(tr))[: len(tr) // args.k]; sub = np.array([j for j in sub if len(Hl[j]) >= args.k]); kk = np.stack([np.bincount(brng.choice(Hl[j], args.k, replace=False), minlength=K) / args.k for j in sub])
    yva = np.array([(i, y) for i, y in zip(va_r.item, va_r.y)]); Xva = X[yva[:, 0]]; yv = yva[:, 1]
    def ev(name, m): Pm = torch.softmax(m(torch.tensor(X[te_r.item.to_numpy()])), -1).detach().numpy(); rows.append(dict(user_split=us, isplit=isp, arm=name, rps=float(rps(Pm, te_r.y.to_numpy()).mean())))
    for name, Tg in T.items(): ev(name, train(X[tr], Tg, Xva, yv, 1000 + us * 10 + isp))
    ev("budget_1xall", train(X[tr], one, Xva, yv, 2000 + us * 10 + isp)); ev(f"budget_{args.k}x1/{args.k}", train(X[tr[sub]], kk, Xva, yv, 3000 + us * 10 + isp))
    print(f"user split {us} item split {isp}: {len(tr)} train items, {len(te_r)} held-out-user test ratings [{time.time()-t0:.0f}s]", flush=True)
df = pd.DataFrame(rows); df.to_json(f"{OUT}/runs.jsonl", orient="records", lines=True)
piv = df[~df.arm.str.endswith("_changed")].pivot_table(index=["user_split", "isplit"], columns="arm", values="rps"); d = piv.sub(piv["soft"], axis=0)
txt = f"# user-held-out heads — {args.panel} ({len(piv)} configs; evaluators never in any target)\n\n```\n" + pd.DataFrame({"rps": piv.mean(), "vs_soft": d.mean(), "vs_soft_sem": d.sem()}).round(5).to_string() + "\n\nbudget: " + f"{args.k}x(1/{args.k}) − 1xall = {(piv[f'budget_{args.k}x1/{args.k}'] - piv['budget_1xall']).mean():+.5f} ± {(piv[f'budget_{args.k}x1/{args.k}'] - piv['budget_1xall']).sem():.5f}\nchanged fractions: " + str(df[df.arm.str.endswith('_changed')].groupby('arm').rps.mean().round(3).to_dict()) + "\n```\n"
open(f"{OUT}/summary.md", "w").write(txt); print(txt)
