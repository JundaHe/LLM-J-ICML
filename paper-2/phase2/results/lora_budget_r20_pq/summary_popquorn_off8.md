# Fixed-budget LoRA block — popquorn_off8 (analysis_budget_lora.py)

| design | rating budget | train items | cells | RPS | RPS − full_a7_F1 [95 % crossed bootstrap] |
|---|---|---|---|---|---|
| full_a7_F1 | 5733 | 819 | 9 | 0.1215 | +0.0000 [+0.0000, +0.0000] |
| a1_F1.0 | 819 | 819 | 9 | 0.1278 | +0.0063 [+0.0030, +0.0099] |
| a2_F1.0 | 1638 | 819 | 9 | 0.1247 | +0.0032 [+0.0016, +0.0048] |
| a7_F0.142857 | 819 | 117 | 9 | 0.1305 | +0.0090 [+0.0056, +0.0124] |

Raw RPS against the held-out evaluator on the test items/groups; seeds 2003/2004/2005 × folds 0–2; bootstrap resamples the seed clusters and the test groups (B = 2000). Full-data reference = the a7_F1.0 design of the same batch.
