# Stage 2a — dorn_raters: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DF | LL DL | LL T0 | LL F | LL L | LL DFL | LL FL |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 743 | -1.5356 | -1.5362 | -1.5356 | -1.5388 | -1.5736 | -1.5980 | -1.5362 | -1.5737 |
| 10 | 684 | -1.5376 | -1.4902 | -1.5376 | -1.5422 | -1.5234 | -1.4956 | -1.4902 | -1.5234 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -0.0006 [-0.0015, +0.0005] | -- | -0.0006 [-0.0015, +0.0005] | -- | -- | -- | -- | -0.0000 [-0.0000, +0.0000] |
| 10 | +0.0474 [+0.0249, +0.0687] | -- | +0.0474 [+0.0249, +0.0687] | -- | -- | -- | -- | -0.0000 [-0.0000, +0.0000] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.629 | 0.625 | -- | 0.629 | -0.0038 [-0.0098, +0.0019] | -- |
| 10 | 0.629 | 0.699 | -- | 0.629 | +0.0693 [+0.0479, +0.0902] | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
