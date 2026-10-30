# Stage 2a — multipref_synth_t20: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DFs | LL DL |
|---|---|---|---|---|
| 0 | 45 | -1.4663 | -1.4625 | -1.4616 |
| 20 | 44 | -1.4664 | -1.4096 | -1.4019 |
| 50 | 37 | -1.4650 | -1.3939 | -1.3704 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | +0.0039 [-0.0067, +0.0138] | -- | -- | +0.0047 [-0.0087, +0.0175] |
| 20 | -- | -- | -- | -- | +0.0568 [+0.0307, +0.0855] | -- | -- | +0.0645 [+0.0267, +0.1041] |
| 50 | -- | -- | -- | -- | +0.0710 [+0.0404, +0.1055] | -- | -- | +0.0946 [+0.0584, +0.1339] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.645 | -- | 0.640 | 0.636 | -- | -0.0047 [-0.0092, +0.0000] |
| 20 | 0.645 | -- | 0.643 | 0.660 | -- | -0.0017 [-0.0094, +0.0064] |
| 50 | 0.641 | -- | 0.643 | 0.671 | -- | +0.0020 [-0.0063, +0.0117] |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
