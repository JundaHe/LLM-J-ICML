"""Commit-message benchmark loader: per-annotator ratings + diff + message, with the verbatim Zeng et al. prompt."""
from __future__ import annotations
import importlib.util, numpy as np, pandas as pd
ROOT = "/mnt/hdd2/jundahe/LLM-J/code/commit_message"
LEVELS = [0, 1, 2, 3, 4]

def _prompt_template():
    spec = importlib.util.spec_from_file_location("u", f"{ROOT}/replication_package/cmeval/llm_metrics/prompts/unified_prompts.py")
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.UNIFIED_EVALUTE_PROMPT_TEMPLATE_ZERO_SHOT_NONCOT

def load(pool: str = "developer", max_diff_chars: int = 6000) -> pd.DataFrame:
    """Return one row per message with columns: hash, msg_type, message, diff, what_1..6, why_1..6, prompt."""
    bench = pd.read_csv(f"{ROOT}/data/CM-benchmark.csv")
    src = pd.read_csv(f"{ROOT}/datasets/commits.csv")
    d = bench[bench.msg_type == pool].merge(src[["hash", "git_diff_u3"]], on="hash", how="left")
    assert d.git_diff_u3.notna().all(), "missing diffs"
    tpl = _prompt_template()
    d["diff"] = d.git_diff_u3.str.slice(0, max_diff_chars)
    d["prompt"] = [tpl.replace("{diff}", df_).replace("{message}", str(msg)).replace("{{", "{").replace("}}", "}")
                   for df_, msg in zip(d["diff"], d["commit_message"])]
    return d.reset_index(drop=True)

def H(d: pd.DataFrame, crit: str) -> np.ndarray:
    return d[[f"{crit}_{i}" for i in range(1, 7)]].to_numpy(int)
