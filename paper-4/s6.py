"""Stage 6 (PROTOCOL_STAGE6.md): LoRe under the new-rater protocol. Own gain LoRe(k) − LoRe(0), own − other (permutation control), LoRe(k) − Dp, in choice /
direction accuracy and LL, per panel and label, rater bootstrap; decision rule on PRISM pairs E2 at k = 20."""
import json, glob, os, collections, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.join(HERE, "results")
def rows_of(pat): return [r for f in sorted(glob.glob(pat)) for r in json.load(open(f))["per_rater"]]
def boot(d, w):
    rng = np.random.RandomState(17); bs = [d[ix].sum() / w[ix].sum() for ix in (rng.randint(0, len(d), len(d)) for _ in range(2000))]
    return [100 * d.sum() / w.sum(), 100 * np.percentile(bs, 2.5), 100 * np.percentile(bs, 97.5)]
def per(rows, k, key, den):
    by = collections.defaultdict(list)
    for r in rows:
        if r["k"] == k and key in r: by[(r["fold"], r["rater"])].append(r)
    return {z: (np.mean([x[key] for x in v]), np.mean([x[den] for x in v])) for z, v in by.items()}
def own(rows, k, m, mt, den):
    a, b = per(rows, k, f"{m}_{mt}", den), per(rows, 0, f"{m}_{mt}", den); q = [z for z in a if z in b and a[z][1] > 0 and b[z][1] > 0]
    return boot(np.array([a[z][0] - b[z][0] * a[z][1] / b[z][1] for z in q]), np.array([a[z][1] for z in q]))
def pair(rows, k, k1, k2, den):
    a, b = per(rows, k, k1, den), per(rows, k, k2, den); q = [z for z in a if z in b and a[z][1] > 0]
    return boot(np.array([a[z][0] - b[z][0] for z in q]), np.array([a[z][1] for z in q]))
fmt = lambda v: f"{v[0]:+.2f} [{v[1]:+.2f}, {v[2]:+.2f}]"
L = ["# Stage 6 — LoRe under the new-rater protocol (points for accuracy; ×100 nats for LL)", "",
     "| panel | label | k | LoRe own gain, acc | LoRe own − other, acc | LoRe − Dp, acc | LoRe own gain, LL×100 | LoRe − Dp, LL×100 | raters |", "|---|---|---|---|---|---|---|---|---|"]; out = {}
for panel, pfx, ks in (("prism_pairs", "stage2c_prism_pairs_", (5, 20)), ("multipref_overall", "stage2c_", (20, 50))):
    for ev in ("E2", "E1"):
        rows = rows_of(f"{R}/{pfx}{ev}_f?_lore.json")
        if not rows: continue
        den = "n" if ev == "E2" else "n_dir"
        for k in ks:
            c = {"own_acc": own(rows, k, "LORE", "dir", den), "perm_acc": pair(rows, k, "LORE_dir", "LORE_perm_dir", den), "vsDp_acc": pair(rows, k, "LORE_dir", "Dp_dir", den),
                 "own_ll": own(rows, k, "LORE", "ll", "n"), "vsDp_ll": pair(rows, k, "LORE_ll", "Dp_ll", "n")}
            out[f"{panel}_{ev}_k{k}"] = c; nr = len({(r["fold"], r["rater"]) for r in rows if r["k"] == k})
            L.append(f"| {panel} | {ev} | {k} | {fmt(c['own_acc'])} | {fmt(c['perm_acc'])} | {fmt(c['vsDp_acc'])} | {fmt(c['own_ll'])} | {fmt(c['vsDp_ll'])} | {nr} |")
key = "prism_pairs_E2_k20"
if key in out:
    lb = max(out[key]["own_acc"][1], out[key]["perm_acc"][1]); out["rule_withdraw_prism_null"] = bool(lb > 1.0)
    L += ["", f"**Decision rule (PRISM pairs, binary, k = 20): max lower bound of own gain / own − other = {lb:+.2f} points → {'WITHDRAW the PRISM ranking null' if lb > 1.0 else 'PRISM ranking null stands'}.**"]
hp = {}
for f in sorted(glob.glob(f"{R}/stage2c_*_f?_lore.json")): hp[os.path.basename(f)] = json.load(open(f))["hp"].get("LORE")
L += ["", "Selected LoRe hyper-parameters per run: " + "; ".join(f"{k.replace('stage2c_', '').replace('_lore.json', '')}: B={v['B']}, lr={v['lr']}" for k, v in hp.items() if v)]
json.dump(out, open(f"{R}/stage6_lore.json", "w"), indent=1); open(f"{R}/stage6_lore.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
