"""Manuscript ↔ artefact consistency check (Codex round 12 §D.3). Builds the set of canonical numbers from the frozen artefacts and checks that every
occurrence of a 'matching-shaped' number in PAPER_DRAFT.md (contrasts with 4 decimals, intervals) is one of them; also checks specific named claims.
Exit code 1 if any mismatch. Usage: python check_consistency.py"""
import json, re, os, sys, numpy as np, pandas as pd
from paths import LLMJ
P = os.path.dirname(os.path.abspath(__file__)); PILOT = LLMJ + "/paper-2/idea-stage/pilot"
DRAFT = sys.argv[1] if len(sys.argv) > 1 else "PAPER_DRAFT.md"   # 2026-11-07: draft is an argument; before, v2 checks silently read v1
draft = open(f"{P}/{DRAFT}").read(); print("checking", DRAFT); tables = open(f"{P}/RESULTS_TABLES.md").read()
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
# v2-era sources (2026-11-07): LoRA budget blocks (all rounds), per-fold contrasts, R20-7 compare, shrinkage (bfix + SUMMARY.md)
import glob as _glob
def walk(o, src):
    if isinstance(o, dict): [walk(v, src) for v in o.values()]
    elif isinstance(o, list): [walk(v, src) for v in o]
    elif isinstance(o, (int, float)) and not isinstance(o, bool) and np.isfinite(o) and abs(o) < 1: add(float(o), src)
for f in sorted(_glob.glob(f"{P}/results/lora_budget*/summary*.json") + [f"{P}/results/lora_by_fold.json", f"{P}/results/lora_budget_r207/compare.json"] + _glob.glob(f"{P}/results/shrinkage/*_bfix.json")):
    if os.path.exists(f): walk(json.load(open(f)), os.path.relpath(f, P))
for v in re.findall(r"[−+-]?\d\.\d{4}", open(f"{P}/results/shrinkage/SUMMARY.md").read()): add(float(v.replace("−", "-")), "shrinkage/SUMMARY.md")
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
claims.append(("DICES-990 pmmx dose 0.985 (TV>1e-9 rule) in draft" + ("" if DRAFT == "PAPER_DRAFT.md" else " [v2+: dose details live in the appendix; only the stale value is checked]"), ("0.985" in draft or not DRAFT == "PAPER_DRAFT.md") and "0.995 on Buse" not in draft))
claims.append(("pmmx range −0.0024…+0.0006 in draft (no stale +0.0005 range)", "−0.0024 to +0.0006" in draft and "−0.0024 to +0.0005" not in draft))
claims.append(("zero-TV wording is pre-projection only" + ("" if DRAFT == "PAPER_DRAFT.md" else " [v2+: only the stale wording is checked]"), ("no zero-TV donor pairs before projection" in draft or not DRAFT == "PAPER_DRAFT.md") and "Zero-TV pairs were 0 in every configuration" not in draft))
claims.append(("no commit / bridge / VERIFY / arXiv-id residue in draft", all(s not in draft for s in ("commit What", "commit Why", "bridge", "[VERIFY]")) and not re.search(r"arXiv \d{4}\.\d{5}", draft)))
req = [f"{P}/results/MANIFEST.json", f"{P}/results/nominal_final_dose.json", f"{P}/results/nominal_final_dose_chaosnli_snli.json", f"{P}/results/nominal_final_dose_chaosnli_alphanli.json", f"{P}/results/probe_mean/bw_inject_v8/runs.jsonl", f"{P}/results/probe_mean/scalabrino_inject_v8/runs.jsonl", f"{P}/results/probe_mean/popquorn_off8_inject_v8/runs.jsonl", f"{P}/results/probe_mean/csc6_inject_v8/runs.jsonl"] + [f"{P}/results/probe_nominal/chaosnli_{k}_m{m}{t}/runs.jsonl" for k, t in (("mnli", "_v6"), ("snli", "_v7"), ("alphanli", "_v7")) for m in (5, 10, 20, 50)]
claims.append(("required artefacts present", all(os.path.exists(p) for p in req)))
# ---- headline percentages (2026-11-07 percentage audit, reviews/percent_audit_v3_2026-11-07.md; v2+ drafts only)
if DRAFT != "PAPER_DRAFT.md":
    import glob as _g, math as _m, collections as _co
    _J = lambda p: json.load(open(f"{P}/results/{p}")); _r = lambda f: _J(f"decode_decomp/{f}.json")["clt"]["G_own/X_own"]
    def _rng(pat):
        v = [100 * json.load(open(x))["est"]["G_own/X_own"] for x in sorted(_g.glob(f"{P}/results/decode_decomp/{pat}"))]; return f"{round(min(v))}–{round(max(v))} %", len(v)
    for lab, pat in (("DICES-350 dispersion plant γ0.4 recovery", "dices_r22_plant0.4_s*.json"), ("DICES-350 polarisation plant γ1.5 recovery", "dices_r22p_polar1.5_s*.json")):
        t, n = _rng(pat); claims.append((f"{lab} {t} (n={n}) in draft", n == 5 and t in draft))
    _det = sum(json.load(open(x))["clt"]["G_own"]["ci95"][0] > 0 for x in _g.glob(f"{P}/results/decode_decomp/dices_r22p_polar1.5_s*.json")); claims.append((f"polarisation detected {_det}/5 is 3", _det == 3))
    _nli = [100 * _r(f"chaosnli_{k}_r21")["est"] for k in ("mnli", "snli")]; claims.append((f"NLI recovery {round(min(_nli))}–{round(max(_nli))} % in draft", f"{round(min(_nli))}–{round(max(_nli))} %" in draft))
    _ub = max(100 * _r(f)["ci95"][1] for f in ("dices_a40_r21", "dices_a40_qwen3_r22", "dices_a40_olmo_r22")); claims.append((f"DICES-350 upper bounds ≤ {_m.ceil(_ub)} % in draft", f"≤ {_m.ceil(_ub)} %" in draft))
    _xc = [100 * [r for r in _J(f"rho_own/chaosnli_{k}.json")["rows"] if r["a"] == 20][0]["X_cross"] / [r for r in _J(f"rho_own/chaosnli_{k}.json")["rows"] if r["a"] == 20][0]["X"] for k in ("mnli", "snli")]
    claims.append((f"ChaosNLI cross-term share {round(min(_xc))}–{round(max(_xc))} % of X in draft", f"{round(min(_xc))}–{round(max(_xc))} % of $X$" in draft))
    _lo = min(100 * _r(f)["ci95"][0] for f in ("chaosnli_mnli_r21", "chaosnli_snli_r21", "chaosnli_mnli_a4_r21", "chaosnli_snli_a4_r21")); _hi = 100 * _r("dorn_all_r21")["ci95"][1]
    claims.append((f"pooled NLI–ordinal margin {_m.floor(_lo)} % vs {_m.ceil(_hi)} % in draft", f"{_m.floor(_lo)} % vs {_m.ceil(_hi)} %" in draft))
    for _a, _nli, _ord in ((20, ("chaosnli_mnli_r21", "chaosnli_snli_r21", "chaosnli_mnli_qwen3_r21", "chaosnli_mnli_olmo_r21"), ("dices_r21", "dices_qwen3_r21", "dices_olmo_r21", "dorn_all_r21", "dorn_java_r21")),
                           (4, ("chaosnli_mnli_a4_r21", "chaosnli_snli_a4_r21"), ("summeval_coherence8_r21", "summeval_coherence8_qwen3_r21", "summeval_coherence8_olmo_r21", "summeval_relevance8_r21"))):   # R22-7: matched rater count
        _t = f"{_m.floor(min(100 * _r(f)['ci95'][0] for f in _nli))} % vs {_m.ceil(max(100 * _r(f)['ci95'][1] for f in _ord))} % at {_a}"; claims.append((f"matched-a margin {_t} in draft", _t in draft))
    claims.append((f"Dorn upper bound {_hi / 100:.2f} in draft (no stale 0.18)", f"upper bound {_hi / 100:.2f}" in draft and "upper bound 0.18" not in draft))
    _s = _J("lora_budget_r20_pq/summary_popquorn_off8.json"); _a1, _a2 = _s["a1_F1.0"]["diff_vs_full"], _s["a2_F1.0"]["diff_vs_full"]
    claims.append((f"POPQUORN second rating recovers {round(100 * (_a1 - _a2) / _a1)} % in draft", f"recovers {round(100 * (_a1 - _a2) / _a1)} %" in draft))
    _mv = []
    for k in ("mnli", "snli"):
        rows = [json.loads(l) for l in open(f"{P}/results/budget_heads/chaosnli_{k}/runs.jsonl") if l.strip()]; rows = [x for x in rows if x["arm"] == "soft"]; n = max(x["n_items"] for x in rows); d = _co.defaultdict(list)
        for x in rows:
            if x["n_items"] == n: d[x["a"]].append(x["pop_rps"])
        _mv.append(100 * (np.mean(d[2]) - np.mean(d[1])) / np.mean(d[1]))
    _t = f"−{round(-max(_mv))} to −{round(-min(_mv))} %"; claims.append((f"ChaosNLI second-rating marginal value {_t} in draft", _t in draft))
for name, ok in claims: print(("OK   " if ok else "FAIL ") + name)
sys.exit(1 if bad or not all(ok for _, ok in claims) else 0)
