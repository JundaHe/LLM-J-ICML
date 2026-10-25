# Fixed-budget LoRA block — SummEval coherence (analysis_budget_lora.py)

| design | rating budget | train items | cells | RPS | RPS − full chen [95 % crossed bootstrap] |
|---|---|---|---|---|---|
| full_a7_F1 | 6720 | 960 | 6 | 0.1701 | +0.0000 [+0.0000, +0.0000] |
| a1_F1.0 | 960 | 960 | 6 | 0.1640 | -0.0061 [-0.0087, -0.0035] |
| a2_F0.5 | 960 | 480 | 6 | 0.1648 | -0.0052 [-0.0091, -0.0014] |
| a2_F1.0 | 1920 | 960 | 6 | 0.1637 | -0.0064 [-0.0106, -0.0031] |
| a4_F0.25 | 960 | 240 | 6 | 0.1862 | +0.0162 [+0.0116, +0.0204] |
| a4_F0.5 | 1920 | 480 | 6 | 0.1678 | -0.0023 [-0.0047, +0.0003] |
| a7_F0.142857 | 1008 | 144 | 6 | 0.1912 | +0.0211 [+0.0168, +0.0253] |
| a7_F0.285714 | 1904 | 272 | 6 | 0.1813 | +0.0112 [+0.0071, +0.0155] |

Raw RPS against the held-out expert on the 30 test documents (480 summaries); seeds 2000/2001 × folds 0–2; bootstrap resamples the two seed clusters and the test documents (B = 2000). Full-data chen = T3b runs restricted to the same seeds.
