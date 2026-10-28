# Two-way bootstrap (Stage 2 Amendment 9) — dices, k = 20, folds [0, 1, 2, 3, 4]

Raters and item clusters (prompt groups) resampled independently (pigeonhole bootstrap), B = 2,000. Per-rating differences are averaged over the 5 adaptation draws within each rating.

| contrast | metric | rerun point | primary point | rater-only 95 % | two-way 95 % |
|---|---|---|---|---|---|
| DF − D | LL per rating | +0.0888 | +0.0888 | [+0.0644, +0.1160] | [+0.0599, +0.1201] |
| DF − D | direction acc. | +0.0481 | +0.0481 | [+0.0249, +0.0772] | [+0.0179, +0.0813] |
| DG − D | LL per rating | -0.0061 | -0.0061 | [-0.0197, +0.0066] | [-0.0210, +0.0074] |
| DG − D | direction acc. | -0.0019 | -0.0019 | [-0.0082, +0.0039] | [-0.0120, +0.0083] |
| DF − DG | LL per rating | +0.0950 | +0.0950 | [+0.0706, +0.1228] | [+0.0664, +0.1283] |
| DF − DG | direction acc. | +0.0501 | +0.0501 | [+0.0266, +0.0770] | [+0.0230, +0.0841] |

n raters (fold-specific) = 104, item clusters = 350. Reproduction check (Am. 9): |rerun − primary| ≤ 1e-3 for every row: True.
