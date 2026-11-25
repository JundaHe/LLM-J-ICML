# Stage 15 S15-3 — two-way intervals and multiplicity for the corrected real-panel contrasts (post hoc; rung a; k = 20, Dorn k = 10; ×100 nats or points per rating)

Reproduction of the Stage 14 rung-a points by the rerun (family A, |difference| ≤ 1e-3 per rating): False (max 2.27e-03, 24 contrasts; 22 within tolerance). Not reproduced: ['prism: LL L − F (-1.81 → -1.58)', 'prism: direction L own − other (+2.68 → +2.50)']. Panels: {'multipref_overall': {'k': 20, 'folds': [0, 1, 2, 3, 4], 'n_raters': 209, 'n_clusters': 4225, 'n_pairs': 163399}, 'dices': {'k': 20, 'folds': [0, 1, 2, 3, 4], 'n_raters': 104, 'n_clusters': 350, 'n_pairs': 112980}, 'prism': {'k': 20, 'folds': [0, 1, 2, 3, 4], 'n_raters': 941, 'n_clusters': 1473, 'n_pairs': 72758}, 'dorn_raters': {'k': 10, 'folds': [0, 1, 2, 3, 4], 'n_raters': 3393, 'n_clusters': 360, 'n_pairs': 17044}}

Reading rule of §2.4 with the two-way intervals: {'multipref_overall': {'DFL': 'no interaction beyond the offsets', 'DL': 'shift', 'FL': 'no interaction beyond the offsets', 'L': 'shift + interaction'}, 'dices': {'DFL': 'inconclusive', 'DL': 'shift', 'FL': 'inconclusive', 'L': 'neither rule met'}, 'prism': {'DFL': 'no interaction beyond the offsets', 'DL': 'shift', 'FL': 'no interaction beyond the offsets', 'L': 'shift + interaction'}, 'dorn_raters': {'DFL': 'no interaction beyond the offsets', 'DL': 'neither rule met', 'FL': 'no interaction beyond the offsets', 'L': 'shift'}}

| panel | family | contrast | point | Stage 14 point | rater-only 95 % | two-way 95 % | p (two-way, normal) | Holm in family | Holm over A ∪ B | nominal | after Holm (family / union) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| multipref_overall | A | LL DL − DFs | +0.05 | +0.05 | [-0.46, +0.51] | [-0.59, +0.66] | 0.8782 | 1.0000 | 1.0000 | no | no / no |
| multipref_overall | A | direction DL own − other | +0.19 | +0.19 | [-0.12, +0.51] | [-0.38, +0.75] | 0.5072 | 1.0000 | 1.0000 | no | no / no |
| multipref_overall | A | concordance DL own − other | +0.13 | +0.13 | [-0.01, +0.28] | [-0.13, +0.42] | 0.3483 | 1.0000 | 1.0000 | no | no / no |
| multipref_overall | B | LL DFL − DF | -0.11 | — | [-0.19, -0.03] | [-0.25, +0.02] | 0.1063 | 1.0000 | 1.0000 | no | no / no |
| multipref_overall | B | LL DFL own − other latent | +0.02 | — | [-0.08, +0.11] | [-0.14, +0.17] | 0.8181 | 1.0000 | 1.0000 | no | no / no |
| multipref_overall | B | concordance DFL own − other latent | +0.06 | — | [-0.05, +0.15] | [-0.13, +0.24] | 0.5503 | 1.0000 | 1.0000 | no | no / no |
| multipref_overall | – | LL DL own − (other's interaction) | +0.01 | — | [-0.00, +0.03] | [-0.01, +0.04] | 0.3392 | — | — | no | — |
| multipref_overall | – | LL DL own − (other's shift) | +18.10 | — | [+14.66, +21.82] | [+14.54, +22.22] | 0.0000 | — | — | yes | — |
| multipref_overall | – | concordance DL own − (other's interaction) | +0.01 | — | [-0.01, +0.02] | [-0.03, +0.05] | 0.7643 | — | — | no | — |
| multipref_overall | A | LL L − F | -3.05 | -3.05 | [-4.87, -1.51] | [-4.98, -1.30] | 0.0012 | 0.0202 | 0.0486 | yes | yes / yes |
| multipref_overall | A | direction L own − other | -0.12 | -0.12 | [-0.44, +0.22] | [-0.73, +0.45] | 0.6993 | 1.0000 | 1.0000 | no | no / no |
| multipref_overall | A | concordance L own − other | -0.01 | -0.01 | [-0.04, +0.02] | [-0.07, +0.05] | 0.7529 | 1.0000 | 1.0000 | no | no / no |
| multipref_overall | B | LL FL − F | +0.17 | — | [+0.02, +0.33] | [-0.03, +0.39] | 0.1078 | 1.0000 | 1.0000 | no | no / no |
| multipref_overall | B | LL FL own − other latent | +0.30 | — | [+0.14, +0.48] | [+0.09, +0.54] | 0.0097 | 0.2233 | 0.3690 | yes | no / no |
| multipref_overall | B | concordance FL own − other latent | +0.04 | — | [-0.06, +0.13] | [-0.17, +0.26] | 0.7056 | 1.0000 | 1.0000 | no | no / no |
| multipref_overall | – | LL L own − (other's interaction) | +0.06 | — | [+0.03, +0.09] | [+0.02, +0.10] | 0.0034 | — | — | yes | — |
| multipref_overall | – | LL L own − (other's shift) | +0.44 | — | [+0.26, +0.65] | [+0.16, +0.77] | 0.0040 | — | — | yes | — |
| multipref_overall | – | concordance L own − (other's interaction) | -0.01 | — | [-0.04, +0.02] | [-0.07, +0.05] | 0.7529 | — | — | no | — |
| dices | A | LL DL − DF | -1.11 | -1.11 | [-1.83, -0.44] | [-2.06, -0.29] | 0.0150 | 0.2251 | 0.5553 | yes | no / no |
| dices | A | direction DL own − other | +9.44 | +9.44 | [+7.36, +11.65] | [+6.93, +11.97] | 0.0000 | 0.0000 | 0.0000 | yes | yes / yes |
| dices | A | concordance DL own − other | +0.06 | +0.06 | [-0.12, +0.26] | [-0.25, +0.36] | 0.7043 | 1.0000 | 1.0000 | no | no / no |
| dices | B | LL DFL − DF | -0.05 | — | [-0.30, +0.22] | [-0.64, +0.54] | 0.8752 | 1.0000 | 1.0000 | no | no / no |
| dices | B | LL DFL own − other latent | +0.41 | — | [+0.16, +0.68] | [+0.08, +0.77] | 0.0220 | 0.4843 | 0.7926 | yes | no / no |
| dices | B | concordance DFL own − other latent | +0.68 | — | [+0.24, +1.18] | [+0.02, +1.43] | 0.0544 | 1.0000 | 1.0000 | yes | no / no |
| dices | – | LL DL own − (other's interaction) | +0.13 | — | [+0.01, +0.26] | [-0.03, +0.30] | 0.1358 | — | — | no | — |
| dices | – | LL DL own − (other's shift) | +27.23 | — | [+22.58, +32.16] | [+22.24, +32.95] | 0.0000 | — | — | yes | — |
| dices | – | concordance DL own − (other's interaction) | +0.05 | — | [-0.11, +0.23] | [-0.21, +0.32] | 0.7120 | — | — | no | — |
| dices | A | LL L − F | -0.19 | -0.19 | [-1.02, +0.61] | [-1.38, +0.97] | 0.7501 | 1.0000 | 1.0000 | no | no / no |
| dices | A | direction L own − other | +10.01 | +10.01 | [+7.96, +12.14] | [+7.54, +12.52] | 0.0000 | 0.0000 | 0.0000 | yes | yes / yes |
| dices | A | concordance L own − other | +0.50 | +0.50 | [+0.10, +0.97] | [-0.06, +1.21] | 0.1241 | 1.0000 | 1.0000 | no | no / no |
| dices | B | LL FL − F | -0.23 | — | [-0.56, +0.07] | [-0.67, +0.15] | 0.2706 | 1.0000 | 1.0000 | no | no / no |
| dices | B | LL FL own − other latent | +0.29 | — | [-0.01, +0.61] | [-0.08, +0.67] | 0.1448 | 1.0000 | 1.0000 | no | no / no |
| dices | B | concordance FL own − other latent | +0.47 | — | [+0.16, +0.84] | [+0.03, +1.02] | 0.0610 | 1.0000 | 1.0000 | yes | no / no |
| dices | – | LL L own − (other's interaction) | +0.39 | — | [+0.06, +0.78] | [-0.05, +0.87] | 0.1019 | — | — | no | — |
| dices | – | LL L own − (other's shift) | +18.98 | — | [+15.56, +22.57] | [+15.21, +23.03] | 0.0000 | — | — | yes | — |
| dices | – | concordance L own − (other's interaction) | +0.50 | — | [+0.10, +0.97] | [-0.06, +1.21] | 0.1241 | — | — | no | — |
| prism | A | LL DL − DF | +0.37 | +0.37 | [+0.10, +0.65] | [-0.11, +0.83] | 0.1211 | 1.0000 | 1.0000 | no | no / no |
| prism | A | direction DL own − other | +1.59 | +1.59 | [+1.14, +2.07] | [+0.84, +2.40] | 0.0001 | 0.0012 | 0.0028 | yes | yes / yes |
| prism | A | concordance DL own − other | -0.06 | -0.06 | [-0.26, +0.13] | [-0.51, +0.38] | 0.7720 | 1.0000 | 1.0000 | no | no / no |
| prism | B | LL DFL − DF | -0.07 | — | [-0.13, -0.01] | [-0.18, +0.03] | 0.1611 | 1.0000 | 1.0000 | no | no / no |
| prism | B | LL DFL own − other latent | -0.01 | — | [-0.07, +0.06] | [-0.12, +0.11] | 0.8554 | 1.0000 | 1.0000 | no | no / no |
| prism | B | concordance DFL own − other latent | -0.06 | — | [-0.15, +0.03] | [-0.25, +0.11] | 0.5112 | 1.0000 | 1.0000 | no | no / no |
| prism | – | LL DL own − (other's interaction) | +0.03 | — | [+0.00, +0.07] | [-0.02, +0.09] | 0.2353 | — | — | no | — |
| prism | – | LL DL own − (other's shift) | +17.14 | — | [+15.83, +18.43] | [+14.91, +19.28] | 0.0000 | — | — | yes | — |
| prism | – | concordance DL own − (other's interaction) | +0.02 | — | [-0.04, +0.07] | [-0.11, +0.13] | 0.7728 | — | — | no | — |
| prism | A | LL L − F | -1.58 | -1.81 | [-2.26, -0.90] | [-2.72, -0.51] | 0.0047 | 0.0758 | 0.1894 | yes | no / no |
| prism | A | direction L own − other | +2.50 | +2.68 | [+1.94, +3.09] | [+1.55, +3.52] | 0.0000 | 0.0000 | 0.0000 | yes | yes / yes |
| prism | A | concordance L own − other | +0.01 | +0.01 | [-0.05, +0.06] | [-0.10, +0.12] | 0.8443 | 1.0000 | 1.0000 | no | no / no |
| prism | B | LL FL − F | +0.08 | — | [-0.09, +0.25] | [-0.22, +0.37] | 0.5938 | 1.0000 | 1.0000 | no | no / no |
| prism | B | LL FL own − other latent | +0.47 | — | [+0.27, +0.67] | [+0.14, +0.80] | 0.0071 | 0.1699 | 0.2761 | yes | no / no |
| prism | B | concordance FL own − other latent | +0.26 | — | [+0.08, +0.42] | [-0.14, +0.64] | 0.1864 | 1.0000 | 1.0000 | no | no / no |
| prism | – | LL L own − (other's interaction) | +0.08 | — | [+0.03, +0.14] | [+0.00, +0.18] | 0.0569 | — | — | yes | — |
| prism | – | LL L own − (other's shift) | +12.45 | — | [+11.15, +13.74] | [+10.27, +14.57] | 0.0000 | — | — | yes | — |
| prism | – | concordance L own − (other's interaction) | +0.01 | — | [-0.05, +0.06] | [-0.10, +0.12] | 0.8462 | — | — | no | — |
| dorn_raters | A | LL DL − DF | -3.99 | -3.99 | [-4.96, -3.11] | [-5.62, -2.35] | 0.0000 | 0.0000 | 0.0000 | yes | yes / yes |
| dorn_raters | A | direction DL own − other | +0.00 | +0.00 | [+0.00, +0.00] | [+0.00, +0.00] | 1.0000 | 1.0000 | 1.0000 | no | no / no |
| dorn_raters | A | concordance DL own − other | +0.00 | +0.00 | [+0.00, +0.00] | [+0.00, +0.00] | 1.0000 | 1.0000 | 1.0000 | no | no / no |
| dorn_raters | B | LL DFL − DF | +0.00 | — | [-0.04, +0.05] | [-0.07, +0.08] | 0.9161 | 1.0000 | 1.0000 | no | no / no |
| dorn_raters | B | LL DFL own − other latent | +0.03 | — | [-0.02, +0.07] | [-0.05, +0.11] | 0.5181 | 1.0000 | 1.0000 | no | no / no |
| dorn_raters | B | concordance DFL own − other latent | +0.22 | — | [+0.07, +0.37] | [-0.14, +0.69] | 0.2813 | 1.0000 | 1.0000 | no | no / no |
| dorn_raters | – | LL DL own − (other's interaction) | -0.00 | — | [-0.00, +0.00] | [-0.00, +0.00] | 1.0000 | — | — | no | — |
| dorn_raters | – | LL DL own − (other's shift) | +0.00 | — | [+0.00, +0.00] | [-0.00, +0.00] | 1.0000 | — | — | no | — |
| dorn_raters | – | concordance DL own − (other's interaction) | +0.00 | — | [+0.00, +0.00] | [+0.00, +0.00] | 1.0000 | — | — | no | — |
| dorn_raters | A | LL L − F | +3.74 | +3.74 | [+2.78, +4.65] | [+2.04, +5.49] | 0.0000 | 0.0006 | 0.0014 | yes | yes / yes |
| dorn_raters | A | direction L own − other | +11.24 | +11.24 | [+10.35, +12.16] | [+9.66, +12.81] | 0.0000 | 0.0000 | 0.0000 | yes | yes / yes |
| dorn_raters | A | concordance L own − other | +0.00 | +0.00 | [+0.00, +0.00] | [+0.00, +0.00] | 1.0000 | 1.0000 | 1.0000 | no | no / no |
| dorn_raters | B | LL FL − F | -0.03 | — | [-0.10, +0.05] | [-0.18, +0.13] | 0.7371 | 1.0000 | 1.0000 | no | no / no |
| dorn_raters | B | LL FL own − other latent | -0.01 | — | [-0.09, +0.07] | [-0.17, +0.15] | 0.8515 | 1.0000 | 1.0000 | no | no / no |
| dorn_raters | B | concordance FL own − other latent | -0.22 | — | [-0.44, -0.01] | [-0.90, +0.40] | 0.4890 | 1.0000 | 1.0000 | no | no / no |
| dorn_raters | – | LL L own − (other's interaction) | +0.00 | — | [+0.00, +0.00] | [-0.00, +0.00] | 0.2072 | — | — | no | — |
| dorn_raters | – | LL L own − (other's shift) | +21.14 | — | [+19.84, +22.53] | [+19.04, +23.34] | 0.0000 | — | — | yes | — |
| dorn_raters | – | concordance L own − (other's interaction) | +0.00 | — | [+0.00, +0.00] | [+0.00, +0.00] | 1.0000 | — | — | no | — |

Family A: 24 contrasts; nominal (two-way interval excludes 0) 10; Holm within family 8; Holm over the union 8.

Family B: 24 contrasts; nominal (two-way interval excludes 0) 5; Holm within family 0; Holm over the union 0.
