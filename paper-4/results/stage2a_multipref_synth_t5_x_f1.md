# Stage 2a — multipref_synth_t5: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 46 | -1.4239 | -1.4287 |
| 20 | 42 | -1.4253 | -1.3552 |
| 50 | 35 | -1.4234 | -1.3106 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0048 [-0.0140, +0.0052] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0701 [+0.0393, +0.1001] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.1128 [+0.0659, +0.1650] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.674 | -- | -- | 0.672 | -- | -- |
| 20 | 0.675 | -- | -- | 0.677 | -- | -- |
| 50 | 0.679 | -- | -- | 0.683 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
