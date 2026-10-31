# Stage 2a — multipref_synth_t5s13: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 46 | -1.4599 | -1.4640 |
| 20 | 42 | -1.4595 | -1.3809 |
| 50 | 35 | -1.4581 | -1.3439 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0041 [-0.0150, +0.0064] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0787 [+0.0299, +0.1327] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.1142 [+0.0657, +0.1708] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.637 | -- | -- | 0.641 | -- | -- |
| 20 | 0.639 | -- | -- | 0.642 | -- | -- |
| 50 | 0.643 | -- | -- | 0.641 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
