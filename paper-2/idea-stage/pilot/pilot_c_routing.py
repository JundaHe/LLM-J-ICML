"""
Pilot C — route to humans by matched-human GAIN, not by judge uncertainty (training-signal#3).
For every test item i and ordered rater pair (h = routed human, r = held-out reference, h != r):
    g_i(h,r) = |J_i - Y_ir| - |Y_ih - Y_ir|      (>0: a human would help relative to the judge)
A cross-fitted gain head predicts E_{h,r}[g_i] from judge-side features only; routing policies are compared on the
hybrid MAE vs the reference rater at fixed human budgets f, by consensus stratum (strata from the raters other than r).
Usage: python pilot_c_routing.py results/base_zeroshot [results/kl_soft_s0 ...]
"""
import sys, os, json, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import csje_eval as E, cm_data
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.model_selection import GroupKFold

def load_run(run):
    te = pd.read_csv(f"{run}/test_items.csv")
    d = pd.concat([cm_data.load("developer", 4000), cm_data.load("generated", 4000)]).reset_index(drop=True)
    d = te.merge(d, on=["hash", "msg_type"], how="left")
    return d, {c: np.load(f"{run}/P_{c}.npy") for c in ["what", "why"]}

def features(P, d):
    ent = E.entropy(P); lvl = P.argmax(1); ev = P @ np.arange(5)
    return np.column_stack([P, ent, lvl, ev, np.abs(ev - 2), d.msg_type.eq("generated").astype(float),
                            np.log1p(d.commit_message.astype(str).str.len()), np.log1p(d.git_diff_u3.astype(str).str.len())])

def evaluate(run, B=500, seed=0):
    d, Ps = load_run(run); out = {}
    rng = np.random.RandomState(seed)
    for crit in ["what", "why"]:
        P = Ps[crit]; H = cm_data.H(d, crit); n, m = H.shape
        J = np.clip(np.round(P @ np.arange(5)), 0, 4)          # judge point = rounded expected score
        X = features(P, d)
        # per-item mean gain over all ordered rater pairs, and per-pair arrays
        pairs = [(h, r) for h in range(m) for r in range(m) if h != r]
        G = np.stack([np.abs(J - H[:, r]) - np.abs(H[:, h] - H[:, r]) for h, r in pairs], 1)   # n x 30
        g_mean = G.mean(1)
        # strata from the raters other than r (per pair), reduced to the modal stratum across pairs for reporting
        st_full = E.strata(H)
        # cross-fitted gain head (regression on g_mean) and a contested-first head (classifier for Low stratum)
        pred_g = np.zeros(n); pred_low = np.zeros(n)
        groups = pd.factorize(d.hash)[0]
        for tr, va in GroupKFold(5).split(X, groups=groups):
            pred_g[va] = GradientBoostingRegressor(n_estimators=150, max_depth=2, learning_rate=0.05, random_state=seed).fit(X[tr], g_mean[tr]).predict(X[va])
            pred_low[va] = GradientBoostingClassifier(n_estimators=150, max_depth=2, learning_rate=0.05, random_state=seed).fit(X[tr], st_full[tr] == "Low").predict_proba(X[va])[:, 1]
        ent = E.entropy(P)
        policies = {"gain-head": pred_g, "entropy-first": ent, "predicted-Low-first": pred_low,
                    "random": rng.rand(n), "oracle-gain": g_mean}
        res = {"n": int(n), "auroc_gain_pos": {k: E.auroc(v, g_mean > 0) for k, v in policies.items()},
               "spearman_with_oracle": {k: float(pd.Series(v).corr(pd.Series(g_mean), method="spearman")) for k, v in policies.items()},
               "mae_judge_only": float(np.mean([np.abs(J - H[:, r]).mean() for r in range(m)])),
               "mae_human_only": float(np.mean([np.abs(H[:, h] - H[:, r]).mean() for h, r in pairs])), "budgets": {}}
        def hybrid_mae(route_mask):
            # hybrid prediction: human h where routed, judge elsewhere; averaged over all ordered pairs
            vals = []
            for k, (h, r) in enumerate(pairs):
                pred = np.where(route_mask, H[:, h], J); vals.append(np.abs(pred - H[:, r]))
            return np.mean(vals, 0)                    # per-item error averaged over pairs
        for f in [0.1, 0.2, 0.3, 0.5]:
            kf = int(round(f * n)); res["budgets"][f] = {}
            per_item = {}
            for k, score in policies.items():
                mask = np.zeros(n, bool); mask[np.argsort(-score)[:kf]] = True
                e = hybrid_mae(mask); per_item[k] = e
                res["budgets"][f][k] = {"mae": float(e.mean()), **{s: float(e[st_full == s].mean()) for s in ["High", "Partial", "Low"]}}
            # paired item-bootstrap of (entropy-first − gain-head) at this budget
            diff = per_item["entropy-first"] - per_item["gain-head"]
            uniq = np.unique(groups); boots = []
            for _ in range(B):
                g = rng.choice(uniq, len(uniq), replace=True); idx = np.concatenate([np.where(groups == x)[0] for x in g]); boots.append(diff[idx].mean())
            res["budgets"][f]["gain_vs_entropy_mae_reduction"] = [float(diff.mean()), float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))]
        out[crit] = res
        print(f"[{os.path.basename(run)} {crit}] judge-only MAE={res['mae_judge_only']:.3f} human-only MAE={res['mae_human_only']:.3f} | AUROC(g>0): " +
              ", ".join(f"{k}={v:.3f}" for k, v in res["auroc_gain_pos"].items()))
        for f in [0.2, 0.5]:
            b = res["budgets"][f]
            print(f"   budget {f:.0%}: " + " | ".join(f"{k} {b[k]['mae']:.3f} (H {b[k]['High']:.2f}/P {b[k]['Partial']:.2f}/L {b[k]['Low']:.2f})" for k in policies) +
                  f" || gain−entropy ΔMAE={b['gain_vs_entropy_mae_reduction'][0]:+.3f} CI[{b['gain_vs_entropy_mae_reduction'][1]:+.3f},{b['gain_vs_entropy_mae_reduction'][2]:+.3f}]")
    json.dump(out, open(f"{run}/pilot_c_routing.json", "w"), indent=1, default=float)

if __name__ == "__main__":
    for run in sys.argv[1:]:
        evaluate(run)
