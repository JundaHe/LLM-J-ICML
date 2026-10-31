# Stage 2a — multipref_synth_t5s13: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 44 | -1.4727 | -1.4438 |
| 20 | 43 | -1.4732 | -1.4085 |
| 50 | 37 | -1.4701 | -1.3697 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | +0.0289 [+0.0126, +0.0427] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0647 [+0.0257, +0.1078] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.1004 [+0.0654, +0.1420] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.644 | -- | -- | 0.649 | -- | -- |
| 20 | 0.643 | -- | -- | 0.646 | -- | -- |
| 50 | 0.646 | -- | -- | 0.649 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
