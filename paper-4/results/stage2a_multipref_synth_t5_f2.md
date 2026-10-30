# Stage 2a — multipref_synth_t5: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DFs | LL DL |
|---|---|---|---|---|
| 0 | 46 | -1.4319 | -1.4418 | -1.4476 |
| 20 | 40 | -1.4317 | -1.3608 | -1.3570 |
| 50 | 35 | -1.4364 | -1.3363 | -1.3365 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -0.0099 [-0.0206, +0.0016] | -- | -- | -0.0157 [-0.0302, +0.0001] |
| 20 | -- | -- | -- | -- | +0.0709 [+0.0264, +0.1180] | -- | -- | +0.0747 [+0.0306, +0.1206] |
| 50 | -- | -- | -- | -- | +0.1001 [+0.0526, +0.1506] | -- | -- | +0.0999 [+0.0540, +0.1490] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.654 | -- | 0.654 | 0.657 | -- | +0.0000 [-0.0038, +0.0036] |
| 20 | 0.655 | -- | 0.656 | 0.656 | -- | +0.0011 [-0.0053, +0.0079] |
| 50 | 0.654 | -- | 0.659 | 0.654 | -- | +0.0048 [-0.0043, +0.0142] |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
