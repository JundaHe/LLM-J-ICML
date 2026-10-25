# Fixed-budget LoRA block — popquorn_off8 (analysis_budget_lora.py)

| design | rating budget | train items | cells | RPS | RPS − full chen [95 % crossed bootstrap] |
|---|---|---|---|---|---|
| full_a7_F1 | 5733 | 819 | 6 | 0.1217 | +0.0000 [+0.0000, +0.0000] |
| a1_F1.0 | 819 | 819 | 6 | 0.1294 | +0.0077 [+0.0046, +0.0111] |
| a2_F0.5 | 820 | 410 | 6 | 0.1339 | +0.0122 [+0.0083, +0.0166] |
| a4_F0.25 | 820 | 205 | 6 | 0.1352 | +0.0135 [+0.0099, +0.0171] |
| a7_F0.142857 | 819 | 117 | 1 | 0.1309 | +0.0093 [+nan, +nan] |

Raw RPS against the held-out evaluator on the test items/groups; seeds 2000/2001 × folds 0–2; bootstrap resamples the two seed clusters and the test groups (B = 300). Full-data chen = the T3b/T3c runs restricted to the same seeds.
