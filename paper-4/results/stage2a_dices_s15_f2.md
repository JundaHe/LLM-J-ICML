# Stage 2a — dices: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DF | LL DL | LL T0 | LL F | LL L | LL DFL | LL FL |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 21 | -0.8684 | -0.9059 | -0.9750 | -0.8688 | -0.8792 | -0.8809 | -0.9105 | -0.8822 |
| 20 | 21 | -0.8684 | -0.8347 | -0.8703 | -0.8688 | -0.8851 | -0.8851 | -0.8441 | -0.8985 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -0.0376 [-0.0728, -0.0037] | -- | +0.0691 [+0.0325, +0.1066] | -- | -- | -- | -- | -0.1066 [-0.1793, -0.0367] |
| 20 | +0.0337 [-0.0077, +0.0807] | -- | +0.0357 [+0.0162, +0.0579] | -- | -- | -- | -- | -0.0019 [-0.0628, +0.0594] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.656 | 0.656 | -- | 0.660 | +0.0000 [+0.0000, +0.0000] | -- |
| 20 | 0.656 | 0.667 | -- | 0.660 | +0.0111 [-0.0142, +0.0531] | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
