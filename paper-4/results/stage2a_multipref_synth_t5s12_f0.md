# Stage 2a — multipref_synth_t5s12: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 45 | -1.4410 | -1.4603 |
| 20 | 44 | -1.4416 | -1.3774 |
| 50 | 37 | -1.4407 | -1.3366 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0193 [-0.0474, +0.0069] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0642 [+0.0160, +0.1183] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.1042 [+0.0614, +0.1475] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.655 | -- | -- | 0.655 | -- | -- |
| 20 | 0.656 | -- | -- | 0.649 | -- | -- |
| 50 | 0.659 | -- | -- | 0.653 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
