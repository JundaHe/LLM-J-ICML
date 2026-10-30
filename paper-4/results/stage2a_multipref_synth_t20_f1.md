# Stage 2a — multipref_synth_t20: new raters, k adaptation ratings (PROTOCOL_STAGE2.md)

| k | raters | LL D | LL DFs | LL DL |
|---|---|---|---|---|
| 0 | 46 | -1.4448 | -1.4487 | -1.4502 |
| 20 | 42 | -1.4456 | -1.3763 | -1.3687 |
| 50 | 35 | -1.4440 | -1.3502 | -1.3281 |

| k | DF−D (H1) | DF−DG (H2) | DF−DL (H3) | F_scale−F_shift (H4) | DFs−D | DF−DFs | F1−T1 | DL−D |
|---|---|---|---|---|---|---|---|---|
| 0 | -- | -- | -- | -- | -0.0040 [-0.0112, +0.0039] | -- | -- | -0.0055 [-0.0168, +0.0065] |
| 20 | -- | -- | -- | -- | +0.0693 [+0.0345, +0.1038] | -- | -- | +0.0769 [+0.0263, +0.1230] |
| 50 | -- | -- | -- | -- | +0.0938 [+0.0509, +0.1388] | -- | -- | +0.1159 [+0.0645, +0.1691] |

| k | dir D | dir DF | dir DFs | dir DL | DF−D dir | DFs−D dir |
|---|---|---|---|---|---|---|
| 0 | 0.630 | -- | 0.632 | 0.637 | -- | +0.0016 [-0.0049, +0.0078] |
| 20 | 0.629 | -- | 0.632 | 0.658 | -- | +0.0030 [-0.0051, +0.0126] |
| 50 | 0.633 | -- | 0.634 | 0.659 | -- | +0.0012 [-0.0074, +0.0103] |

Held-out log-likelihood per rating of new raters' ratings of held-out items; differences with 95 % rater-cluster bootstrap (B = 2000). RPS and direction accuracy in the JSON.
