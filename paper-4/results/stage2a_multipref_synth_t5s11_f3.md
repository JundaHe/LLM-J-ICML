# Stage 2a — multipref_synth_t5s11: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 45 | -1.4668 | -1.4700 |
| 20 | 40 | -1.4674 | -1.3727 |
| 50 | 36 | -1.4647 | -1.3442 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0032 [-0.0183, +0.0092] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0947 [+0.0319, +0.1611] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.1204 [+0.0528, +0.1971] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.657 | -- | -- | 0.655 | -- | -- |
| 20 | 0.657 | -- | -- | 0.650 | -- | -- |
| 50 | 0.660 | -- | -- | 0.655 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
