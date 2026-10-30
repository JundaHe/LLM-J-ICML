# Stage 2a — multipref_synth_t0: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DFs | LL DL |
|---|---|---|---|---|
| 0 | 45 | -1.4396 | -1.4397 | -1.4412 |
| 20 | 44 | -1.4393 | -1.3625 | -1.3621 |
| 50 | 37 | -1.4374 | -1.3391 | -1.3386 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -0.0001 [-0.0131, +0.0124] | -- | -- | -0.0016 [-0.0168, +0.0122] |
| 20 | -- | -- | -- | -- | +0.0769 [+0.0478, +0.1085] | -- | -- | +0.0772 [+0.0472, +0.1098] |
| 50 | -- | -- | -- | -- | +0.0983 [+0.0622, +0.1344] | -- | -- | +0.0988 [+0.0620, +0.1354] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.667 | -- | 0.665 | 0.665 | -- | -0.0026 [-0.0066, +0.0009] |
| 20 | 0.668 | -- | 0.664 | 0.663 | -- | -0.0031 [-0.0105, +0.0043] |
| 50 | 0.668 | -- | 0.667 | 0.664 | -- | -0.0016 [-0.0099, +0.0070] |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
