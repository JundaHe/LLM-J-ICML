# Fixed-budget LoRA block — summeval_coherence8 (analysis_budget_lora.py)

| design | rating budget | train items | cells | RPS | RPS − a1_F1.0 [95 % crossed bootstrap] |
|---|---|---|---|---|---|
| full_a7_F1 | 6720 | 960 | 9 | 0.1691 | +0.0027 [-0.0014, +0.0063] |
| a1_F1.0 | 960 | 960 | 9 | 0.1664 | +0.0000 [+0.0000, +0.0000] |
| a2_F0.5 | 960 | 480 | 9 | 0.1651 | -0.0013 [-0.0073, +0.0039] |
| a7_F0.142857 | 1008 | 144 | 9 | 0.1897 | +0.0233 [+0.0176, +0.0285] |

Raw RPS against the held-out evaluator on the test items/groups; seeds 2000/2001/2002 × folds 0–2; bootstrap resamples the seed clusters and the test groups (B = 2000). Full-data reference = the a7_F1.0 design of the same batch.
