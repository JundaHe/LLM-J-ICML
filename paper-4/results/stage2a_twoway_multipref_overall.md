# Two-way bootstrap (Stage 2 Amendment 9) — multipref_overall, k = 20, folds [0, 1, 2, 3, 4]

Raters and item clusters (prompt groups) resampled independently (pigeonhole bootstrap), B = 2,000. Per-rating differences are averaged over the 5 adaptation draws within each rating.

| contrast | metric | rerun point | primary point | rater-only 95 % | two-way 95 % |
|---|---|---|---|---|---|
| DF − D | LL per rating | +0.0802 | +0.0802 | [+0.0556, +0.1067] | [+0.0543, +0.1106] |
| DF − D | direction acc. | -0.0137 | -0.0137 | [-0.0204, -0.0070] | [-0.0243, -0.0016] |
| DFs − D | LL per rating | +0.0997 | +0.0997 | [+0.0738, +0.1272] | [+0.0710, +0.1298] |
| DFs − D | direction acc. | +0.0046 | +0.0046 | [+0.0013, +0.0080] | [-0.0014, +0.0110] |
| DG − D | LL per rating | -0.0003 | -0.0003 | [-0.0030, +0.0025] | [-0.0034, +0.0032] |
| DG − D | direction acc. | +0.0023 | +0.0023 | [-0.0005, +0.0053] | [-0.0028, +0.0076] |
| DF − DG | LL per rating | +0.0805 | +0.0805 | [+0.0560, +0.1056] | [+0.0534, +0.1081] |
| DF − DG | direction acc. | -0.0160 | -0.0160 | [-0.0223, -0.0095] | [-0.0271, -0.0049] |
| DFs − DG | LL per rating | +0.1000 | +0.1000 | [+0.0749, +0.1262] | [+0.0713, +0.1292] |
| DFs − DG | direction acc. | +0.0023 | +0.0023 | [-0.0017, +0.0062] | [-0.0043, +0.0088] |

n raters (fold-specific) = 209, item clusters = 4225. Reproduction check (Am. 9): |rerun − primary| ≤ 1e-3 for every row: True.
