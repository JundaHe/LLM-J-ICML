# Fixed-budget LoRA block — summeval_coherence8 (analysis_budget_lora.py)

| design | rating budget | train items | cells | RPS | RPS − full chen [95 % crossed bootstrap] |
|---|---|---|---|---|---|
| full_a7_F1 | 6720 | 960 | 3 | 0.1687 | +0.0000 [+0.0000, +0.0000] |
| a1_F1.0 | 960 | 960 | 3 | 0.1652 | -0.0035 [-0.0052, -0.0012] |
| a2_F0.5 | 960 | 480 | 3 | 0.1648 | -0.0038 [-0.0076, +0.0001] |
| a7_F0.142857 | 1008 | 144 | 3 | 0.1896 | +0.0209 [+0.0171, +0.0247] |

Raw RPS against the held-out evaluator on the test items/groups; seeds 2000 × folds 0–2; bootstrap resamples the seed clusters and the test groups (B = 200). Full-data reference = the a7_F1.0 design of the same batch.
