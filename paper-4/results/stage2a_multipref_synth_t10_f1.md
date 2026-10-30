# Stage 2a — multipref_synth_t10: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DFs | LL DL |
|---|---|---|---|---|
| 0 | 46 | -1.4356 | -1.4379 | -1.4387 |
| 20 | 42 | -1.4369 | -1.3646 | -1.3634 |
| 50 | 35 | -1.4351 | -1.3306 | -1.3317 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -0.0023 [-0.0094, +0.0054] | -- | -- | -0.0031 [-0.0125, +0.0068] |
| 20 | -- | -- | -- | -- | +0.0723 [+0.0379, +0.1048] | -- | -- | +0.0736 [+0.0398, +0.1040] |
| 50 | -- | -- | -- | -- | +0.1046 [+0.0576, +0.1538] | -- | -- | +0.1034 [+0.0613, +0.1474] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.666 | -- | 0.669 | 0.670 | -- | +0.0033 [-0.0025, +0.0090] |
| 20 | 0.666 | -- | 0.668 | 0.671 | -- | +0.0022 [-0.0055, +0.0097] |
| 50 | 0.670 | -- | 0.670 | 0.673 | -- | -0.0002 [-0.0083, +0.0078] |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
