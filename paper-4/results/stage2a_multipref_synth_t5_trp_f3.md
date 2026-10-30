# Stage 2a — multipref_synth_t5: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 45 | -1.4660 | -1.4744 |
| 20 | 40 | -1.4671 | -1.3901 |
| 50 | 36 | -1.4641 | -1.3384 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | -0.0084 [-0.0278, +0.0089] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0770 [+0.0023, +0.1533] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.1257 [+0.0474, +0.2058] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.633 | -- | -- | 0.634 | -- | -- |
| 20 | 0.632 | -- | -- | 0.631 | -- | -- |
| 50 | 0.634 | -- | -- | 0.632 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
