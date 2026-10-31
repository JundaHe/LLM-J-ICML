# Stage 6 — LoRe under the new-rater protocol (points for accuracy; ×100 nats for LL)

| panel | label | k | LoRe own gain, acc | LoRe own − other, acc | LoRe − Dp, acc | LoRe own gain, LL×100 | LoRe − Dp, LL×100 | raters |
|---|---|---|---|---|---|---|---|---|
| LORE prism_pairs (folds [0, 1, 2, 3, 4]) | E2 | 5 | -4.84 [-5.74, -3.98] | +0.04 [-0.70, +0.82] | -4.60 [-5.74, -3.58] | -29.98 [-33.40, -26.83] | -31.28 [-34.96, -27.96] | 1018 |
| LORE prism_pairs (folds [0, 1, 2, 3, 4]) | E2 | 20 | -1.49 [-2.54, -0.43] | +0.17 [-0.79, +1.16] | -1.43 [-2.94, +0.12] | -7.24 [-10.78, -4.43] | -8.28 [-11.91, -5.42] | 669 |
| LORER prism_pairs (folds [0, 1, 2, 3, 4]) | E2 | 5 | -0.95 [-1.43, -0.48] | +0.11 [-0.29, +0.49] | -0.71 [-1.78, +0.28] | -2.55 [-3.31, -1.82] | -3.86 [-5.06, -2.73] | 1018 |
| LORER prism_pairs (folds [0, 1, 2, 3, 4]) | E2 | 20 | -0.47 [-1.15, +0.17] | +0.18 [-0.45, +0.80] | -0.41 [-1.76, +0.96] | -1.57 [-2.81, -0.32] | -2.61 [-4.15, -1.15] | 669 |
| LORE prism_pairs (folds [0]) | E1 | 5 | -4.42 [-6.16, -2.56] | -0.84 [-2.58, +0.89] | -4.69 [-7.11, -2.32] | -29.41 [-36.73, -22.96] | -35.70 [-44.30, -28.05] | 213 |
| LORE prism_pairs (folds [0]) | E1 | 20 | -2.83 [-5.24, -0.66] | -0.83 [-3.14, +1.19] | -2.94 [-6.73, +0.74] | -5.56 [-9.89, -1.62] | -10.76 [-16.67, -5.28] | 144 |
| LORER prism_pairs (folds [0]) | E1 | 5 | -2.20 [-3.68, -0.59] | -0.24 [-1.58, +1.18] | -2.47 [-4.87, -0.01] | -8.19 [-11.06, -5.56] | -14.48 [-19.52, -10.17] | 213 |
| LORER prism_pairs (folds [0]) | E1 | 20 | -2.83 [-5.24, -0.66] | -0.83 [-3.14, +1.19] | -2.94 [-6.73, +0.74] | -5.56 [-9.89, -1.62] | -10.76 [-16.67, -5.28] | 144 |

**Decision rule, LORE (PRISM pairs, binary, k = 20): max lower bound of own gain / own − other = -0.79 points → does not withdraw.**

**Decision rule, LORER (PRISM pairs, binary, k = 20): max lower bound of own gain / own − other = -0.45 points → does not withdraw.**

Selected LoRe hyper-parameters per run: E1_f0_lorer: B=20, lr=0.005, λ={'20': 10.0, '50': 10.0}; E1_f1_lorer: B=10, lr=0.005, λ={'20': 10.0, '50': 10.0}; E1_f2_lorer: B=5, lr=0.005, λ={'20': 10.0, '50': 100.0}; E1_f3_lorer: B=5, lr=0.005, λ={'20': 10.0, '50': 10.0}; E1_f4_lorer: B=20, lr=0.005, λ={'20': 1.0, '50': 1.0}; E2_f0_lorer: B=20, lr=0.005, λ={'20': 1.0, '50': 1.0}; E2_f1_lorer: B=10, lr=0.005, λ={'20': 10.0, '50': 10.0}; E2_f2_lorer: B=50, lr=0.005, λ={'20': 0.1, '50': 0.0}; E2_f3_lorer: B=5, lr=0.005, λ={'20': 1.0, '50': 0.1}; E2_f4_lorer: B=10, lr=0.005, λ={'20': 100.0, '50': 10.0}; prism_pairs_E1_f0_lore: B=2, lr=0.005; prism_pairs_E1_f0_lorer: B=2, lr=0.005, λ={'5': 1.0, '20': 0.0}; prism_pairs_E1_f1_lorer: B=10, lr=0.005, λ={'5': 10.0, '20': 10.0}; prism_pairs_E1_f2_lorer: B=5, lr=0.005, λ={'5': 100.0, '20': 100.0}; prism_pairs_E1_f3_lorer: B=50, lr=0.005, λ={'5': 10.0, '20': 10.0}; prism_pairs_E1_f4_lorer: B=50, lr=0.005, λ={'5': 0.1, '20': 0.1}; prism_pairs_E2_f0_lore: B=2, lr=0.005; prism_pairs_E2_f0_lorer: B=2, lr=0.005, λ={'5': 1.0, '20': 0.1}; prism_pairs_E2_f1_lore: B=50, lr=0.005; prism_pairs_E2_f1_lorer: B=50, lr=0.005, λ={'5': 1.0, '20': 1.0}; prism_pairs_E2_f2_lore: B=2, lr=0.005; prism_pairs_E2_f2_lorer: B=2, lr=0.005, λ={'5': 1.0, '20': 10.0}; prism_pairs_E2_f3_lore: B=5, lr=0.005; prism_pairs_E2_f3_lorer: B=5, lr=0.005, λ={'5': 10.0, '20': 1.0}; prism_pairs_E2_f4_lore: B=2, lr=0.005; prism_pairs_E2_f4_lorer: B=2, lr=0.005, λ={'5': 100.0, '20': 100.0}
