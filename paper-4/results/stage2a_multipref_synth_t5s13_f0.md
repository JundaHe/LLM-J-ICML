# Stage 2a — multipref_synth_t5s13: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 45 | -1.4440 | -1.4589 |
| 20 | 44 | -1.4448 | -1.3615 |
| 50 | 37 | -1.4418 | -1.3231 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0149 [-0.0360, +0.0054] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0833 [+0.0324, +0.1374] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.1187 [+0.0703, +0.1722] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.656 | -- | -- | 0.655 | -- | -- |
| 20 | 0.656 | -- | -- | 0.654 | -- | -- |
| 50 | 0.664 | -- | -- | 0.657 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
