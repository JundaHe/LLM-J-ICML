# Stage 2a — multipref_synth_t5s11: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 46 | -1.4129 | -1.4219 |
| 20 | 40 | -1.4147 | -1.3372 |
| 50 | 35 | -1.4160 | -1.3167 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0090 [-0.0193, +0.0021] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0775 [+0.0352, +0.1245] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.0993 [+0.0568, +0.1492] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.642 | -- | -- | 0.645 | -- | -- |
| 20 | 0.641 | -- | -- | 0.647 | -- | -- |
| 50 | 0.644 | -- | -- | 0.649 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
