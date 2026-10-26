"""PROTOCOL_STAGE1 estimand 4 (PRISM): how much of the 1–100 score is user-side? (a) variance components (users with ≥ 10 ratings): between-user variance of user means vs within-user variance;
(b) out-of-sample gain of a per-user offset fitted on k ∈ {5, 10, 20} of the user's ratings for predicting their held-out scores, over (i) the global mean, (ii) a per-model mean (a crude item-side predictor: the
response's model), (iii) per-model mean + user offset. 20 random splits; users with ≥ k + 5 ratings. MSE and R²."""
import pandas as pd, numpy as np, json, os
HERE = os.path.dirname(os.path.abspath(__file__)); u = pd.read_json(f"{HERE}/data/prism/utterances.jsonl", lines=True)[["user_id", "model_name", "score", "conversation_id", "interaction_id"]].dropna()
cnt = u.user_id.value_counts(); u10 = u[u.user_id.isin(cnt[cnt >= 10].index)]
g = u10.groupby("user_id").score; between = g.mean().var(); within = g.var().mean(); out = {"n_users_ge10": int(u10.user_id.nunique()), "n_ratings": int(len(u10)), "var_between_user_means": float(between), "mean_within_user_var": float(within), "share_between": float(between / (between + within))}
rng = np.random.RandomState(0); res = {}
for k in (5, 10, 20):
    us = cnt[cnt >= k + 5].index; m = {"global": [], "model": [], "model+user": [], "user": []}
    for rep in range(20):
        fit, test = [], []
        for uid, grp in u[u.user_id.isin(us)].groupby("user_id"):
            idx = rng.permutation(len(grp)); fit.append(grp.iloc[idx[:k]]); test.append(grp.iloc[idx[k:]])
        fit = pd.concat(fit); test = pd.concat(test); gm = fit.score.mean(); mm = fit.groupby("model_name").score.mean()
        pm = test.model_name.map(mm).fillna(gm).to_numpy(); off = (fit.score - fit.model_name.map(mm).fillna(gm)).groupby(fit.user_id).mean(); uo = test.user_id.map(off).fillna(0).to_numpy()
        um = fit.groupby("user_id").score.mean(); y = test.score.to_numpy()
        for name, pred in (("global", np.full(len(y), gm)), ("model", pm), ("model+user", pm + uo), ("user", test.user_id.map(um).to_numpy())): m[name].append(float(((y - pred) ** 2).mean()))
    var_y = float(u[u.user_id.isin(us)].score.var()); res[k] = {n: dict(mse=float(np.mean(v)), r2=1 - float(np.mean(v)) / var_y) for n, v in m.items()}; res[k]["n_users"] = int(len(us))
out["offset_prediction"] = res; json.dump(out, open(f"{HERE}/results/prism_rater_side.json", "w"), indent=1); print(json.dumps(out, indent=1))
