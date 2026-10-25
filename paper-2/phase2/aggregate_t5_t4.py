"""Regenerate T5 (ChaosNLI nominal, probe_nominal _v6) and T4 (positive controls, probe_mean *_inject_v6) markdown from the v6 artefacts only, with dose certificates."""
import os, json, numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
def f4(d): return f"{d.mean():+.3f}±{d.sem():.3f}"
NOMINAL = [("chaosnli_mnli", "ChaosNLI MNLI", "_v6", ""), ("chaosnli_snli", "ChaosNLI SNLI", "_v7", "_chaosnli_snli"), ("chaosnli_alphanli", "ChaosNLI αNLI (K = 2)", "_v7", "_chaosnli_alphanli")]
out = []
for pkey, plabel, ptag, fdsuf in NOMINAL:
    if not all(os.path.exists(f"{HERE}/results/probe_nominal/{pkey}_m{m}{ptag}/runs.jsonl") for m in (5, 10, 20, 50)): out.append(f"## T5 ({plabel}) — pending\n"); continue
    FD = json.load(open(f"{HERE}/results/nominal_final_dose{fdsuf}.json")) if os.path.exists(f"{HERE}/results/nominal_final_dose{fdsuf}.json") else {}
    out += [f"## T5 ({plabel}). Nominal decomposition (heads, `{ptag}`: histogram-class matching, full dose certificate; m training annotations; KL to a FIXED 50-annotation reference panel; 9 configurations = 3 optimizer seeds × 3 item splits, annotation subsample tied to the item split; ± = descriptive SEM over the 9 dependent configurations). Constraint-certified `zc`/`pzc` targets (q_z = c, q_k ≤ c; 0 violations). Dose columns: donor-mapped fraction / support / mean final TV over all training items [effective-change sensitivity, TV > 1e-6]; zero donor-TV pairs = 0 in every configuration.",
            "| m | soft − zc (KL) | soft − cond (KL) | soft − shrunk (KL) | pzc − soft (KL) | pmode − soft (KL) | resid ρ: soft − zc | resid ρ: pzc − soft | pzc dose (mapped / support / final TV-all) [eff. change] | pmode dose (changed / TV all) | fidelity resid ρ: m-hist / zc |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for m in (5, 10, 20, 50):
        df = pd.read_json(f"{HERE}/results/probe_nominal/{pkey}_m{m}{ptag}/runs.jsonl", lines=True); idx = ["seed", "isplit"]; kl = df.pivot_table(index=idx, columns="arm", values="kl_ref"); rr = df.pivot_table(index=idx, columns="arm", values="resid_spearman", dropna=False)
        for a in ("soft", "zc", "soft_pzc"):
            if a not in rr.columns: rr[a] = np.nan          # K = 2: residual-share rank is undefined (one non-modal class)
        assert (df[df.arm.isin(["soft_pmode", "soft_pzc"])].n_tv_zero == 0).all()
        dz = df[df.arm == "soft_pzc"]; dm = df[df.arm == "soft_pmode"]; fid = {a: rr[a].mean() for a in ("fidelity_soft", "fidelity_zc") if a in rr.columns}; fd = FD.get(str(m), {}).get("zc", {})
        out.append(f"| {m} | {f4(kl['soft'] - kl['zc'])} | {f4(kl['soft'] - kl['cond'])} | {f4(kl['soft'] - kl['shrunk'])} | {f4(kl['soft_pzc'] - kl['soft'])} | {f4(kl['soft_pmode'] - kl['soft'])} | {f4(rr['soft'] - rr['zc'])} | {f4(rr['soft_pzc'] - rr['soft'])} | "
                   f"{dz.changed_fraction.mean():.3f} / {dz.support_fraction.mean():.2f} / {dz.dose_tv_final_all.mean():.3f} [{fd.get('final_changed_1e6', float('nan')):.3f}] | {dm.changed_fraction.mean():.2f} / {dm.dose_tv_final_all.mean():.3f} | {fid.get('fidelity_soft', float('nan')):.2f} / {fid.get('fidelity_zc', float('nan')):.2f} |")
    out.append("")
out += ["## T4. Semi-synthetic sanity check (`_v8`: histogram-class matching AND injection applied separately within the realised training-position and evaluation-position panels, so mode and mean are preserved within each subset — Codex round 14; heads; 30 cfgs; D = Spearman of predicted vs reference disagreement; ± = descriptive SEM over paired configurations)",
        "| panel | oracle resid gap (oracle_soft − oracle_mean2, D) | soft − mean2 (D) | pmm − soft (D) | learnable fraction (soft−mean2)/(oracle gap) |", "|---|---|---|---|---|"]
for key, label in (("bw", "Buse–Weimer"), ("scalabrino", "Scalabrino"), ("popquorn_off8", "POPQUORN offensiveness"), ("csc6", "CSC sarcasm")):
    f = f"{HERE}/results/probe_mean/{key}_inject_v8/runs.jsonl"
    if not os.path.exists(f): out.append(f"| {label} | pending |"); continue
    df = pd.read_json(f, lines=True); idx = [c for c in ("seed", "isplit", "rsplit") if c in df.columns]; D = df.pivot_table(index=idx, columns="arm", values="D_spearman", dropna=False)
    if "oracle_soft" not in D.columns or D["oracle_soft"].isna().all():
        out.append(f"| {label} | D undefined (a single held-out annotation position gives no reference disagreement) | — | — | — |"); continue
    gap = D["oracle_soft"] - D["oracle_mean2"]; sm = D["soft"] - D["mean2"]; ps = D["soft_pmm"] - D["soft"]
    out.append(f"| {label} | {f4(gap)} | {f4(sm)} | {f4(ps)} | {sm.mean() / gap.mean():.2f} |" if gap.mean() > 0.05 else f"| {label} | {f4(gap)} (no positive oracle gap under this injection: no positive-control evidence) | {f4(sm)} | {f4(ps)} | — |")
out.append("Earlier versions (`_v6`/`_v7`) injected on the full annotation row before the position split, so mode and mean were not preserved within the realised panels (Codex round 14); they are superseded. Under the subset-wise injection the Scalabrino and POPQUORN offensiveness oracle gaps are ≈ 0 or negative (the feature-aligned injection is not recoverable from the reference positions there), and CSC's single held-out position leaves D undefined, so only Buse–Weimer supplies positive-control evidence.\n")
print("\n".join(out))
