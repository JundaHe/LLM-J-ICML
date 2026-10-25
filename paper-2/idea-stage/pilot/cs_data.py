"""Code-summarization benchmark loader (Crupi et al.): 3 raters, 1-5 Likert on CA / Conciseness / Fluency, verbatim zero-shot prompt."""
from __future__ import annotations
import numpy as np, pandas as pd
ROOT = "/mnt/hdd2/jundahe/LLM-J/code/code_summarization"
LEVELS = [1, 2, 3, 4, 5]
CRITS = ["CA", "Conciseness", "Fluency"]

def _template():
    return open(f"{ROOT}/prompts/prompt-judge-code-summarization-zeroshot.tex").read()

def load(language: str = "Java") -> pd.DataFrame:
    d = pd.read_csv(f"{ROOT}/benchmarks/CS-benchmark-{language}.csv")
    tpl = _template()
    summ = d["summary_postprocessed"].fillna(d["summary"]).astype(str)
    d["prompt"] = [tpl.replace("{language}", language).replace("{function}", str(f)).replace("{comment}", s)
                   for f, s in zip(d["target"], summ)]
    d["language"] = language
    return d.reset_index(drop=True)

def H(d: pd.DataFrame, crit: str) -> np.ndarray:
    return d[[f"{crit}_{i}" for i in range(1, 4)]].to_numpy(int)

if __name__ == "__main__":
    import sys; sys.path.insert(0, "/mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/pilot"); import csje_eval as E
    for lang in ["Java", "Python"]:
        d = load(lang); print(lang, "items", len(d))
        for c in CRITS:
            st = E.strata(H(d, c)); print("  ", c, {s: round(float(np.mean(st == s)), 2) for s in ["High", "Partial", "Low"]})
