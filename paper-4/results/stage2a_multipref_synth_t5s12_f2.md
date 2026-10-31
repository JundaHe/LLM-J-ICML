# Stage 2a — multipref_synth_t5s12: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 46 | -1.4345 | -1.4439 |
| 20 | 40 | -1.4348 | -1.3474 |
| 50 | 35 | -1.4356 | -1.3254 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0094 [-0.0216, +0.0033] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0874 [+0.0324, +0.1474] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.1102 [+0.0542, +0.1726] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.681 | -- | -- | 0.675 | -- | -- |
| 20 | 0.682 | -- | -- | 0.681 | -- | -- |
| 50 | 0.685 | -- | -- | 0.685 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
