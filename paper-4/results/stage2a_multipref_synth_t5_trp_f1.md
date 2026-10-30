# Stage 2a — multipref_synth_t5: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 46 | -1.4239 | -1.4287 |
| 20 | 42 | -1.4253 | -1.3721 |
| 50 | 35 | -1.4234 | -1.3109 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0048 [-0.0140, +0.0052] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0532 [-0.0036, +0.1027] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.1126 [+0.0621, +0.1689] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.674 | -- | -- | 0.672 | -- | -- |
| 20 | 0.675 | -- | -- | 0.678 | -- | -- |
| 50 | 0.679 | -- | -- | 0.682 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
