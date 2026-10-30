# Stage 2a — multipref_synth_t5: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DFs | LL DL |
|---|---|---|---|---|
| 0 | 44 | -1.4930 | -1.4801 | -1.4792 |
| 20 | 43 | -1.4936 | -1.4240 | -1.4420 |
| 50 | 37 | -1.4971 | -1.4120 | -1.4149 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | +0.0129 [+0.0013, +0.0231] | -- | -- | +0.0138 [+0.0008, +0.0250] |
| 20 | -- | -- | -- | -- | +0.0695 [+0.0401, +0.1022] | -- | -- | +0.0516 [+0.0123, +0.0962] |
| 50 | -- | -- | -- | -- | +0.0851 [+0.0519, +0.1274] | -- | -- | +0.0822 [+0.0489, +0.1243] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.659 | -- | 0.660 | 0.663 | -- | +0.0015 [-0.0034, +0.0068] |
| 20 | 0.658 | -- | 0.657 | 0.658 | -- | -0.0015 [-0.0089, +0.0054] |
| 50 | 0.655 | -- | 0.653 | 0.654 | -- | -0.0018 [-0.0110, +0.0059] |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
