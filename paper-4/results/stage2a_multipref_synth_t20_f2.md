# Stage 2a — multipref_synth_t20: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DFs | LL DL |
|---|---|---|---|---|
| 0 | 46 | -1.4858 | -1.5002 | -1.5100 |
| 20 | 40 | -1.4855 | -1.3854 | -1.3838 |
| 50 | 35 | -1.4903 | -1.3668 | -1.3444 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -0.0144 [-0.0276, -0.0003] | -- | -- | -0.0242 [-0.0415, -0.0052] |
| 20 | -- | -- | -- | -- | +0.1001 [+0.0547, +0.1492] | -- | -- | +0.1017 [+0.0547, +0.1523] |
| 50 | -- | -- | -- | -- | +0.1235 [+0.0726, +0.1803] | -- | -- | +0.1459 [+0.0904, +0.2024] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.605 | -- | 0.604 | 0.596 | -- | -0.0009 [-0.0056, +0.0036] |
| 20 | 0.608 | -- | 0.609 | 0.617 | -- | +0.0018 [-0.0058, +0.0098] |
| 50 | 0.609 | -- | 0.612 | 0.656 | -- | +0.0024 [-0.0072, +0.0112] |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
