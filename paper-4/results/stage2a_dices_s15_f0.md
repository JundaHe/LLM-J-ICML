# Stage 2a — dices: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DF | LL DL | LL T0 | LL F | LL L | LL DFL | LL FL |
|---|---|---|---|---|---|---|---|---|---|
| 0 | 23 | -0.8536 | -0.8734 | -0.9110 | -0.8590 | -0.8794 | -0.8811 | -0.8764 | -0.8813 |
| 20 | 23 | -0.8536 | -0.7143 | -0.7138 | -0.8590 | -0.7673 | -0.7738 | -0.7119 | -0.7658 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -0.0198 [-0.0590, +0.0099] | -- | +0.0376 [+0.0121, +0.0740] | -- | -- | -- | -- | -0.0573 [-0.1333, -0.0023] |
| 20 | +0.1393 [+0.0793, +0.2176] | -- | -0.0005 [-0.0104, +0.0088] | -- | -- | -- | -- | +0.1399 [+0.0784, +0.2210] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.595 | 0.601 | -- | 0.611 | +0.0066 [+0.0013, +0.0120] | -- |
| 20 | 0.595 | 0.698 | -- | 0.698 | +0.1028 [+0.0396, +0.1820] | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
