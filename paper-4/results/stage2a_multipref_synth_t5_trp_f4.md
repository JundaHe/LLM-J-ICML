# Stage 2a — multipref_synth_t5: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 44 | -1.4930 | -1.4792 |
| 20 | 43 | -1.4936 | -1.4655 |
| 50 | 37 | -1.4971 | -1.4170 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | +0.0138 [+0.0008, +0.0250] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0280 [-0.0130, +0.0724] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.0800 [+0.0468, +0.1212] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.659 | -- | -- | 0.663 | -- | -- |
| 20 | 0.658 | -- | -- | 0.658 | -- | -- |
| 50 | 0.655 | -- | -- | 0.651 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
