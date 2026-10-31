"""Stage 8 learner-free statistic (PROTOCOL_STAGE8.md): on Community Alignment first-turn pairs, response pairs (same prompt, identical response texts) that
occur for at least two annotators; rate at which two annotators choose the same response (all annotator pairs within a response pair, pairs weighted equally),
item bootstrap (B = 2,000, seed 31). Writes results/stage8_agree.json; the text-only model's accuracy on the same pairs is added by s8.py."""
import os, sys, json, collections, itertools, numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(HERE), "paper-2", "phase2"))
import data_panels
P = data_panels.load("ca_pairs"); by = collections.defaultdict(list)
for j, (p, a, b, y, e) in enumerate(zip(P["texts"], P["resp_A"], P["resp_B"], P["yb"], P["evaluators"])):
    x, z = sorted([a, b]); ch = b if y == 1 else a; by[(p, x, z)].append((e[0], ch == x, j))
items = [(k, v) for k, v in by.items() if len({u for u, _, _ in v}) >= 2]
agr = np.array([np.mean([c1 == c2 for (u1, c1, _), (u2, c2, _) in itertools.combinations(v, 2) if u1 != u2]) for _, v in items])
rng = np.random.RandomState(31); bs = [agr[rng.randint(0, len(agr), len(agr))].mean() for _ in range(2000)]
out = {"n_pairs_multi": len(items), "n_ratings": int(sum(len(v) for _, v in items)), "agreement": float(agr.mean()), "ci": [float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
       "rows": [j for _, v in items for _, _, j in v]}
json.dump(out, open(f"{HERE}/results/stage8_agree.json", "w")); print({k: v for k, v in out.items() if k != "rows"})
