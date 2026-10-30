# Stage 2a — multipref_synth_t0: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DFs | LL DL |
|---|---|---|---|---|
| 0 | 46 | -1.4238 | -1.4242 | -1.4266 |
| 20 | 42 | -1.4249 | -1.3517 | -1.3626 |
| 50 | 35 | -1.4233 | -1.3199 | -1.3179 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -0.0004 [-0.0068, +0.0064] | -- | -- | -0.0028 [-0.0114, +0.0065] |
| 20 | -- | -- | -- | -- | +0.0732 [+0.0390, +0.1059] | -- | -- | +0.0623 [+0.0116, +0.1097] |
| 50 | -- | -- | -- | -- | +0.1034 [+0.0613, +0.1498] | -- | -- | +0.1054 [+0.0572, +0.1594] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.670 | -- | 0.672 | 0.673 | -- | +0.0017 [-0.0038, +0.0064] |
| 20 | 0.670 | -- | 0.676 | 0.678 | -- | +0.0057 [+0.0014, +0.0096] |
| 50 | 0.674 | -- | 0.683 | 0.684 | -- | +0.0092 [+0.0041, +0.0145] |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
