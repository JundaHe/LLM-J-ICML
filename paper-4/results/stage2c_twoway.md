# Two-way bootstrap (Stage 2c Amendment 5) — MultiPref, k = 20

Raters and prompt groups resampled independently, B = 2,000; per-rating values averaged over the 5 adaptation draws. Own gain = the same method at k = 20 minus k = 0 on the same ratings.

## E1 (graded)

| quantity | metric | rerun point | primary point | rater-only 95 % | two-way 95 % |
|---|---|---|---|---|---|
| DFsp − VPL | LL per rating | +0.0920 | +0.0920 | [+0.0671, +0.1204] | [+0.0625, +0.1241] |
| DFsp − VPL | direction acc. | -0.0093 | -0.0094 | [-0.0188, +0.0002] | [-0.0267, +0.0079] |
| DFsp − PAL2 | LL per rating | +0.1584 | +0.1584 | [+0.1310, +0.1881] | [+0.1254, +0.1936] |
| DFsp − PAL2 | direction acc. | +0.0020 | +0.0019 | [-0.0077, +0.0122] | [-0.0162, +0.0201] |
| DFsp − Dp | LL per rating | +0.0940 | +0.0940 | [+0.0695, +0.1206] | [+0.0674, +0.1250] |
| DFsp − Dp | direction acc. | -0.0020 | -0.0021 | [-0.0058, +0.0016] | [-0.0082, +0.0044] |
| VPL − Dp | LL per rating | +0.0020 | +0.0020 | [-0.0084, +0.0123] | [-0.0141, +0.0183] |
| VPL − Dp | direction acc. | +0.0073 | +0.0073 | [-0.0020, +0.0173] | [-0.0095, +0.0250] |
| own gain DFp | LL per rating | +0.0803 | +0.0803 | [+0.0573, +0.1036] | [+0.0542, +0.1057] |
| own gain DFp | direction acc. | -0.0070 | -0.0075 | [-0.0126, -0.0012] | [-0.0166, +0.0030] |
| own gain DFsp | LL per rating | +0.0974 | +0.0974 | [+0.0707, +0.1262] | [+0.0665, +0.1292] |
| own gain DFsp | direction acc. | -0.0007 | -0.0010 | [-0.0042, +0.0026] | [-0.0069, +0.0054] |
| own gain VPL | LL per rating | +0.0873 | +0.0873 | [+0.0695, +0.1062] | [+0.0641, +0.1131] |
| own gain VPL | direction acc. | +0.0007 | +0.0007 | [-0.0032, +0.0046] | [-0.0057, +0.0074] |
| own gain PAL2 | LL per rating | -0.0002 | -0.0002 | [-0.0019, +0.0016] | [-0.0033, +0.0028] |
| own gain PAL2 | direction acc. | -0.0048 | -0.0048 | [-0.0091, -0.0009] | [-0.0111, +0.0014] |
| own gain PAL4 | LL per rating | +0.0015 | +0.0015 | [-0.0019, +0.0052] | [-0.0032, +0.0068] |
| own gain PAL4 | direction acc. | -0.0021 | -0.0021 | [-0.0069, +0.0026] | [-0.0096, +0.0054] |

Reproduction check: |rerun − primary| ≤ 1e-3 for every E1 row: True.

## E2 (binary)

| quantity | metric | rerun point | primary point | rater-only 95 % | two-way 95 % |
|---|---|---|---|---|---|
| DFsp − VPL | LL per rating | -0.0100 | -0.0100 | [-0.0168, -0.0034] | [-0.0218, +0.0016] |
| DFsp − VPL | binary acc. | -0.0094 | -0.0094 | [-0.0194, -0.0001] | [-0.0281, +0.0098] |
| DFsp − PAL2 | LL per rating | +0.0020 | +0.0020 | [-0.0064, +0.0104] | [-0.0125, +0.0169] |
| DFsp − PAL2 | binary acc. | +0.0038 | +0.0039 | [-0.0062, +0.0146] | [-0.0163, +0.0242] |
| DFsp − Dp | LL per rating | -0.0052 | -0.0052 | [-0.0095, -0.0016] | [-0.0117, +0.0004] |
| DFsp − Dp | binary acc. | -0.0002 | -0.0002 | [-0.0059, +0.0054] | [-0.0101, +0.0098] |
| VPL − Dp | LL per rating | +0.0048 | +0.0048 | [-0.0018, +0.0116] | [-0.0075, +0.0160] |
| VPL − Dp | binary acc. | +0.0092 | +0.0092 | [-0.0015, +0.0201] | [-0.0098, +0.0292] |
| own gain DFp | LL per rating | +0.0003 | +0.0003 | [-0.0012, +0.0019] | [-0.0024, +0.0030] |
| own gain DFp | binary acc. | -0.0019 | -0.0029 | [-0.0064, +0.0029] | [-0.0099, +0.0063] |
| own gain DFsp | LL per rating | +0.0002 | +0.0002 | [-0.0005, +0.0009] | [-0.0010, +0.0014] |
| own gain DFsp | binary acc. | +0.0004 | +0.0001 | [-0.0012, +0.0022] | [-0.0028, +0.0038] |
| own gain VPL | LL per rating | +0.0010 | +0.0010 | [-0.0004, +0.0026] | [-0.0010, +0.0034] |
| own gain VPL | binary acc. | +0.0004 | +0.0004 | [-0.0014, +0.0022] | [-0.0029, +0.0039] |
| own gain PAL2 | LL per rating | -0.0004 | -0.0004 | [-0.0015, +0.0006] | [-0.0021, +0.0011] |
| own gain PAL2 | binary acc. | -0.0014 | -0.0014 | [-0.0036, +0.0008] | [-0.0056, +0.0028] |
| own gain PAL4 | LL per rating | +0.0021 | +0.0021 | [+0.0000, +0.0044] | [-0.0012, +0.0061] |
| own gain PAL4 | binary acc. | -0.0009 | -0.0009 | [-0.0044, +0.0023] | [-0.0066, +0.0044] |

Reproduction check: |rerun − primary| ≤ 1e-3 for every E2 row: False.


**Note (Am. 5 reproduction rule).** E1 reproduces (all rows within 5e-4). E2 fails by one row: the 5-offset model's own binary-accuracy gain, −0.0019 in the rerun vs −0.0029 in the primary run (difference 0.0010; float32 L-BFGS adaptation noise flips a few near-0.5 predictions — Dp, VPL and PAL reproduce exactly). Per the rule the E2 rerun is not used as evidence; it is shown here descriptively, and the paper only uses it to weaken (not to strengthen) the binary-label comparisons. Paper use of E1: DFsp − VPL LL interval and the ranking-null upper bounds (all own direction-accuracy gains < +0.0074 under the two-way bootstrap).
