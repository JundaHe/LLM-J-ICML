"""Manuscript ↔ artefact consistency check (Codex round 12 §D.3). Builds the set of canonical numbers from the frozen artefacts and checks that every
occurrence of a 'matching-shaped' number in PAPER_DRAFT.md (contrasts with 4 decimals, intervals) is one of them; also checks specific named claims.
Exit code 1 if any mismatch. Usage: python check_consistency.py"""
import json, re, os, sys, numpy as np, pandas as pd
from paths import LLMJ
P = os.path.dirname(os.path.abspath(__file__)); PILOT = LLMJ + "/paper-2/idea-stage/pilot"
draft = open(f"{P}/PAPER_DRAFT.md").read(); tables = open(f"{P}/RESULTS_TABLES.md").read()
canon = {}   # value string -> source
def add(v, src, nd=4):
    for s in (f"{v:+.{nd}f}", f"{v:.{nd}f}", f"{abs(v):.{nd}f}"): canon.setdefault(s, src)
# SummEval block (primary + lamext)
for tag, f in (("T3b primary", "analysis_block_summeval.json"), ("T3b lamext", "analysis_block_summeval_lamext.json")):
    j = json.load(open(f"{P}/results/lora/summeval_coherence8/{f}"))
    for r in j["rows"]:
        for k in ("est", "lo", "hi", "lo90", "hi90"):
            if r.get(k) is not None and not (isinstance(r[k], float) and np.isnan(r[k])): add(float(r[k]), f"{tag} {r['contrast']} {r['estimand']} {k}")
        for dct in (r.get("per_seed") or {}, r.get("per_fold") or {}):
            for v in dct.values(): add(float(v), f"{tag} {r['contrast']} {r['estimand']} cell")
# POPQUORN block (T3c) + rater-aware sensitivity
j = json.load(open(f"{P}/results/lora/popquorn_off8/analysis_block_popquorn.json"))
for r in j["rows"]:
    for k in ("est", "lo", "hi", "lo90", "hi90"):
        if r.get(k) is not None and not (isinstance(r[k], float) and np.isnan(r[k])): add(float(r[k]), f"T3c {r['contrast']} {r['estimand']} {k}")
    for dct in (r.get("per_seed") or {}, r.get("per_fold") or {}):
        for v in dct.values(): add(float(v), f"T3c {r['contrast']} {r['estimand']} cell")
for r in json.load(open(f"{P}/results/lora/popquorn_off8/sensitivity_popquorn_users.json"))["rows"]:
    for k in ("est", "pigeonhole_lo", "pigeonhole_hi", "pigeonhole_lo90", "pigeonhole_hi90", "item_lo", "item_hi"): add(float(r[k]), f"T3c rater-aware {r['contrast']} {k}")
import sys as _sys; _sys.path.insert(0, P); import data_panels as _dp
_H = _dp.load("popquorn_off8")["H"]; _LV = np.arange(5)
def _rps(Pm, y): c = np.cumsum(Pm, 1); st = (_LV[None] >= y[:, None]).astype(float); return ((c - st) ** 2).sum(1) / 4
for _sd in ("s0", "s0_seed2001", "s0_seed2002"):
    for _f in range(3):
        _b = f"{P}/results/lora/popquorn_off8/{_sd}/f{_f}"; _it = pd.read_csv(f"{_b}/chen/items_test.csv").row.to_numpy(); _y = _H[_it, _f]
        _L = {a: _rps(np.load(f"{_b}/{a}/P_test.npy"), _y).mean() for a in ("chen", "perm", "perm_mode")}
        add(_L["perm"] - _L["chen"], f"T3c cell {_sd} f{_f} perm−chen"); add(_L["perm_mode"] - _L["chen"], f"T3c cell {_sd} f{_f} perm_mode−chen")
# heads T2b (arm − soft per panel) from runs.jsonl
TAG = {"hs2_help5": "_v7", "popquorn_off8": "_v7", "dices990": "_v7", "popquorn_pol5": "_v7", "csc6": "_v7", "emobank_reader_v5": "_v7"}
for key in [k for k in ("summeval_coherence8", "bw", "dices", "scalabrino", "hs2_help5", "popquorn_off8", "dices990", "popquorn_pol5", "csc6", "emobank_reader_v5") if os.path.exists(f"{P}/results/probe_mean2/{k}{TAG.get(k, '_v6')}/runs.jsonl")]:
    df = pd.read_json(f"{P}/results/probe_mean2/{key}{TAG.get(key, '_v6')}/runs.jsonl", lines=True); idx = ["seed", "isplit", "rsplit"]
    for m, nd in (("pop_rps", 4), ("kl_ref", 3), ("D_partial", 3)):
        piv = df.pivot_table(index=idx, columns="arm", values=m, dropna=False)
        for a in piv.columns:
            if a != "soft" and piv[a].notna().any(): add(float((piv[a] - piv["soft"]).mean()), f"T2b {key} {a}-soft {m}", nd); add(float((piv[a] - piv["soft"]).sem()), f"T2b {key} {a}-soft {m} sem", nd)
    for a in ("soft_pmode", "soft_pmm"):
        dd = df[df.arm == a]; add(float(dd.changed_fraction.mean()), f"T2b {key} {a} changed", 3); add(float(dd.dose_tv.mean()), f"T2b {key} {a} tv", 2); add(float(dd.dose_tv.mean()), f"T2b {key} {a} tv", 3)
# ChaosNLI
for pkey, ptag in (("chaosnli_mnli", "_v6"), ("chaosnli_snli", "_v7"), ("chaosnli_alphanli", "_v7")):
  for m in (5, 10, 20, 50):
    f = f"{P}/results/probe_nominal/{pkey}_m{m}{ptag}/runs.jsonl"
    if not os.path.exists(f): continue
    df = pd.read_json(f, lines=True); kl = df.pivot_table(index=["seed", "isplit"], columns="arm", values="kl_ref")
    for a, b in (("soft_pzc", "soft"), ("soft_pmode", "soft"), ("soft", "zc"), ("soft", "cond"), ("soft", "shrunk")): add(float((kl[a] - kl[b]).mean()), f"T5 {pkey} m{m} {a}-{b}", 3)
    dz = df[df.arm == "soft_pzc"]; add(float(dz.changed_fraction.mean()), f"T5 {pkey} m{m} pzc changed", 3); add(float(dz.support_fraction.mean()), f"T5 {pkey} m{m} pzc support", 2); add(float(dz.dose_tv_final_all.mean()), f"T5 {pkey} m{m} tv all", 3)
# SummEval single-seed s0 analysis (hard − chen etc.)
f0 = f"{P}/results/lora/summeval_coherence8/s0/analysis_lora_v3.json"
if os.path.exists(f0):
    def walk0(o, path):
        if isinstance(o, dict):
            for k, v in o.items(): walk0(v, path + "/" + str(k))
        elif isinstance(o, list):
            for v in o: walk0(v, path)
        elif isinstance(o, (int, float)) and not isinstance(o, bool) and abs(o) < 1: add(float(o), f"summeval s0 analysis_lora_v3 {path}")
    walk0(json.load(open(f0)), "")
# dose audit
da = pd.read_csv(f"{P}/results/dose_audit_summary.csv")
for _, r in da.iterrows():
    for col in ("support", "changed", "tv_chg", "tv_all"): add(float(r[col]), f"dose_audit {r.panel} {r.arm} {col}", 3); add(float(r[col]), f"dose_audit {r.panel} {r.arm} {col}", 2)
# ---- scan the draft for 4-decimal signed numbers and interval endpoints (the contrast-shaped numbers)
nums = re.findall(r"(?<![\d.])[−+-]?\d\.\d{4}(?!\d)", draft); bad = []   # exclude arXiv ids like 2609.01073
for s in sorted(set(nums)):
    s2 = s.replace("−", "-")
    v = float(s2)
    keys = {f"{v:+.4f}", f"{v:.4f}", f"{abs(v):.4f}"}
    if not keys & set(canon): bad.append(s)
print(f"canonical values: {len(canon)}; 4-decimal numbers in draft: {len(set(nums))}; unmatched: {len(bad)}")
for s in bad: print("  UNMATCHED:", s, "| context:", [draft[max(0, m.start() - 70): m.end() + 20].replace("\n", " ") for m in re.finditer(re.escape(s), draft)][:1])
# ---- named claims
claims = []
j = json.load(open(f"{P}/results/lora/summeval_coherence8/analysis_block_summeval.json")); rows = {(r["contrast"], r["estimand"]): r for r in j["rows"]}
pc = rows[("perm − chen", "raw")]; pm = rows[("perm_mode − chen", "raw")]
claims.append(("perm−chen raw in draft", f"{pc['est']:+.4f} [{pc['lo']:+.4f}, {pc['hi']:+.4f}]".replace("-", "−") in draft.replace("-", "−")))
dd = draft.replace("-", "−"); est_s = f"{pm['est']:+.4f}".replace("-", "−"); lo_s = f"{pm['lo']:+.4f}".replace("-", "−"); hi_s = f"{pm['hi']:+.4f}".replace("-", "−")
wins = [dd[m.start(): m.start() + 160] for m in re.finditer(re.escape(est_s), dd)]
claims.append(("perm_mode−chen raw est+interval together in draft (some occurrence)", any(lo_s in w and hi_s in w for w in wins)))
jp = json.load(open(f"{P}/results/lora/popquorn_off8/analysis_block_popquorn.json")); rp = {(r["contrast"], r["estimand"]): r for r in jp["rows"]}
for _c in ("perm − chen", "perm_mode − chen"):
    _r = rp[(_c, "raw")]; claims.append((f"POPQUORN {_c} raw est+interval in draft", f"{_r['est']:+.4f} [{_r['lo']:+.4f}, {_r['hi']:+.4f}]".replace("-", "−") in draft.replace("-", "−")))
allpos = all(v > 0 for v in list(pm["per_seed"].values()) + list(pm["per_fold"].values()))
claims.append(("mode-only positive in all seed/fold marginals", allpos))
# ---- structural assertions (Codex round 15 §D.7)
tab = tables
claims.append(("T2b lists exactly ten primary ordinal panels", tab.count("(`_v7`,") + tab.count("(`_v6`,") == 10))
claims.append(("DICES-990 pmmx dose 0.985 (TV>1e-9 rule) in draft", "0.985" in draft and "0.995 on Buse" not in draft))
claims.append(("pmmx range −0.0024…+0.0006 in draft (no stale +0.0005 range)", "−0.0024 to +0.0006" in draft and "−0.0024 to +0.0005" not in draft))
claims.append(("zero-TV wording is pre-projection only", "no zero-TV donor pairs before projection" in draft and "Zero-TV pairs were 0 in every configuration" not in draft))
claims.append(("no commit / bridge / VERIFY / arXiv-id residue in draft", all(s not in draft for s in ("commit What", "commit Why", "bridge", "[VERIFY]")) and not re.search(r"arXiv \d{4}\.\d{5}", draft)))
req = [f"{P}/results/MANIFEST.json", f"{P}/results/nominal_final_dose.json", f"{P}/results/nominal_final_dose_chaosnli_snli.json", f"{P}/results/nominal_final_dose_chaosnli_alphanli.json", f"{P}/results/probe_mean/bw_inject_v8/runs.jsonl", f"{P}/results/probe_mean/scalabrino_inject_v8/runs.jsonl", f"{P}/results/probe_mean/popquorn_off8_inject_v8/runs.jsonl", f"{P}/results/probe_mean/csc6_inject_v8/runs.jsonl"] + [f"{P}/results/probe_nominal/chaosnli_{k}_m{m}{t}/runs.jsonl" for k, t in (("mnli", "_v6"), ("snli", "_v7"), ("alphanli", "_v7")) for m in (5, 10, 20, 50)]
claims.append(("required artefacts present", all(os.path.exists(p) for p in req)))
for name, ok in claims: print(("OK   " if ok else "FAIL ") + name)
sys.exit(1 if bad or not all(ok for _, ok in claims) else 0)
