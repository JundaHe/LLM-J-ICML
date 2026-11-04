"""Stage 13 S13-3 (PROTOCOL_STAGE13.md), part b — third turns: history-conditioned population model m3 (sap_ca.py base + per-language μ3 on the history features, fitted on
other user folds' third turns; user folds carried over from the first turn) vs m3 + a3ᵀ δ̂_u^(1) with the frozen first-turn deviations (no rescaling, selection or tuning),
on each eligible user's third turns of conversations not used as first-turn support. User bootstrap (primary) and user × conversation-prompt two-way (secondary)."""
import os, sys, json, collections, numpy as np, torch
HERE = os.path.dirname(os.path.abspath(__file__)); P2 = os.path.abspath(os.path.join(HERE, "..", "paper-2", "phase2")); sys.path.insert(0, P2); os.environ["CA_PANEL"] = "ca_pairs_third"
import data_panels
PAN0 = data_panels.load("ca_pairs_third"); Hz = np.load(f"{P2}/features/ca_third_hist/hist_Qwen2.5-7B-Instruct.npz", allow_pickle=True)  # own file; conversation_id is an object array; ci = {c: i for i, c in enumerate(Hz["conversation_id"])}
EVT0 = np.array([s.split("|")[0] for s in PAN0["item_ids"]]); OTH = np.array([s.split("|")[1] for s in PAN0["item_ids"]]); ch = {}
for e_, o_ in zip(EVT0, OTH): ch.setdefault(e_, set("abcd")).discard(o_)
CH = np.array([next(iter(ch[e_])) for e_ in EVT0]); yb = np.asarray(PAN0["yb"]); LB = np.where(yb == 1, CH, OTH); LA = np.where(yb == 1, OTH, CH); L_ = {x: i for i, x in enumerate("abcd")}
keep_rows = np.array([e_ in ci for e_ in EVT0]); assert keep_rows.all(), f"{(~keep_rows).sum()} third-turn pairs without history features"
cv = np.array([ci[e_] for e_ in EVT0]); out_dir = f"{P2}/features/ca_pairs_third"; os.makedirs(out_dir, exist_ok=True)
if not os.path.exists(f"{out_dir}/pairs_Qwen2.5-7B-Instruct.npz"):
    np.savez(f"{out_dir}/pairs_Qwen2.5-7B-Instruct.npz", E_A=Hz["E_R"][cv, [L_[x] for x in LA]], E_B=Hz["E_R"][cv, [L_[x] for x in LB]], E_P=Hz["E_P"][cv], item_ids=np.asarray(PAN0["item_ids"]).astype(str))
del Hz, PAN0
exec(open(f"{HERE}/sap_ca.py").read().split("recs = []; info = []")[0])   # population-model code of sap_ca.py on the third-turn panel (history features)
D1 = json.load(open(f"{HERE}/results/stage13_delta1.json")); assert D1["names"] == NAMES
rfold = np.array([D1["rfold"].get(r, -1) for r in raters])                  # first-turn user folds; users absent from the first-turn panel (-1) are training-only
from attr_feats import attrs
RAW3 = np.stack([attrs(str(b), str(p)) - attrs(str(a), str(p)) for a, b, p in zip(PAN["resp_A"], PAN["resp_B"], PAN["texts"])]); A1u = (RAW3 - np.array(D1["mean1"])) / np.array(D1["sd1"]); del RAW3   # third-turn differences in first-turn attribute units
An = A.numpy(); Yn = YB.numpy(); recs = []
for f in range(5):
    test_r = rfold == f; is_tr = ~test_r[R]; idx_tr = np.where(is_tr & ~va_item)[0]; idx_va = np.where(is_tr & va_item)[0]; idx_all = np.concatenate([idx_tr, idx_va])
    base, lam = fit_base(idx_tr, idx_va); mu = fit_mu(base, idx_all); MU = mu[torch.tensor(ulang)]; lg3 = (base + (MU[Rt] * A).sum(1)).numpy()
    for r in np.where(test_r)[0]:
        u = D1["users"].get(raters[r])
        if u is None or u["fold"] != f: continue
        js = np.where((R == r) & ~np.isin(EVT, u["support_conv"]))[0]
        if len(np.unique(EVT[js])) < 5: continue
        lt = lg3[js] + A1u[np.ix_(js, u["cols"])] @ np.array(u["delta"]); lp = lg3[js]; y = Yn[js]
        ll = lambda lg_: y * -np.logaddexp(0, -lg_) + (1 - y) * -np.logaddexp(0, lg_)
        recs.append({"fold": f, "rater": int(r), "n": int(len(js)), "acc_d": float(((lt > 0) == y).sum() - ((lp > 0) == y).sum()), "ll_d": float((ll(lt) - ll(lp)).sum()), "groups": [str(g) for g in Gp[js]],
                     "acc_rows": (((lt > 0) == y).astype(float) - ((lp > 0) == y).astype(float)).tolist(), "ll_rows": (ll(lt) - ll(lp)).tolist()})
    print(f"fold {f}: λ {lam}; {sum(1 for x in recs if x['fold'] == f)} users", flush=True)
def boot(key, sc_):
    d_ = np.array([x[key] for x in recs]); w = np.array([x["n"] for x in recs]); rng = np.random.RandomState(17); bs = [d_[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(recs), len(recs)) for _ in range(2000))]
    return [sc_ * d_.sum() / w.sum(), sc_ * np.percentile(bs, 2.5), sc_ * np.percentile(bs, 97.5), len(recs)]
def boot2(key, sc_, B=1000):
    dp = np.concatenate([x[key] for x in recs]); ui = np.concatenate([[i] * x["n"] for i, x in enumerate(recs)]); gi = np.unique(np.concatenate([x["groups"] for x in recs]), return_inverse=True)[1]
    rng = np.random.RandomState(17); bs = []
    for _ in range(B):
        w = np.bincount(rng.randint(0, len(recs), len(recs)), minlength=len(recs))[ui] * np.bincount(rng.randint(0, gi.max() + 1, gi.max() + 1), minlength=gi.max() + 1)[gi]; bs.append((w * dp).sum() / max(w.sum(), 1))
    return [sc_ * dp.mean(), sc_ * np.percentile(bs, 2.5), sc_ * np.percentile(bs, 97.5)]
out = {"acc": boot("acc_d", 100), "ll": boot("ll_d", 1), "acc_2way": boot2("acc_rows", 100), "ll_2way": boot2("ll_rows", 1)}
out["decision"] = {"transport_improves_prediction": bool(out["acc"][1] > 0 and out["ll"][1] > 0)}
json.dump(out, open(f"{HERE}/results/stage13_s3.json", "w"), indent=1); print(json.dumps(out), flush=True)
