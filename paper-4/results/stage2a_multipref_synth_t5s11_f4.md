# Stage 2a — multipref_synth_t5s11: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 44 | -1.4848 | -1.4753 |
| 20 | 43 | -1.4854 | -1.4086 |
| 50 | 37 | -1.4808 | -1.3727 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | +0.0095 [-0.0044, +0.0209] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0768 [+0.0326, +0.1282] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.1081 [+0.0615, +0.1669] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.669 | -- | -- | 0.673 | -- | -- |
| 20 | 0.669 | -- | -- | 0.670 | -- | -- |
| 50 | 0.672 | -- | -- | 0.672 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
