# Stage 7 S7-3 — seen-rater ceiling, real MultiPref (training raters × test items; trained rater parameters)

904 rater-folds, folds [0, 1, 2, 3, 4]; median training ratings per rater 134, median test-item ratings 34.

| model | direction acc. | − D, direction (points) | own − other, direction (points) | − D, LL (×100 nats) | own − other, LL (×100 nats) |
|---|---|---|---|---|---|
| D | 66.66 | — | — | — | — |
| DF | 66.15 | -0.51 [-0.88, -0.11] | -0.23 [-0.67, +0.23] | +12.87 [+11.56, +14.23] | +28.00 [+25.33, +30.53] |
| DFs | 66.66 | -0.00 [-0.20, +0.18] | +0.10 [-0.10, +0.32] | +12.69 [+11.38, +14.06] | +27.94 [+25.13, +30.57] |
| DL | 66.24 | -0.42 [-0.81, -0.02] | -0.11 [-0.57, +0.36] | +12.78 [+11.41, +14.17] | +32.62 [+29.46, +35.67] |

**Reading (Am. 2): DL own − other direction lower bound -0.57 points → the ranking null also holds for seen raters with all their training ratings.**
