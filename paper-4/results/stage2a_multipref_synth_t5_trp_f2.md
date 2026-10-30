# Stage 2a — multipref_synth_t5: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 46 | -1.4319 | -1.4476 |
| 20 | 40 | -1.4317 | -1.3786 |
| 50 | 35 | -1.4364 | -1.3403 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0157 [-0.0302, +0.0001] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0531 [+0.0061, +0.1033] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.0960 [+0.0499, +0.1459] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.654 | -- | -- | 0.657 | -- | -- |
| 20 | 0.655 | -- | -- | 0.653 | -- | -- |
| 50 | 0.654 | -- | -- | 0.652 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
