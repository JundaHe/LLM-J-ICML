"""Rater-identity checks for the four panels: persistent IDs across items, demographic consistency within ID (DICES, PRISM, Community Alignment), and, for
MultiPref (no demographics), behavioural persistence — early-vs-late (by timestamp) correlation across evaluators of each evaluator's tie rate and extreme
rate, against 20 shuffles of the evaluator labels. Prints only; numbers are quoted in the draft (Appendix C)."""
import json, sys, os, collections, numpy as np, pandas as pd
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "paper-2", "phase2")); import data_panels
raw = [json.loads(l) for l in open(data_panels.MULTIPREF)]; LV = {"A-is-clearly-better": 0, "A-is-slightly-better": 1, "Tie": 2, "B-is-slightly-better": 3, "B-is-clearly-better": 4}
df = pd.DataFrame([(a["evaluator"], a["timestamp"], LV[a["overall_pref"]]) for r in raw for a in r["normal_worker_annotations"] + r["expert_worker_annotations"]], columns=["e", "t", "y"])
print("MultiPref evaluators", df.e.nunique(), "ratings per evaluator median", df.groupby("e").size().median(), "| items with a repeated evaluator", sum(len({a["evaluator"] for a in r["normal_worker_annotations"] + r["expert_worker_annotations"]}) < 4 for r in raw))
def persist(df):
    o = []
    for e, g in df.sort_values(["e", "t"]).groupby("e"):
        if len(g) < 40: continue
        h = len(g) // 2; a, b = g.y.values[:h], g.y.values[h:]; o.append([(a == 2).mean(), (b == 2).mean(), np.isin(a, [0, 4]).mean(), np.isin(b, [0, 4]).mean()])
    o = np.array(o); return len(o), np.corrcoef(o[:, 0], o[:, 1])[0, 1], np.corrcoef(o[:, 2], o[:, 3])[0, 1]
print("MultiPref persistence (n, tie r, extreme r):", persist(df))
rng = np.random.RandomState(0); nl = np.array([persist(df.assign(e=rng.permutation(df.e.values)))[1:] for _ in range(20)]); print("shuffled-label null mean / max:", nl.mean(0).round(2), nl.max(0).round(2))
d = pd.read_csv(data_panels.DICES); demo = [c for c in d.columns if c.startswith("rater_") and c != "rater_id"]; print("DICES raters", d.rater_id.nunique(), "| IDs with inconsistent demographics:", int((d.groupby("rater_id")[demo].nunique() > 1).any(axis=1).sum()))
u = pd.read_json(f"{data_panels.PRISM_DIR}/utterances.jsonl", lines=True); s = pd.read_json(f"{data_panels.PRISM_DIR}/survey.jsonl", lines=True); print("PRISM users", u.user_id.nunique(), "| survey rows per user max", s.groupby("user_id").size().max(), "| users without survey", len(set(u.user_id) - set(s.user_id)))
c = pd.read_csv(data_panels.CA_CSV, usecols=["annotator_id", "annotator_age", "annotator_gender", "annotator_education_level", "annotator_country"]); g = c.groupby("annotator_id").nunique()
print("Community Alignment annotators", len(g), "| share of IDs with any inconsistent demographic:", round(float((g > 1).any(axis=1).mean()), 4))
