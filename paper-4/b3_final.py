"""Stage 2b Amendment 4: final B3 — runs b3_compare.py for the four pre-specified versions (seed 2000 primary, seed 3000, seed 4000, three-seed average)
and applies the Amendment-3/4 wording rule to DFs(D-LoRA) − RC-LoRA at k = 20 (LL; direction reported alongside)."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results"); PY = sys.executable
VERS = [("seed 2000 (primary)", ""), ("seed 3000", "s3000"), ("seed 4000", "s4000"), ("three-seed average", "seedavg3")]
rows, lb = [], []
for name, v in VERS:
    subprocess.run([PY, f"{HERE}/b3_compare.py"] + ([v] if v else []), check=True, capture_output=True)
    o = json.load(open(f"{R}/stage2b_B3{'_' + v if v else ''}.json"))
    ll = [-x for x in o["k20_lora_DFs"]["ll"]]; ll = [ll[0], ll[2], ll[1]]                      # b3_compare reports RC − model; flip to DFs − RC
    dr = [-x for x in o["k20_lora_DFs"]["dir"]]; dr = [dr[0], dr[2], dr[1]]
    rc = o["k20_lora_D"]["ll"]; fz = [-x for x in o["k20_frozen_DFs"]["ll"]]; fz = [fz[0], fz[2], fz[1]]
    lb.append(ll[1]); rows.append(f"| {name} | {ll[0]:+.4f} [{ll[1]:+.4f}, {ll[2]:+.4f}] | {dr[0]:+.4f} [{dr[1]:+.4f}, {dr[2]:+.4f}] | {rc[0]:+.4f} [{rc[1]:+.4f}, {rc[2]:+.4f}] | {fz[0]:+.4f} [{fz[1]:+.4f}, {fz[2]:+.4f}] | {o['k20_lora_DFs']['n_raters']} |")
verdict = "better" if all(x > 0 for x in lb) else ("not worse" if all(x >= -0.005 for x in lb) else "seed-dependent")
L = ["# B3 final (Stage 2b Amendments 3–4) — MultiPref, new raters, k = 20", "",
     "| version | DFs(D-LoRA) − RC-LoRA, LL/rating | DFs(D-LoRA) − RC-LoRA, direction | RC-LoRA − D-LoRA, LL | DFs(frozen) − RC-LoRA, LL | raters |", "|---|---|---|---|---|---|"] + rows + \
    ["", f"Wording rule (Am. 3/4): lower bounds {', '.join(f'{x:+.4f}' for x in lb)} → **{verdict}**."]
open(f"{R}/stage2b_B3_final.md", "w").write("\n".join(L) + "\n"); json.dump({"verdict": verdict, "lower_bounds": lb}, open(f"{R}/stage2b_B3_final.json", "w"), indent=1); print("\n".join(L))
