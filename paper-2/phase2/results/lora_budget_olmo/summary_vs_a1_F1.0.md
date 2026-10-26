# Fixed-budget LoRA block — summeval_coherence8 (analysis_budget_lora.py)

| design | rating budget | train items | cells | RPS | RPS − a1_F1.0 [95 % crossed bootstrap] |
|---|---|---|---|---|---|
| full_a7_F1 | 6720 | 960 | 6 | 0.1794 | -0.0007 [-0.0070, +0.0057] |
| a1_F1.0 | 960 | 960 | 6 | 0.1801 | +0.0000 [+0.0000, +0.0000] |
| a2_F0.5 | 960 | 480 | 6 | 0.1778 | -0.0024 [-0.0075, +0.0028] |
| a7_F0.142857 | 1008 | 144 | 6 | 0.1896 | +0.0095 [+0.0022, +0.0160] |

Raw RPS against the held-out evaluator on the test items/groups; seeds 2000/2001 × folds 0–2; bootstrap resamples the seed clusters and the test groups (B = 2000). Full-data reference = the a7_F1.0 design of the same batch.
