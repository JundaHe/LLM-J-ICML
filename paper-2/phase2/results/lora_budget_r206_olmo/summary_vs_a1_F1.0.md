# Fixed-budget LoRA block — summeval_coherence8 (analysis_budget_lora.py)

| design | rating budget | train items | cells | RPS | RPS − a1_F1.0 [95 % crossed bootstrap] |
|---|---|---|---|---|---|
| full_a7_F1 | 6720 | 960 | 9 | 0.1798 | -0.0063 [-0.0085, -0.0041] |
| a1_F1.0 | 960 | 960 | 9 | 0.1861 | +0.0000 [+0.0000, +0.0000] |
| a2_F1.0 | 1920 | 960 | 9 | 0.1775 | -0.0086 [-0.0117, -0.0056] |

Raw RPS against the held-out evaluator on the test items/groups; seeds 2003/2004/2005 × folds 0–2; bootstrap resamples the seed clusters and the test groups (B = 2000). Full-data reference = the a7_F1.0 design of the same batch.
