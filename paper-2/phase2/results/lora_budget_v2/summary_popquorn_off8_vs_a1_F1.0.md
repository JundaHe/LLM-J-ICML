# Fixed-budget LoRA block — popquorn_off8 (analysis_budget_lora.py)

| design | rating budget | train items | cells | RPS | RPS − a1_F1.0 [95 % crossed bootstrap] |
|---|---|---|---|---|---|
| full_a7_F1 | 5733 | 819 | 9 | 0.1213 | -0.0087 [-0.0120, -0.0054] |
| a1_F1.0 | 819 | 819 | 9 | 0.1300 | +0.0000 [+0.0000, +0.0000] |
| a2_F1.0 | 1638 | 819 | 9 | 0.1246 | -0.0054 [-0.0084, -0.0027] |
| a7_F0.142857 | 819 | 117 | 9 | 0.1322 | +0.0022 [-0.0029, +0.0072] |

Raw RPS against the held-out evaluator on the test items/groups; seeds 2000/2001/2002 × folds 0–2; bootstrap resamples the seed clusters and the test groups (B = 2000). Full-data reference = the a7_F1.0 design of the same batch.
