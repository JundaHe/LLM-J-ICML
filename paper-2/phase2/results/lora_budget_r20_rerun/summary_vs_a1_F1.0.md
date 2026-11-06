# Fixed-budget LoRA block — summeval_coherence8 (analysis_budget_lora.py)

| design | rating budget | train items | cells | RPS | RPS − a1_F1.0 [95 % crossed bootstrap] |
|---|---|---|---|---|---|
| full_a7_F1 | 6720 | 960 | 9 | 0.1713 | -0.0064 [-0.0083, -0.0043] |
| a1_F1.0 | 960 | 960 | 9 | 0.1777 | +0.0000 [+0.0000, +0.0000] |
| a2_F1.0 | 1920 | 960 | 9 | 0.1679 | -0.0098 [-0.0132, -0.0066] |

Raw RPS against the held-out evaluator on the test items/groups; seeds 2003/2004/2005 × folds 0–2; bootstrap resamples the seed clusters and the test groups (B = 2000). Full-data reference = the a7_F1.0 design of the same batch.
