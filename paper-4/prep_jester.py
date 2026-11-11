"""Label-blind preparation of Jester dataset 2 (HF ports): integrity check of the joke-text ↔ rating mapping, then compact files for the llmj venv (no parquet reader there)."""
import sys, json, hashlib, numpy as np, pandas as pd
RAW, OUT = sys.argv[1], sys.argv[2]
r = pd.read_parquet(f"{RAW}/hf_rating/jester_rating.parquet"); t = pd.read_parquet(f"{RAW}/hf_texts/train.parquet")
by = {i: np.sort(g.rating.to_numpy().round(3)) for i, g in r.groupby("item_id")}
tj = {int(j.split("_")[1]): np.sort(np.asarray(x, float).round(3)) for j, x in zip(t.jokeId, t.ratings)}
print("text joke ids", min(tj), max(tj), len(tj), "| rating item ids", min(by), max(by), len(by))
m = {}
for j, x in tj.items():
    c = [i for i, y in by.items() if len(y) == len(x) and np.array_equal(y, x)]
    m[j] = c
amb = {j: c for j, c in m.items() if len(c) != 1}; print("text jokes with a unique rating-set match:", sum(len(c) == 1 for c in m.values()), "/", len(m), "| non-unique:", amb)
ident = [j for j, c in m.items() if c == [j]]; off = sorted({c[0] - j for j, c in m.items() if len(c) == 1}); print("matches with item_id == joke index:", len(ident), "| offsets seen:", off[:10])
if not amb:
    it = {c[0]: t.jokeText[t.jokeId == f"joke_{j}"].iloc[0] for j, c in m.items()}
    assert len(it) == r.item_id.nunique()
    with open(f"{OUT}/jokes.jsonl", "w") as f:
        for i in sorted(it): f.write(json.dumps({"item_id": int(i), "text": it[i]}) + "\n")
    np.savez_compressed(f"{OUT}/ratings.npz", user=r.user_id.to_numpy(np.int32), item=r.item_id.to_numpy(np.int16), rating=r.rating.to_numpy(np.float32))
    L = np.array([len(x) for x in it.values()]); print("joke chars min/med/max", L.min(), int(np.median(L)), L.max(), "| empty", int((L == 0).sum()), "| duplicate texts", len(it) - len(set(it.values())))
    n_u = r.groupby("user_id").size(); print("users with >=120 ratings", int((n_u >= 120).sum()), ">=130", int((n_u >= 130).sum()), "== all", int((n_u == r.item_id.nunique()).sum()), "| rating range", float(r.rating.min()), float(r.rating.max()))
    print("sha256 ratings parquet", hashlib.sha256(open(f"{RAW}/hf_rating/jester_rating.parquet", "rb").read()).hexdigest()[:16], "texts parquet", hashlib.sha256(open(f"{RAW}/hf_texts/train.parquet", "rb").read()).hexdigest()[:16])
