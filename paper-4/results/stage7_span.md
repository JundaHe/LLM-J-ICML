# Stage 7 S7-2 — injected g2 inside (x) vs outside (t) DL's input space (direction accuracy, points; 95 % rater bootstrap)

| panel | g2 in DL's input | oracle gain | DL own − other, k = 20 | DL own − other, k = 50 | reference own − population, k = 20 (est. base) | reference own − other, k = 20 (est. base) |
|---|---|---|---|---|---|---|
| t5 | no (R² 0.02) | +5.2 | -0.02 [-0.28, +0.26] | -0.08 [-0.42, +0.23] | +3.13 [+2.30, +3.97] | +5.34 [+4.48, +6.27] |
| x5 | yes | +5.1 | +0.08 [-0.18, +0.33] | +0.03 [-0.29, +0.34] | +2.67 [+1.88, +3.45] | +4.39 [+3.70, +5.10] |
| t10 | no (R² 0.02) | +10.1 | +0.09 [-0.18, +0.36] | +0.02 [-0.30, +0.35] | +7.96 [+6.42, +9.43] | +12.75 [+11.35, +14.20] |
| x10 | yes | +10.4 | +1.97 [+1.31, +2.65] | +7.02 [+5.84, +8.16] | +8.33 [+6.79, +9.88] | +11.72 [+10.29, +13.20] |

Detection (lower bound > +1 point, k = 20) by DL: t5 no, x5 no, t10 no, x10 yes.
