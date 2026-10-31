# Stage 2a — multipref_synth_t5s11: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 45 | -1.4535 | -1.4558 |
| 20 | 44 | -1.4532 | -1.3743 |
| 50 | 37 | -1.4517 | -1.3566 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0023 [-0.0141, +0.0092] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0789 [+0.0460, +0.1151] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.0951 [+0.0601, +0.1321] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.644 | -- | -- | 0.647 | -- | -- |
| 20 | 0.644 | -- | -- | 0.648 | -- | -- |
| 50 | 0.645 | -- | -- | 0.644 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
