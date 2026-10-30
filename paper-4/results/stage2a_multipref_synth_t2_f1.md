# Stage 2a — multipref_synth_t2: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DFs | LL DL |
|---|---|---|---|---|
| 0 | 46 | -1.4219 | -1.4236 | -1.4262 |
| 20 | 42 | -1.4231 | -1.3454 | -1.3495 |
| 50 | 35 | -1.4220 | -1.3095 | -1.3109 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -0.0017 [-0.0082, +0.0053] | -- | -- | -0.0044 [-0.0128, +0.0051] |
| 20 | -- | -- | -- | -- | +0.0777 [+0.0421, +0.1107] | -- | -- | +0.0736 [+0.0231, +0.1214] |
| 50 | -- | -- | -- | -- | +0.1125 [+0.0635, +0.1653] | -- | -- | +0.1111 [+0.0606, +0.1650] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.674 | -- | 0.676 | 0.683 | -- | +0.0017 [-0.0016, +0.0052] |
| 20 | 0.674 | -- | 0.682 | 0.682 | -- | +0.0086 [+0.0016, +0.0173] |
| 50 | 0.675 | -- | 0.685 | 0.687 | -- | +0.0097 [+0.0012, +0.0196] |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
