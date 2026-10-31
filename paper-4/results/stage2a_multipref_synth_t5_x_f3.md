# Stage 2a — multipref_synth_t5: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 45 | -1.4660 | -1.4744 |
| 20 | 40 | -1.4671 | -1.3916 |
| 50 | 36 | -1.4641 | -1.3398 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0084 [-0.0278, +0.0089] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0755 [+0.0280, +0.1222] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.1243 [+0.0448, +0.2061] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.633 | -- | -- | 0.634 | -- | -- |
| 20 | 0.632 | -- | -- | 0.637 | -- | -- |
| 50 | 0.634 | -- | -- | 0.636 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
