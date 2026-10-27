# Fixed-budget LoRA block — popquorn_off8 (analysis_budget_lora.py)

| design | rating budget | train items | cells | RPS | RPS − full_a7_F1 [95 % crossed bootstrap] |
|---|---|---|---|---|---|
| full_a7_F1 | 5733 | 819 | 9 | 0.1213 | +0.0000 [+0.0000, +0.0000] |
| a1_F1.0 | 819 | 819 | 9 | 0.1300 | +0.0087 [+0.0054, +0.0122] |
| a2_F1.0 | 1638 | 819 | 9 | 0.1246 | +0.0033 [+0.0011, +0.0053] |
| a7_F0.142857 | 819 | 117 | 9 | 0.1322 | +0.0109 [+0.0070, +0.0151] |

Raw RPS against the held-out evaluator on the test items/groups; seeds 2000/2001/2002 × folds 0–2; bootstrap resamples the seed clusters and the test groups (B = 2000). Full-data reference = the a7_F1.0 design of the same batch.
