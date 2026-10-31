# Stage 2a — multipref_synth_t5: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 45 | -1.4427 | -1.4483 |
| 20 | 44 | -1.4423 | -1.3720 |
| 50 | 37 | -1.4384 | -1.3481 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0055 [-0.0275, +0.0155] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0703 [+0.0409, +0.1017] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.0904 [+0.0531, +0.1272] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.670 | -- | -- | 0.671 | -- | -- |
| 20 | 0.671 | -- | -- | 0.672 | -- | -- |
| 50 | 0.669 | -- | -- | 0.668 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
