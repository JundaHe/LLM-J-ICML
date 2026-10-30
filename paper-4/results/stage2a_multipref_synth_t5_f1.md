# Stage 2a — multipref_synth_t5: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DFs | LL DL |
|---|---|---|---|---|
| 0 | 46 | -1.4239 | -1.4260 | -1.4287 |
| 20 | 42 | -1.4253 | -1.3484 | -1.3518 |
| 50 | 35 | -1.4234 | -1.3089 | -1.3100 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -0.0021 [-0.0094, +0.0055] | -- | -- | -0.0048 [-0.0140, +0.0052] |
| 20 | -- | -- | -- | -- | +0.0769 [+0.0416, +0.1095] | -- | -- | +0.0735 [+0.0241, +0.1196] |
| 50 | -- | -- | -- | -- | +0.1145 [+0.0663, +0.1685] | -- | -- | +0.1134 [+0.0639, +0.1686] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.674 | -- | 0.672 | 0.672 | -- | -0.0017 [-0.0065, +0.0018] |
| 20 | 0.675 | -- | 0.676 | 0.677 | -- | +0.0010 [-0.0042, +0.0064] |
| 50 | 0.679 | -- | 0.684 | 0.683 | -- | +0.0052 [-0.0012, +0.0124] |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
