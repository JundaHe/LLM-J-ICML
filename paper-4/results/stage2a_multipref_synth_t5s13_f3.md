# Stage 2a — multipref_synth_t5s13: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 45 | -1.4690 | -1.4773 |
| 20 | 40 | -1.4699 | -1.3358 |
| 50 | 36 | -1.4734 | -1.3129 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0083 [-0.0317, +0.0122] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.1341 [+0.0584, +0.2163] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.1605 [+0.0732, +0.2559] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.641 | -- | -- | 0.640 | -- | -- |
| 20 | 0.641 | -- | -- | 0.643 | -- | -- |
| 50 | 0.640 | -- | -- | 0.640 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
