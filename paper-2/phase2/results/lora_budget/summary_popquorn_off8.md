# Fixed-budget LoRA block — popquorn_off8 (analysis_budget_lora.py)

| design | rating budget | train items | cells | RPS | RPS − full chen [95 % crossed bootstrap] |
|---|---|---|---|---|---|
| full_a7_F1 | 5733 | 819 | 6 | 0.1217 | +0.0000 [+0.0000, +0.0000] |
| a1_F1.0 | 819 | 819 | 6 | 0.1294 | +0.0077 [+0.0046, +0.0110] |
| a2_F0.5 | 820 | 410 | 6 | 0.1339 | +0.0122 [+0.0083, +0.0167] |
| a2_F1.0 | 1638 | 819 | 6 | 0.1241 | +0.0024 [+0.0002, +0.0046] |
| a4_F0.25 | 820 | 205 | 6 | 0.1352 | +0.0135 [+0.0096, +0.0172] |
| a4_F0.5 | 1640 | 410 | 6 | 0.1282 | +0.0065 [+0.0036, +0.0097] |
| a7_F0.142857 | 819 | 117 | 6 | 0.1322 | +0.0105 [+0.0065, +0.0151] |
| a7_F0.285714 | 1638 | 234 | 6 | 0.1277 | +0.0061 [+0.0030, +0.0092] |

Raw RPS against the held-out evaluator on the test items/groups; seeds 2000/2001 × folds 0–2; bootstrap resamples the two seed clusters and the test groups (B = 2000). Full-data chen = the T3b/T3c runs restricted to the same seeds.
