# Stage 2a — multipref_synth_t5s12: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 44 | -1.5048 | -1.4866 |
| 20 | 43 | -1.5044 | -1.4303 |
| 50 | 37 | -1.5084 | -1.4071 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | +0.0182 [+0.0028, +0.0307] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0741 [+0.0344, +0.1181] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.1013 [+0.0589, +0.1489] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.643 | -- | -- | 0.643 | -- | -- |
| 20 | 0.643 | -- | -- | 0.642 | -- | -- |
| 50 | 0.640 | -- | -- | 0.640 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
