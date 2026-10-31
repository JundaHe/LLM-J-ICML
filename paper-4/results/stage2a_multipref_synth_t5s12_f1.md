# Stage 2a — multipref_synth_t5s12: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DL |
|---|---|---|---|
| 0 | 46 | -1.4401 | -1.4371 |
| 20 | 42 | -1.4408 | -1.3478 |
| 50 | 35 | -1.4373 | -1.3167 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -- | -- | -- | +0.0030 [-0.0046, +0.0106] |
| 20 | -- | -- | -- | -- | -- | -- | -- | +0.0930 [+0.0364, +0.1539] |
| 50 | -- | -- | -- | -- | -- | -- | -- | +0.1206 [+0.0660, +0.1828] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.647 | -- | -- | 0.643 | -- | -- |
| 20 | 0.646 | -- | -- | 0.651 | -- | -- |
| 50 | 0.650 | -- | -- | 0.654 | -- | -- |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
