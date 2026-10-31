# Stage 4 S4-A — ceiling on trade-off personalisation (MultiPref; rater's own aspect labels as inputs; rater cut-points in both models)

| k | R − P direction acc. (points) | R − P LL per rating | R − P direction on conflict items (points) | conflict share of test items | raters |
|---|---|---|---|---|---|
| 20 | +0.03 [-0.05, +0.12] | +0.0108 [+0.0027, +0.0195] | +0.58 [-1.08, +2.43] | 4.0 % | 209 |
| 50 | +0.06 [-0.09, +0.21] | +0.0231 [+0.0113, +0.0369] | +0.34 [-2.67, +3.77] | 4.0 % | 180 |
| all | +0.10 [-0.24, +0.43] | +0.0462 [+0.0281, +0.0679] | +2.02 [-4.96, +9.23] | 4.0 % | 226 |
| insample | +0.44 [+0.27, +0.64] | +0.0935 [+0.0785, +0.1115] | +9.72 [+5.60, +14.49] | 4.0 % | 226 |

Penalties per fold (λ_c, λ_δ): {0: (0.3, 1.0), 1: (0.3, 1.0), 2: (0.3, 1.0), 3: (0.3, 1.0), 4: (0.3, 1.0)}.
**Decision rule (S4-B runs only if the k = all lower bound > +0.5 points): FAIL — S4-B not run.**
