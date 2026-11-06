# Fixed-budget LoRA block — popquorn_off8 (analysis_budget_lora.py)

| design | rating budget | train items | cells | RPS | RPS − a1_F1.0 [95 % crossed bootstrap] |
|---|---|---|---|---|---|
| full_a7_F1 | 5733 | 819 | 9 | 0.1215 | -0.0063 [-0.0100, -0.0029] |
| a1_F1.0 | 819 | 819 | 9 | 0.1278 | +0.0000 [+0.0000, +0.0000] |
| a2_F1.0 | 1638 | 819 | 9 | 0.1247 | -0.0031 [-0.0062, -0.0002] |
| a7_F0.142857 | 819 | 117 | 9 | 0.1305 | +0.0027 [-0.0024, +0.0074] |

Raw RPS against the held-out evaluator on the test items/groups; seeds 2003/2004/2005 × folds 0–2; bootstrap resamples the seed clusters and the test groups (B = 2000). Full-data reference = the a7_F1.0 design of the same batch.
