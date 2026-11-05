# Fixed-budget LoRA block — summeval_coherence8 (analysis_budget_lora.py)

| design | rating budget | train items | cells | RPS | RPS − full_a7_F1 [95 % crossed bootstrap] |
|---|---|---|---|---|---|
| full_a7_F1 | 6720 | 960 | 9 | 0.1718 | +0.0000 [+0.0000, +0.0000] |
| a1_F1.0 | 960 | 960 | 9 | 0.1782 | +0.0064 [+0.0045, +0.0085] |
| a7_F0.142857 | 1008 | 144 | 9 | 0.1884 | +0.0166 [+0.0119, +0.0217] |

Raw RPS against the held-out evaluator on the test items/groups; seeds 2003/2004/2005 × folds 0–2; bootstrap resamples the seed clusters and the test groups (B = 2000). Full-data reference = the a7_F1.0 design of the same batch.
