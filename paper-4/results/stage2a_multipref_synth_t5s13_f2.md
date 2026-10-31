# Stage 2a — multipref_synth_t5s13: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 46 | -1.4391 | -1.4694 |
| 20 | 40 | -1.4406 | -1.3767 |
| 50 | 35 | -1.4405 | -1.3442 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0303 [-0.0538, -0.0079] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0639 [+0.0116, +0.1195] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.0962 [+0.0472, +0.1534] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.654 | -- | -- | 0.654 | -- | -- |
| 20 | 0.653 | -- | -- | 0.647 | -- | -- |
| 50 | 0.653 | -- | -- | 0.649 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
