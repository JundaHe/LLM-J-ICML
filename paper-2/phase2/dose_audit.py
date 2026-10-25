"""
Offline dose / support certificates for the permutation interventions (Codex round 9 §A), independent of training.
Mirrors probe_mean2's split logic exactly (grouped 60/10/30 item split by isplit; rater split by rsplit; cells (mode) for pmode and (mode, floor(mean/tau)) for pmm;
randomised maximum matching on histogram classes with the probe's RNG seed) and reports per panel (mean over the 18 = 3 × 3 × 2 configs used by gxr_check; the
probe_mean2 configs use the same first 3 seeds):
  support   = fraction of training items in cells containing >= 2 histogram classes (an upper bound on what any bijection can change)
  changed   = realised fraction changed by the maximum-cardinality matching
  tv_chg    = mean TV between recipient and donor histograms over changed items
  tv_all    = mean TV over ALL training items (unchanged = 0)
  tv_zero   = number of matched pairs with identical histograms (must be 0)
  shift     = mean / max |mu_recipient - mu_donor| (pmm: <= tau; pmode: free)
  pmmx_tv_final / pmmx_changed_final = TV and changed fraction AFTER the exact mode-and-mean KL projection of the donor (post-projection dose)
Usage: python dose_audit.py [--panels ...] [--seeds 3]
"""
import argparse, os, sys, math, json, itertools, numpy as np, pandas as pd
from paths import LLMJ
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, LLMJ + "/paper-2/idea-stage/pilot")
from support_audit import z_label, random_max_matching
import data_panels, targets as tgt
ap = argparse.ArgumentParser(); ap.add_argument("--panels", default="bw,dices,summeval_coherence8,summeval_relevance8,scalabrino,hs2_help5,popquorn_off8,popquorn_pol5,dices990,csc6,emobank_reader_v5")
ap.add_argument("--seeds", type=int, default=3); ap.add_argument("--tau", type=float, default=0.1); args = ap.parse_args()
NEVAL = {"commit_why": 2, "commit_what": 2, "bw": 24, "dices": 24, "summeval_coherence8": 2, "summeval_relevance8": 2, "scalabrino": 3, "hs2_help5": 2, "popquorn_off8": 2, "dices990": 20, "popquorn_pol5": 1, "csc6": 1, "emobank_reader_v5": 1}
rows = []
for panel in args.panels.split(","):
    PAN = data_panels.load(panel); H0 = PAN["H"]; N, M = H0.shape; K = PAN["K"]; n_eval = NEVAL[panel]
    for seed, isplit, rsplit in itertools.product(range(args.seeds), range(3), range(2)):
        rng = np.random.RandomState(seed * 1000 + isplit * 10 + rsplit)
        G = PAN.get("groups", PAN["item_ids"]); ug = np.unique(G); ug = ug[np.random.RandomState(isplit).permutation(len(ug))]
        g_tr = set(ug[: int(.6 * len(ug))]); tr = np.array([i for i in range(N) if G[i] in g_tr])
        rp = np.random.RandomState(100 + rsplit).permutation(M); R_train = np.sort(rp[n_eval:])
        Htr = H0[np.ix_(tr, R_train)]; z = np.array([z_label(r) for r in Htr]); mu = Htr.mean(1); hist = np.stack([np.bincount(r, minlength=K) / len(R_train) for r in Htr])
        hk = [tuple(np.bincount(r, minlength=K)) for r in Htr]
        for kind in ("mode", "mm"):
            cells = {}
            for i in range(len(tr)): cells.setdefault((int(z[i]), int(math.floor(mu[i] / args.tau)) if kind == "mm" else 0), []).append(i)
            support = sum(len(it) for it in cells.values() if len({hk[i] for i in it}) >= 2) / len(tr)
            mp = {}
            for it in cells.values(): mp.update(random_max_matching(it, [hk[i] for i in it], rng))
            tv = np.array([0.5 * np.abs(hist[a] - hist[b]).sum() for a, b in mp.items()]); sh = np.array([abs(mu[a] - mu[b]) for a, b in mp.items()])
            r = dict(panel=panel, arm="soft_pmode" if kind == "mode" else "soft_pmm", seed=seed, isplit=isplit, rsplit=rsplit, n_train=len(tr), n_raters=len(R_train), support=support, changed=len(mp) / len(tr),
                     tv_chg=float(tv.mean()) if len(tv) else 0.0, tv_all=float(tv.sum() / len(tr)), tv_zero=int((tv < 1e-12).sum()), shift_mean=float(sh.mean()) if len(sh) else 0.0, shift_max=float(sh.max()) if len(sh) else 0.0)
            rows.append(r)
            if kind == "mm":   # pmmx: exact projection of the donor onto the recipient's mode and mean
                tgt.reset_status(); tvx = []
                for a, b in mp.items():
                    q = tgt.ordinal_mode_mean(hist[b], int(z[a]), mu[a], feasible=hist[a]); tvx.append(0.5 * np.abs(q - hist[a]).sum())
                tvx = np.array(tvx); rx = dict(r); rx.update(arm="soft_pmmx", tv_chg=float(tvx[tvx > 1e-9].mean()) if (tvx > 1e-9).any() else 0.0, tv_all=float(tvx.sum() / len(tr)), changed=float((tvx > 1e-9).sum() / len(tr)),
                                              tv_zero=int((tvx <= 1e-9).sum()), shift_mean=0.0, shift_max=0.0, **{f"status_{k}": v for k, v in tgt.STATUS.items()})
                rows.append(rx)
    print(panel, "done", flush=True)
df = pd.DataFrame(rows)
if os.path.exists(f"{HERE}/results/dose_audit.jsonl") and args.panels != ap.get_default("panels"):
    old = pd.read_json(f"{HERE}/results/dose_audit.jsonl", lines=True); df = pd.concat([old[~old.panel.isin(df.panel.unique())], df], ignore_index=True)   # merge a subset run into the existing audit
df.to_json(f"{HERE}/results/dose_audit.jsonl", orient="records", lines=True)
agg = df.groupby(["panel", "arm"]).agg(n_train=("n_train", "first"), n_raters=("n_raters", "first"), support=("support", "mean"), changed=("changed", "mean"), tv_chg=("tv_chg", "mean"), tv_all=("tv_all", "mean"),
                                        tv_zero=("tv_zero", "sum"), shift_mean=("shift_mean", "mean"), shift_max=("shift_max", "max")).round(3)
print(agg.to_string()); agg.to_csv(f"{HERE}/results/dose_audit_summary.csv")
md = ["| panel | arm | n_train | train raters | support (het. cells) | changed | TV (changed) | TV (all items) | zero-TV pairs | mean shift mean / max |", "|---|---|---|---|---|---|---|---|---|---|"]
for (p, a), r in agg.iterrows(): md.append(f"| {p} | {a} | {int(r.n_train)} | {int(r.n_raters)} | {r.support:.3f} | {r.changed:.3f} | {r.tv_chg:.3f} | {r.tv_all:.3f} | {int(r.tv_zero)} | {r.shift_mean:.2f} / {r.shift_max:.2f} |")
open(f"{HERE}/results/dose_audit_table.md", "w").write("\n".join(md) + "\n")
