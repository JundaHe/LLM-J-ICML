"""
pools — identity-preserving loaders for paper 3 (PROTOCOL_CALIBRATION.md). Each loader returns
  items     : list of item ids in the SAME order as the paper-2 panel loader (so paper-2/phase2/features/<panel>/*.npz rows align), plus `panel` (the paper-2 panel key) and K
  ratings   : DataFrame (item, rater, y) with item = row index into `items`, y in 0..K-1, one row per rating (sparse panels allowed)
  raters    : DataFrame indexed by rater id with the metadata columns available (may be empty); column `persistent` says whether the id is a real person (vs an anonymous position)
Panels: dices (350 × 104 raters; gender/race/age/education), dices990 (990 × 172; + locale), popquorn_off / popquorn_pol (user_id; gender/race/age/education/occupation),
        summeval (1,600; experts 0–2 persistent, crowd positions anonymous; group ∈ {expert, crowd}), bw (100 × 121; group column of oracle.csv), mlcq (26 reviewers; no features),
        dorn_<lang> (sparse; experience column 1 of experience.csv assumed = years of programming, UNVERIFIED).
"""
import os, sys, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "..")); P2 = os.path.join(ROOT, "paper-2", "phase2"); sys.path.insert(0, P2)
import data_panels

def _pack(panel, items, K, ratings, raters, texts=None):
    ratings = ratings.astype({"item": int, "rater": str, "y": int}); assert ratings.y.min() >= 0 and ratings.y.max() <= K - 1
    raters = raters.copy(); raters.index = raters.index.astype(str)
    return dict(panel=panel, items=list(items), K=K, ratings=ratings.reset_index(drop=True), raters=raters, texts=texts)

def load_dices(quality=True):
    d = pd.read_csv(f"{P2}/data/dices/dices350.csv")
    if quality: d = d[~d.rater_id.astype(str).isin(data_panels.DICES_REMOVED)]
    items = sorted(d.item_id.unique()); idx = {it: i for i, it in enumerate(items)}; lv = {"No": 0, "Unsure": 1, "Yes": 2}
    r = pd.DataFrame({"item": d.item_id.map(idx), "rater": d.rater_id.astype(str), "y": d.Q_overall.map(lv)})
    meta = d.drop_duplicates("rater_id").set_index(d.drop_duplicates("rater_id").rater_id.astype(str))[["rater_gender", "rater_race", "rater_age", "rater_education"]]; meta["persistent"] = True
    return _pack("dices", items, 3, r, meta)

def load_dices990():
    d = pd.read_csv(f"{P2}/data/dices_repo/990/diverse_safety_adversarial_dialog_990.csv"); items = sorted(d.item_id.unique()); idx = {it: i for i, it in enumerate(items)}; lv = {"No": 0, "Unsure": 1, "Yes": 2}
    r = pd.DataFrame({"item": d.item_id.map(idx), "rater": d.rater_id.astype(str), "y": d.Q_overall.map(lv)})
    u = d.drop_duplicates("rater_id"); meta = u.set_index(u.rater_id.astype(str))[["rater_gender", "rater_race", "rater_age", "rater_education", "rater_locale"]]; meta["persistent"] = True
    return _pack("dices990", items, 3, r, meta)

def _load_popquorn(attr, m):
    sub = "offensiveness" if attr == "offensiveness" else "politeness_rating"
    d = pd.read_csv(f"{P2}/data/popquorn/dataset/{sub}/raw_data.csv").dropna(subset=[attr]); g = d.groupby("instance_id"); keep = [iid for iid, grp in g if len(grp) >= m]   # same item set/order as data_panels
    idx = {it: i for i, it in enumerate(keep)}; dd = d[d.instance_id.isin(idx)]
    r = pd.DataFrame({"item": dd.instance_id.map(idx), "rater": dd.user_id.astype(str), "y": dd[attr].astype(int) - 1})
    u = dd.drop_duplicates("user_id"); meta = u.set_index(u.user_id.astype(str))[["gender", "race", "age", "education", "occupation"]]; meta["persistent"] = True
    return _pack(f"popquorn_{'off8' if attr == 'offensiveness' else 'pol5'}", keep, 5, r, meta)
def load_popquorn_off(): return _load_popquorn("offensiveness", 8)
def load_popquorn_pol(): return _load_popquorn("politeness", 5)

def load_summeval(dim="coherence"):
    PAN = data_panels.load(f"summeval_{dim}8"); H = PAN["H"]; n, m = H.shape
    rows = [(i, ("expert%d" % j) if j < 3 else ("turkpos%d" % j), int(H[i, j])) for i in range(n) for j in range(m)]
    r = pd.DataFrame(rows, columns=["item", "rater", "y"]); ids = [f"expert{j}" for j in range(3)] + [f"turkpos{j}" for j in range(3, 8)]
    meta = pd.DataFrame({"group": ["expert"] * 3 + ["crowd"] * 5, "persistent": [True] * 3 + [False] * 5}, index=ids)
    return _pack(f"summeval_{dim}8", list(PAN["item_ids"]), 5, r, meta, texts=PAN["texts"])

def load_bw():
    bw = pd.read_csv(f"{ROOT}/code/code_readability/data/buse_weimer/oracle.csv", header=None); rid = bw.iloc[:, 0].astype(str).to_numpy(); grp = bw.iloc[:, 1].astype(str).to_numpy(); S = bw.iloc[:, 2:].to_numpy(int) - 1
    rows = [(i, rid[j], int(S[j, i])) for j in range(S.shape[0]) for i in range(S.shape[1])]
    meta = pd.DataFrame({"group": grp, "persistent": True}, index=rid)
    return _pack("bw", list(range(1, S.shape[1] + 1)), 5, pd.DataFrame(rows, columns=["item", "rater", "y"]), meta)

def load_mlcq(m=3):
    d = pd.read_csv(f"{P2}/data/mlcq/MLCQCodeSmellSamples.csv", sep=";"); lv = {"none": 0, "minor": 1, "major": 2, "critical": 3}
    g = d.groupby(["sample_id", "smell"]); keep = [k for k, grp in g if len(grp) >= m]; idx = {k: i for i, k in enumerate(keep)}
    dd = d[[(s, sm) in idx for s, sm in zip(d.sample_id, d.smell)]]
    r = pd.DataFrame({"item": [idx[(s, sm)] for s, sm in zip(dd.sample_id, dd.smell)], "rater": dd.reviewer_id.astype(str), "y": dd.severity.map(lv)})
    meta = pd.DataFrame({"persistent": True}, index=sorted(dd.reviewer_id.astype(str).unique()))
    return _pack("mlcq3", [f"{s}_{sm.replace(' ', '-')}" for s, sm in keep], 4, r, meta)

def load_dorn(lang="java"):
    D = f"{ROOT}/code/code_readability/data/dorn"; S = pd.read_csv(f"{D}/scores/{lang}.csv", header=None); rid = S.iloc[:, 0].astype(int); S = S.iloc[:, 1:]
    snips = sorted(int(f.split(".")[0]) for f in os.listdir(f"{D}/snippets/{lang}")); rows = []
    for j in range(S.shape[1]):
        col = S.iloc[:, j]; ok = col.notna()
        rows += [(j, str(int(rid[k])), int(col[k]) - 1) for k in np.where(ok)[0]]
    e = pd.read_csv(f"{D}/experience.csv", header=None); e.index = e[0].astype(int).astype(str)
    meta = pd.DataFrame({"years_programming_UNVERIFIED": e[1]}, index=e.index); meta["persistent"] = True
    return _pack(f"dorn_{lang}", [f"{lang}_{s}" for s in snips], 5, pd.DataFrame(rows, columns=["item", "rater", "y"]), meta)

LOADERS = {"dices": load_dices, "dices990": load_dices990, "popquorn_off8": load_popquorn_off, "popquorn_pol5": load_popquorn_pol, "summeval_coherence8": load_summeval, "bw": load_bw, "mlcq3": load_mlcq,
           "dorn_java": lambda: load_dorn("java"), "dorn_python": lambda: load_dorn("python"), "dorn_cuda": lambda: load_dorn("cuda")}

def pools_for(P, var, min_group=10, seed=0):
    """pool A = largest group of `var`; pool B = each other group with ≥ min_group raters; var == 'random' → two random halves of the persistent raters"""
    R = P["raters"]; pers = R[R.persistent.astype(bool)]
    if var == "random":
        rng = np.random.RandomState(seed); ids = np.array(sorted(pers.index)); rng.shuffle(ids); h = len(ids) // 2; return {"A": set(ids[:h]), "B_random": set(ids[h:])}
    groups = pers[var].dropna().astype(str); counts = groups.value_counts(); counts = counts[counts >= min_group]
    if len(counts) < 2: return {}
    A = counts.index[0]; out = {"A": set(groups[groups == A].index)}
    for g in counts.index[1:]: out[f"B_{g}"] = set(groups[groups == g].index)
    return out

if __name__ == "__main__":
    for k, f in LOADERS.items():
        P = f(); r = P["ratings"]; pers = P["raters"].persistent.astype(bool).sum()
        print(f"{k:20s} items {len(P['items']):5d} ratings {len(r):7d} raters {r.rater.nunique():5d} (persistent {pers}) K={P['K']} meta={[c for c in P['raters'].columns if c != 'persistent']}")
