# Stage 2a — multipref_synth_t5: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DFs | LL DL |
|---|---|---|---|---|
| 0 | 45 | -1.4427 | -1.4399 | -1.4483 |
| 20 | 44 | -1.4423 | -1.3719 | -1.3823 |
| 50 | 37 | -1.4384 | -1.3483 | -1.3528 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | +0.0028 [-0.0090, +0.0145] | -- | -- | -0.0055 [-0.0275, +0.0155] |
| 20 | -- | -- | -- | -- | +0.0704 [+0.0430, +0.1001] | -- | -- | +0.0599 [+0.0240, +0.0979] |
| 50 | -- | -- | -- | -- | +0.0902 [+0.0536, +0.1257] | -- | -- | +0.0856 [+0.0453, +0.1250] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.670 | -- | 0.668 | 0.671 | -- | -0.0025 [-0.0064, +0.0009] |
| 20 | 0.671 | -- | 0.671 | 0.671 | -- | -0.0000 [-0.0062, +0.0056] |
| 50 | 0.669 | -- | 0.669 | 0.668 | -- | -0.0005 [-0.0074, +0.0062] |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
