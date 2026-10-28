# Two-way bootstrap (Stage 2 Amendment 9) — multipref_overall, k = 20, folds [0, 1, 2, 3, 4]

Raters and item clusters (prompt groups) resampled independently (pigeonhole bootstrap), B = 2,000. Per-rating differences are averaged over the 5 adaptation draws within each rating.

| contrast | metric | rerun point | primary point | rater-only 95 % | two-way 95 % |
|---|---|---|---|---|---|
| DF − D | LL per rating | +0.0802 | +0.0802 | [+0.0556, +0.1067] | [+0.0543, +0.1106] |
| DF − D | direction acc. | -0.0137 | -0.0137 | [-0.0204, -0.0070] | [-0.0243, -0.0016] |
| DFs − D | LL per rating | +0.0997 | +0.0997 | [+0.0738, +0.1272] | [+0.0710, +0.1298] |
| DFs − D | direction acc. | +0.0046 | +0.0046 | [+0.0013, +0.0080] | [-0.0014, +0.0110] |
| DL − D | LL per rating | +0.0952 | +0.0952 | [+0.0691, +0.1211] | [+0.0651, +0.1250] |
| DL − D | direction acc. | +0.0047 | +0.0047 | [+0.0008, +0.0089] | [-0.0025, +0.0119] |
| DF − DL | LL per rating | -0.0150 | -0.0150 | [-0.0210, -0.0082] | [-0.0232, -0.0057] |
| DF − DL | direction acc. | -0.0184 | -0.0184 | [-0.0242, -0.0128] | [-0.0279, -0.0090] |
| DFs − DL | LL per rating | +0.0045 | +0.0045 | [-0.0001, +0.0093] | [-0.0021, +0.0112] |
| DFs − DL | direction acc. | -0.0001 | -0.0001 | [-0.0042, +0.0034] | [-0.0062, +0.0056] |

n raters (fold-specific) = 209, item clusters = 4225. Reproduction check (Am. 9): |rerun − primary| ≤ 1e-3 for every row: True.
