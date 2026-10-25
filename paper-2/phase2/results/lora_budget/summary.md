# Fixed-budget LoRA block — SummEval coherence (analysis_budget_lora.py)

| design | rating budget | train items | cells | RPS | RPS − full chen [95 % crossed bootstrap] |
|---|---|---|---|---|---|
| full_a7_F1 | 6720 | 960 | 6 | 0.1701 | +0.0000 [+0.0000, +0.0000] |
| a1_F1.0 | 960 | 960 | 6 | 0.1640 | -0.0061 [-0.0085, -0.0035] |
| a2_F0.5 | 960 | 480 | 6 | 0.1648 | -0.0052 [-0.0088, -0.0015] |
| a4_F0.25 | 960 | 240 | 6 | 0.1862 | +0.0162 [+0.0119, +0.0205] |
| a7_F0.142857 | 1008 | 144 | 4 | 0.1950 | +0.0250 [+0.0186, +0.0321] |

Raw RPS against the held-out expert on the 30 test documents (480 summaries); seeds 2000/2001 × folds 0–2; bootstrap resamples the two seed clusters and the test documents (B = 500). Full-data chen = T3b runs restricted to the same seeds.
