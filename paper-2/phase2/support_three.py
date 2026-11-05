"""R20-T (ROUND20_PROTOCOL.md, issue 8): on the three-rater panels, the share of items whose exact mode-and-mean cell (z_label tie rule: among tied modes the one nearest
the median, then the lowest; mean = rating sum) holds more than one histogram — for the full three ratings and for the two-rating panel 1 of the leave-one-out split.
Writes results/support_three.json. Usage: python support_three.py"""
import sys, os, json, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE); sys.path.insert(0, f"{HERE}/../idea-stage/pilot")
import data_panels
from support_audit import z_label
def support(H, K):
    keys = [(z_label(r), int(r.sum())) for r in H]; cells = {}
    for k, r in zip(keys, H): cells.setdefault(k, set()).add(tuple(np.bincount(r, minlength=K)))
    return float(np.mean([len(cells[k]) > 1 for k in keys]))
out = {}
for p in ["crupi_ca", "crupi_conc", "crupi_flu", "mlcq3", "roy_ca", "roy_conc", "roy_flu"]:
    P = data_panels.load(p); H = P["H"].astype(int); K = P["K"]
    out[p] = dict(K=K, items=len(H), support_3=support(H, K), support_2=float(np.mean([support(np.delete(H, j, 1), K) for j in range(3)])), all_distinct_3=float(np.mean([len(set(r)) == 3 for r in H])))
    print(p, out[p], flush=True)
json.dump(out, open(f"{HERE}/results/support_three.json", "w"), indent=1)
