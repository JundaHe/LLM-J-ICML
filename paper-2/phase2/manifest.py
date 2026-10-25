"""Evidence manifest: sha256 of every results artefact that RESULTS_TABLES.md / PAPER_DRAFT.md draw on, plus the LoRA certificates (dose, mapping_hash, target_hash).
Usage: python manifest.py (figures in results/figures are hashed too)  -> results/MANIFEST.json (+ printed summary). Re-run before regenerating tables; the paper cites the manifest hash."""
import os, glob, json, hashlib, subprocess, datetime
from paths import LLMJ
HERE = os.path.dirname(os.path.abspath(__file__)); PILOT = LLMJ + "/paper-2/idea-stage/pilot"
def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()
groups = {
 "heads_frozen": [f"{HERE}/results/probe_mean2/{k}{t}/runs.jsonl" for k, t in (("summeval_coherence8", "_v6"), ("bw", "_v6"), ("dices", "_v6"), ("scalabrino", "_v6"), ("hs2_help5", "_v7"), ("popquorn_off8", "_v7"), ("popquorn_pol5", "_v7"), ("dices990", "_v7"), ("csc6", "_v7"), ("emobank_reader_v5", "_v7"))],
 "nominal_frozen": sorted(glob.glob(f"{HERE}/results/probe_nominal/chaosnli_mnli_m*_v6/runs.jsonl")) + sorted(glob.glob(f"{HERE}/results/probe_nominal/chaosnli_snli_m*_v7/runs.jsonl")) + sorted(glob.glob(f"{HERE}/results/probe_nominal/chaosnli_alphanli_m*_v7/runs.jsonl")),
 "nominal_final_dose": sorted(glob.glob(f"{HERE}/results/nominal_final_dose*.json")),
 "positive_controls_v8": sorted(glob.glob(f"{HERE}/results/probe_mean/*_inject_v8/runs.jsonl")),
 "dose_audit": [f"{HERE}/results/dose_audit.jsonl", f"{HERE}/results/dose_audit_summary.csv"],
 "gxr": [f"{HERE}/results/gxr_check.json", f"{HERE}/results/gxr_check.jsonl"],
 "summeval_block": [f"{HERE}/results/lora/summeval_coherence8/analysis_block_summeval.json"] + sorted(glob.glob(f"{HERE}/results/lora/summeval_coherence8/analysis_block_summeval_lamext.json")) + sorted(glob.glob(f"{HERE}/results/lora/summeval_coherence8/s0/analysis_lora_v3.json")),
 "summeval_cells": sorted(glob.glob(f"{HERE}/results/lora/summeval_coherence8/s0*/f*/*/P_test.npy")),
 "popquorn_block": [f"{HERE}/results/lora/popquorn_off8/analysis_block_popquorn.json", f"{HERE}/results/lora/popquorn_off8/sensitivity_popquorn_users.json", f"{HERE}/lora_chain_popquorn.sh"],
 "popquorn_cells": sorted(glob.glob(f"{HERE}/results/lora/popquorn_off8/s0*/f*/*/P_test.npy")),
 "tables_and_text": [f"{HERE}/RESULTS_TABLES.md", f"{HERE}/PAPER_DRAFT.md", f"{HERE}/PAPER_OUTLINE.md"],
 "checks": [f"{HERE}/check_consistency.py", f"{HERE}/results/check_consistency_latest.txt"],
 "figures": sorted(glob.glob(f"{HERE}/results/figures/*.pdf")),
 "figure_code": [f"{HERE}/make_fig1.py", f"{HERE}/make_figures.py"],
 "latex": [f"{HERE}/latex/main.tex", f"{HERE}/latex/preamble.tex", f"{HERE}/latex/figures_block.tex", f"{HERE}/build_latex.py", f"{HERE}/latex/tab_heads.tex", f"{HERE}/latex/tab_summeval.tex", f"{HERE}/latex/tab_nominal.tex", f"{HERE}/make_latex_tables.py"],
 "related_work": [f"{HERE}/RELATED_WORK_TODO.md", f"{HERE}/references.bib"],
 "code": sorted(glob.glob(f"{HERE}/*.py")) + [f"{PILOT}/support_audit.py"],
}
man = {"generated": datetime.datetime.now().isoformat(timespec="seconds"), "git_head": subprocess.run(["git", "rev-parse", "HEAD"], cwd=HERE, capture_output=True, text=True).stdout.strip(), "files": {}, "lora_certificates": {}}
for g, files in groups.items():
    for p in files:
        if os.path.exists(p): man["files"][os.path.relpath(p, LLMJ + "/paper-2")] = dict(group=g, sha256=sha(p), bytes=os.path.getsize(p))
for p in sorted(glob.glob(f"{HERE}/results/lora/summeval_coherence8/s0*/f*/*/meta.json")) + sorted(glob.glob(f"{HERE}/results/lora/popquorn_off8/s0*/f*/*/meta.json")):
    d = os.path.dirname(p)
    if not os.path.exists(f"{d}/P_test.npy"): continue
    m = json.load(open(p)); man["lora_certificates"][os.path.relpath(d, LLMJ + "/paper-2")] = {k: m.get(k) for k in ("arm", "opt_seed", "perm_seed", "changed_fraction", "dose_tv_mean", "n_tv_zero", "matching", "mapping_hash", "target_hash", "mean_shift_max", "model")}
json.dump(man, open(f"{HERE}/results/MANIFEST.json", "w"), indent=1)
mh = sha(f"{HERE}/results/MANIFEST.json"); open(f"{HERE}/results/MANIFEST.sha256", "w").write(mh + "\n")
from collections import Counter
print("manifest:", len(man["files"]), "files;", len(man["lora_certificates"]), "LoRA cells;", Counter(v["group"] for v in man["files"].values()), "\nMANIFEST sha256", mh)
