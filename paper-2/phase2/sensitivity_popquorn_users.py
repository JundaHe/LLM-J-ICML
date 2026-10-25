"""
Rater-aware sensitivity for the POPQUORN LoRA block (Codex round 16).
popquorn_off8 assigns each item's ratings to 8 positions by a seeded permutation and drops the user ids, so the
position folds hold out a rating, not a person; the same annotators recur across items. This script
(1) reconstructs the user id behind every (item, position) by replaying the loader's RNG and checks it against H,
(2) reports how many test-evaluator users also appear among the training targets, and
(3) recomputes the RAW contrasts with a pigeonhole (item × user) bootstrap: items and users are resampled
    independently and each test row is weighted by (#draws of its item) × (#draws of its evaluator user),
    crossed with the seed-cluster resampling of analysis_block_popquorn.py.
Usage: ~/miniconda3/envs/skill1/bin/python sensitivity_popquorn_users.py [--B 10000]
"""
import sys, os, json, argparse, itertools, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); import data_panels
ap = argparse.ArgumentParser(); ap.add_argument("--B", type=int, default=10000); args = ap.parse_args()
PAN = data_panels.load("popquorn_off8"); H = PAN["H"]; K = PAN["K"]; LV = np.arange(K); M = 8
# ---- (1) replay the loader to recover user ids per (item, position)
d = pd.read_csv(f"{data_panels.POPQ}/offensiveness/raw_data.csv").dropna(subset=["offensiveness"]); rng = np.random.RandomState(0)
g = d.groupby("instance_id"); keep = [iid for iid, grp in g if len(grp) >= M]
assert list(keep) == list(PAN["item_ids"])
U = []
for i, iid in enumerate(keep):
    grp = g.get_group(iid); p = rng.permutation(len(grp))[:M]
    assert (grp.offensiveness.to_numpy(int)[p] - 1 == H[i]).all(), f"replay mismatch at item {i}"
    U.append(grp.user_id.to_numpy()[p])
U = np.array(U)
print(f"replayed user ids for {len(keep)} items × {M} positions; {len(np.unique(U))} distinct users; replay matches H exactly")
ROOT = f"{HERE}/results/lora/popquorn_off8"; ROSTER = ["chen", "perm", "perm_mode"]; SEEDS = [2000, 2001, 2002]; FOLDS = [0, 1, 2]
def path(s, f, a): return f"{ROOT}/s0{'' if s == 2000 else f'_seed{s}'}/f{f}/{a}"
def rps(P, y): c = np.cumsum(P, 1); st = (LV[None] >= y[:, None]).astype(float); return ((c - st) ** 2).sum(1) / (K - 1)
IT = pd.read_csv(f"{path(2000, 0, 'chen')}/items_test.csv").row.to_numpy()
TR = np.setdiff1d(np.arange(len(H)), np.concatenate([IT, pd.read_csv(f"{path(2000, 0, 'chen')}/items_calib.csv").row.to_numpy()]))
# ---- (2) overlap of evaluator users with training-target users
for f in FOLDS:
    ev = set(U[IT, f]); tgt = set(U[np.ix_(TR, [p for p in range(M) if p != f])].ravel())
    print(f"fold {f}: {len(ev)} distinct test-evaluator users, {len(ev & tgt)} of them ({len(ev & tgt) / len(ev):.0%}) also rate training targets")
# ---- (3) raw losses per cell
L = {}
for s, f in itertools.product(SEEDS, FOLDS):
    y = H[IT, f]
    for a in ROSTER:
        assert (pd.read_csv(f"{path(s, f, a)}/items_test.csv").row.to_numpy() == IT).all()
        L[(s, f, a)] = rps(np.load(f"{path(s, f, a)}/P_test.npy"), y)
users = np.unique(U[IT][:, FOLDS]); uidx = {u: k for k, u in enumerate(users)}; UI = np.array([[uidx[U[i, f]] for f in FOLDS] for i in IT])
CON = [("perm − chen", "perm", "chen"), ("perm_mode − chen", "perm_mode", "chen"), ("perm_mode − perm", "perm_mode", "perm")]
def est(seeds, wi=None, wu=None):
    out = {}
    for n, a, b in CON:
        vals = []
        for s in seeds:
            fv = []
            for f in FOLDS:
                dlt = L[(s, f, a)] - L[(s, f, b)]
                w = np.ones(len(IT)) if wi is None else wi * wu[UI[:, f]]
                fv.append(np.sum(w * dlt) / np.sum(w) if w.sum() > 0 else np.nan)
            vals.append(np.nanmean(fv))
        out[n] = float(np.mean(vals))
    return out
pt = est(SEEDS); r = np.random.RandomState(1); boot_item = {n: [] for n, _, _ in CON}; boot_pw = {n: [] for n, _, _ in CON}
for _ in range(args.B):
    sd = r.choice(SEEDS, 3, replace=True); wi = np.bincount(r.randint(0, len(IT), len(IT)), minlength=len(IT)).astype(float)
    wu = np.bincount(r.randint(0, len(users), len(users)), minlength=len(users)).astype(float)
    e1 = est(sd, wi, np.ones(len(users))); e2 = est(sd, wi, wu)
    for n in e1: boot_item[n].append(e1[n]); boot_pw[n].append(e2[n])
rows = []
for n, _, _ in CON:
    a = np.percentile(boot_item[n], [2.5, 97.5]); b = np.percentile(boot_pw[n], [2.5, 97.5]); c = np.percentile(boot_pw[n], [5, 95])
    rows.append(dict(contrast=n, est=pt[n], item_lo=a[0], item_hi=a[1], pigeonhole_lo=b[0], pigeonhole_hi=b[1], pigeonhole_lo90=c[0], pigeonhole_hi90=c[1]))
    print(f"  {n:18s} raw {pt[n]:+.4f}  item×seed [{a[0]:+.4f}, {a[1]:+.4f}]  item×user×seed (pigeonhole) [{b[0]:+.4f}, {b[1]:+.4f}]  90% [{c[0]:+.4f}, {c[1]:+.4f}]")
print(f"  n_test_items={len(IT)}  n_evaluator_users={len(users)}  B={args.B}  (raw estimand only; calibration maps not refitted)")
json.dump(dict(B=args.B, n_users=int(len(users)), rows=rows), open(f"{ROOT}/sensitivity_popquorn_users.json", "w"), indent=1)
