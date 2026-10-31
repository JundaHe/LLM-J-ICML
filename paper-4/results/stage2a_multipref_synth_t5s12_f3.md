# Stage 2a — multipref_synth_t5s12: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 45 | -1.4788 | -1.4823 |
| 20 | 40 | -1.4795 | -1.3737 |
| 50 | 36 | -1.4799 | -1.3449 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0035 [-0.0176, +0.0102] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.1059 [+0.0396, +0.1913] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.1350 [+0.0615, +0.2234] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.654 | -- | -- | 0.655 | -- | -- |
| 20 | 0.654 | -- | -- | 0.655 | -- | -- |
| 50 | 0.652 | -- | -- | 0.654 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
