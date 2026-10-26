# Fixed-budget LoRA block — summeval_coherence8 (analysis_budget_lora.py)

| design | rating budget | train items | cells | RPS | RPS − full chen [95 % crossed bootstrap] |
|---|---|---|---|---|---|
| full_a7_F1 | 6720 | 960 | 6 | 0.1794 | +0.0000 [+0.0000, +0.0000] |
| a1_F1.0 | 960 | 960 | 6 | 0.1801 | +0.0007 [-0.0054, +0.0068] |
| a2_F0.5 | 960 | 480 | 2 | 0.1552 | -0.0242 [-0.0373, -0.0097] |

Raw RPS against the held-out evaluator on the test items/groups; seeds 2000/2001 × folds 0–2; bootstrap resamples the two seed clusters and the test groups (B = 500). Full-data chen = the T3b/T3c runs restricted to the same seeds.
