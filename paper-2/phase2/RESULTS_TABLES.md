# Consolidated results tables (2026-10-11 12:30; numbers from PROGRESS.md and the analysis JSONs)

Inference labels (Codex round 3): CI = test-item/document-clustered bootstrap **conditional on the trained models** (one optimiser seed, one permutation draw, one split per cell); ± = **descriptive** SEM over pipeline configurations that reuse seeds/splits (not independent replicates). Confirmatory intervals will come from the seed × fold replication (chain7) with crossed bootstrap. "Inert" below means *no detectable average degradation in this conditional analysis*, not equivalence.

Sign convention everywhere: contrasts are `a − b`; for RPS/KL lower is better, so **negative means the first arm is better**.

## T1. Panels (frozen scope, 2026-10-13). Heads: ratings per item = training + reference annotation positions; LoRA (SummEval only): 7 training raters / 1 held-out expert per fold.
| panel | key | items | ratings per item | K | scale | groups (max size) | rater identity |
|---|---|---|---|---|---|---|---|
| SummEval coherence | `summeval_coherence8` | 1600 | 8 | 5 | ordinal | 100 (16) | persistent raters |
| SummEval relevance (auxiliary, T7 only) | `summeval_relevance8` | 1600 | 8 | 5 | ordinal | 100 (16) | persistent raters |
| Scalabrino readability | `scalabrino` | 124 | 9 | 5 | ordinal | 124 (1) | persistent raters |
| Buse–Weimer readability | `bw` | 100 | 121 | 5 | ordinal | 100 (1) | persistent raters |
| HelpSteer2 helpfulness (5-rating subset) | `hs2_help5` | 4786 | 5 | 5 | ordinal | 2393 (2) | annotation positions |
| POPQUORN offensiveness | `popquorn_off8` | 1366 | 8 | 5 | ordinal | 1366 (1) | annotation positions |
| POPQUORN politeness | `popquorn_pol5` | 3690 | 5 | 5 | ordinal | 3690 (1) | annotation positions |
| CSC sarcasm (LeWiDi-2025, 6-observer subset) | `csc6` | 1920 | 6 | 6 | ordinal | 32 (60) | annotation positions |
| EmoBank reader valence (3,000-sentence subsample) | `emobank_reader_v5` | 3000 | 5 | 5 | ordinal | 3000 (1) | annotation positions |
| DICES-350 Q_overall | `dices` | 350 | 104 | 3 | ordinal | 350 (1) | persistent raters |
| DICES-990 Q_overall | `dices990` | 990 | 60 | 3 | ordinal | 990 (1) | annotation positions |
| ChaosNLI MNLI | `chaosnli_mnli` | 1599 | 100 | 3 | nominal | 1599 (1) | annotation positions |
| ChaosNLI SNLI | `chaosnli_snli` | 1514 | 100 | 3 | nominal | 1514 (1) | annotation positions |
| ChaosNLI αNLI (zero-dose check) | `chaosnli_alphanli` | 1532 | 100 | 2 | nominal | 1532 (1) | annotation positions |
Ten primary ordinal head panels; SummEval relevance appears only in the G × R diagnostic (T7); αNLI is a zero-dose implementation check.

## T2. (superseded) The exploratory probe_mean hierarchy used rater-vector matching and is moved to RESULTS_LEGACY.md; it is not evidence. Use T2b.

## T2b. Heads hierarchy — frozen scope. Protocol versions: `_v7` (group-disjoint splits, histogram-class matching, exact KKT projection) for HelpSteer2, POPQUORN ×2, DICES-990, CSC, EmoBank; `_v6` (same matching/projection; single-row items or document-grouped, so the split was already group-disjoint) for SummEval, Scalabrino, BW, DICES-350. 30 cfgs = 5 RNG streams × 3 item splits × 2 annotation-position splits per panel; ± = descriptive SEM over dependent configurations, not a CI. Contrast = arm − soft. Every permutation contrast is accompanied by its realised dose; pmmx post-projection dose uses the T2c rule (changed = TV > 1e-9). Quarantined `_v3`–`_v5` runs (rater-vector matching) are listed once in RESULTS_LEGACY.md as an implementation-audit row.

**SummEval coherence** (`_v6`, 30 cfgs; soft RPS 0.1639). Realised dose (changed fraction / mean TV of changed pairs / TV over all items): pmode 1.000 / 0.29 / 0.291; pmm 0.728 / 0.38 / 0.275; pmmx post-projection (T2c rule, TV > 1e-9): changed 0.728 / TV 0.378 / TV-all 0.273.

| arm − soft | RPS | KL | D partial |
|---|---|---|---|
| hard | +0.0072±0.0006 | +0.079±0.005 | +0.007±0.015 |
| smooth | +0.0044±0.0009 | +0.039±0.005 | +0.007±0.012 |
| sordz | +0.0021±0.0005 | -0.020±0.008 | +0.016±0.008 |
| proto | +0.0049±0.0004 | +0.030±0.003 | +0.007±0.010 |
| sordm | -0.0053±0.0010 | -0.058±0.012 | +0.006±0.008 |
| mean2 | -0.0021±0.0003 | -0.018±0.004 | -0.006±0.007 |
| cond | -0.0012±0.0003 | -0.003±0.004 | -0.003±0.009 |
| shrunk | +0.0005±0.0004 | +0.003±0.003 | +0.006±0.007 |
| shrunk_strong | +0.0015±0.0004 | +0.010±0.004 | +0.002±0.010 |
| shrunk_res | -0.0016±0.0003 | -0.013±0.003 | -0.001±0.008 |
| soft_pmode | +0.0050±0.0006 | +0.028±0.005 | +0.001±0.012 |
| soft_pmm | -0.0008±0.0003 | +0.009±0.004 | -0.002±0.009 |
| soft_pmmx | -0.0010±0.0003 | +0.004±0.004 | -0.007±0.011 |

**Buse–Weimer** (`_v6`, 30 cfgs; soft RPS 0.1645). Realised dose (changed fraction / mean TV of changed pairs / TV over all items): pmode 0.994 / 0.14 / 0.139; pmm 0.761 / 0.09 / 0.069; pmmx post-projection (T2c rule, TV > 1e-9): changed 0.761 / TV 0.089 / TV-all 0.068.

| arm − soft | RPS | KL | D partial |
|---|---|---|---|
| hard | -0.0022±0.0012 | +0.010±0.008 | -0.049±0.040 |
| smooth | -0.0040±0.0013 | +0.000±0.009 | -0.015±0.044 |
| sordz | +0.0001±0.0012 | +0.005±0.010 | -0.119±0.033 |
| proto | -0.0020±0.0007 | -0.016±0.005 | -0.121±0.031 |
| sordm | -0.0043±0.0010 | -0.015±0.007 | -0.062±0.023 |
| mean2 | -0.0016±0.0007 | -0.013±0.005 | -0.028±0.024 |
| cond | -0.0026±0.0008 | -0.017±0.006 | -0.043±0.023 |
| shrunk | -0.0005±0.0007 | -0.004±0.005 | -0.009±0.019 |
| shrunk_strong | -0.0024±0.0011 | -0.019±0.007 | -0.045±0.023 |
| shrunk_res | -0.0007±0.0008 | -0.007±0.006 | -0.036±0.024 |
| soft_pmode | -0.0017±0.0010 | -0.009±0.008 | -0.068±0.042 |
| soft_pmm | -0.0018±0.0010 | -0.013±0.007 | -0.019±0.019 |
| soft_pmmx | -0.0024±0.0007 | -0.018±0.005 | -0.026±0.022 |

**DICES Q_overall** (`_v6`, 30 cfgs; soft RPS 0.2180). Realised dose (changed fraction / mean TV of changed pairs / TV over all items): pmode 1.000 / 0.16 / 0.156; pmm 0.990 / 0.04 / 0.042; pmmx post-projection (T2c rule, TV > 1e-9): changed 0.990 / TV 0.036 / TV-all 0.036.

| arm − soft | RPS | KL | D partial |
|---|---|---|---|
| hard | +0.0045±0.0014 | +0.044±0.005 | -0.078±0.025 |
| smooth | +0.0015±0.0010 | +0.037±0.004 | -0.085±0.025 |
| sordz | +0.0043±0.0013 | +0.048±0.005 | -0.093±0.028 |
| proto | -0.0006±0.0005 | -0.004±0.002 | -0.060±0.017 |
| sordm | +0.0429±0.0011 | +0.319±0.004 | -0.025±0.022 |
| mean2 | -0.0009±0.0006 | -0.006±0.002 | -0.006±0.016 |
| cond | -0.0016±0.0007 | -0.006±0.002 | -0.031±0.015 |
| shrunk | -0.0008±0.0009 | -0.003±0.003 | -0.036±0.014 |
| shrunk_strong | -0.0014±0.0006 | -0.006±0.002 | -0.063±0.016 |
| shrunk_res | -0.0000±0.0006 | -0.003±0.002 | -0.008±0.011 |
| soft_pmode | +0.0022±0.0011 | +0.004±0.003 | -0.055±0.026 |
| soft_pmm | -0.0005±0.0006 | -0.002±0.002 | -0.007±0.012 |
| soft_pmmx | -0.0018±0.0007 | -0.005±0.002 | -0.011±0.012 |

**Scalabrino** (`_v6`, 30 cfgs; soft RPS 0.1501). Realised dose (changed fraction / mean TV of changed pairs / TV over all items): pmode 0.991 / 0.28 / 0.274; pmm 0.509 / 0.34 / 0.173; pmmx post-projection (T2c rule, TV > 1e-9): changed 0.509 / TV 0.340 / TV-all 0.173.

| arm − soft | RPS | KL | D partial |
|---|---|---|---|
| hard | +0.0044±0.0012 | +0.055±0.008 | -0.067±0.031 |
| smooth | +0.0040±0.0012 | +0.074±0.020 | -0.027±0.029 |
| sordz | +0.0030±0.0006 | +0.007±0.007 | -0.001±0.022 |
| proto | +0.0033±0.0009 | +0.005±0.007 | -0.093±0.026 |
| sordm | -0.0033±0.0008 | -0.045±0.009 | -0.000±0.026 |
| mean2 | +0.0007±0.0005 | -0.010±0.005 | -0.035±0.020 |
| cond | +0.0001±0.0006 | -0.020±0.006 | -0.041±0.022 |
| shrunk | +0.0010±0.0005 | +0.004±0.005 | -0.056±0.022 |
| shrunk_strong | +0.0012±0.0008 | -0.003±0.005 | -0.042±0.020 |
| shrunk_res | +0.0010±0.0004 | -0.004±0.004 | -0.073±0.022 |
| soft_pmode | +0.0028±0.0010 | +0.021±0.009 | -0.080±0.029 |
| soft_pmm | -0.0002±0.0007 | -0.006±0.007 | -0.041±0.028 |
| soft_pmmx | -0.0003±0.0007 | -0.001±0.008 | -0.050±0.030 |

**HelpSteer2 helpfulness** (`_v7`, 30 cfgs; soft RPS 0.1951). Realised dose (changed fraction / mean TV of changed pairs / TV over all items): pmode 1.000 / 0.39 / 0.390; pmm 0.280 / 0.67 / 0.186; pmmx post-projection (T2c rule, TV > 1e-9): changed 0.280 / TV 0.667 / TV-all 0.186.

| arm − soft | RPS | KL | D partial |
|---|---|---|---|
| hard | +0.0049±0.0003 | +0.038±0.002 | -0.042±0.006 |
| smooth | +0.0031±0.0003 | +0.031±0.001 | -0.022±0.005 |
| sordz | +0.0044±0.0003 | +0.037±0.002 | -0.030±0.004 |
| proto | -0.0002±0.0002 | -0.003±0.001 | -0.018±0.003 |
| sordm | +0.0088±0.0003 | +0.097±0.002 | -0.000±0.004 |
| mean2 | +0.0002±0.0002 | -0.001±0.001 | -0.005±0.003 |
| cond | +0.0000±0.0001 | -0.000±0.001 | -0.006±0.003 |
| shrunk | -0.0003±0.0001 | -0.003±0.001 | -0.007±0.003 |
| shrunk_strong | -0.0002±0.0002 | -0.004±0.001 | -0.010±0.003 |
| shrunk_res | -0.0001±0.0002 | -0.003±0.001 | -0.005±0.002 |
| soft_pmode | +0.0006±0.0002 | +0.004±0.001 | -0.016±0.003 |
| soft_pmm | +0.0002±0.0001 | +0.002±0.001 | -0.005±0.003 |
| soft_pmmx | +0.0005±0.0001 | +0.002±0.001 | -0.009±0.003 |

**POPQUORN offensiveness** (`_v7`, 30 cfgs; soft RPS 0.1269). Realised dose (changed fraction / mean TV of changed pairs / TV over all items): pmode 1.000 / 0.29 / 0.295; pmm 0.638 / 0.34 / 0.218; pmmx post-projection (T2c rule, TV > 1e-9): changed 0.638 / TV 0.342 / TV-all 0.218.

| arm − soft | RPS | KL | D partial |
|---|---|---|---|
| hard | +0.0042±0.0003 | +0.036±0.002 | -0.021±0.005 |
| smooth | +0.0043±0.0003 | +0.037±0.002 | -0.014±0.004 |
| sordz | +0.0039±0.0002 | +0.032±0.002 | -0.014±0.005 |
| proto | +0.0054±0.0002 | +0.029±0.001 | -0.028±0.004 |
| sordm | +0.0159±0.0005 | +0.155±0.006 | +0.018±0.005 |
| mean2 | +0.0002±0.0001 | -0.002±0.001 | -0.001±0.003 |
| cond | -0.0002±0.0001 | -0.004±0.001 | -0.004±0.003 |
| shrunk | +0.0005±0.0002 | +0.002±0.001 | -0.007±0.004 |
| shrunk_strong | +0.0010±0.0002 | +0.005±0.001 | -0.012±0.003 |
| shrunk_res | +0.0000±0.0002 | -0.004±0.001 | +0.002±0.003 |
| soft_pmode | +0.0068±0.0003 | +0.042±0.002 | -0.008±0.005 |
| soft_pmm | +0.0002±0.0002 | +0.001±0.001 | +0.005±0.003 |
| soft_pmmx | +0.0002±0.0002 | +0.001±0.002 | +0.004±0.003 |

**DICES-990** (`_v7`, 30 cfgs; soft RPS 0.1900). Realised dose (changed fraction / mean TV of changed pairs / TV over all items): pmode 1.000 / 0.14 / 0.135; pmm 0.995 / 0.05 / 0.048; pmmx post-projection (T2c rule, TV > 1e-9): changed 0.985 / TV 0.042 / TV-all 0.042.

| arm − soft | RPS | KL | D partial |
|---|---|---|---|
| hard | +0.0108±0.0004 | +0.064±0.002 | -0.167±0.009 |
| smooth | +0.0066±0.0003 | +0.046±0.001 | -0.125±0.011 |
| sordz | +0.0101±0.0003 | +0.064±0.002 | -0.157±0.009 |
| proto | +0.0055±0.0003 | +0.016±0.001 | -0.165±0.008 |
| sordm | +0.0552±0.0012 | +0.342±0.002 | -0.019±0.010 |
| mean2 | +0.0001±0.0002 | -0.000±0.001 | -0.005±0.006 |
| cond | -0.0002±0.0002 | -0.001±0.001 | -0.003±0.005 |
| shrunk | -0.0002±0.0002 | -0.001±0.001 | -0.004±0.007 |
| shrunk_strong | +0.0002±0.0002 | +0.001±0.001 | -0.048±0.007 |
| shrunk_res | -0.0000±0.0003 | -0.001±0.001 | -0.010±0.006 |
| soft_pmode | +0.0043±0.0002 | +0.013±0.001 | -0.098±0.007 |
| soft_pmm | -0.0002±0.0002 | +0.000±0.001 | +0.003±0.006 |
| soft_pmmx | -0.0001±0.0002 | -0.000±0.001 | +0.003±0.006 |

**POPQUORN politeness** (`_v7`, 30 cfgs; soft RPS 0.1328). Realised dose (changed fraction / mean TV of changed pairs / TV over all items): pmode 1.000 / 0.34 / 0.335; pmm 0.417 / 0.50 / 0.209; pmmx post-projection (T2c rule, TV > 1e-9): changed 0.417 / TV 0.500 / TV-all 0.209.

| arm − soft | RPS | KL | D partial |
|---|---|---|---|
| hard | +0.0049±0.0002 | +0.058±0.002 | +nan±nan |
| smooth | +0.0041±0.0002 | +0.038±0.002 | +nan±nan |
| sordz | +0.0018±0.0002 | +0.014±0.002 | +nan±nan |
| proto | +0.0018±0.0002 | +0.007±0.002 | +nan±nan |
| sordm | +0.0026±0.0002 | +0.021±0.002 | +nan±nan |
| mean2 | +0.0000±0.0002 | -0.001±0.002 | +nan±nan |
| cond | -0.0002±0.0002 | -0.004±0.002 | +nan±nan |
| shrunk | -0.0000±0.0002 | -0.002±0.001 | +nan±nan |
| shrunk_strong | +0.0002±0.0002 | -0.002±0.002 | +nan±nan |
| shrunk_res | -0.0003±0.0002 | -0.005±0.001 | +nan±nan |
| soft_pmode | +0.0033±0.0002 | +0.022±0.002 | +nan±nan |
| soft_pmm | +0.0001±0.0002 | -0.000±0.001 | +nan±nan |
| soft_pmmx | +0.0002±0.0002 | -0.001±0.001 | +nan±nan |

**CSC sarcasm** (`_v7`, 30 cfgs; soft RPS 0.1616). Realised dose (changed fraction / mean TV of changed pairs / TV over all items): pmode 1.000 / 0.33 / 0.332; pmm 0.704 / 0.41 / 0.288; pmmx post-projection (T2c rule, TV > 1e-9): changed 0.704 / TV 0.409 / TV-all 0.288.

| arm − soft | RPS | KL | D partial |
|---|---|---|---|
| hard | +0.0046±0.0006 | +0.034±0.005 | +nan±nan |
| smooth | +0.0055±0.0008 | +0.029±0.006 | +nan±nan |
| sordz | +0.0022±0.0004 | +0.019±0.005 | +nan±nan |
| proto | +0.0014±0.0004 | -0.002±0.003 | +nan±nan |
| sordm | +0.0123±0.0007 | +0.120±0.006 | +nan±nan |
| mean2 | -0.0004±0.0004 | -0.007±0.003 | +nan±nan |
| cond | -0.0003±0.0004 | -0.006±0.003 | +nan±nan |
| shrunk | -0.0002±0.0004 | -0.005±0.003 | +nan±nan |
| shrunk_strong | +0.0006±0.0004 | -0.004±0.003 | +nan±nan |
| shrunk_res | -0.0008±0.0003 | -0.010±0.003 | +nan±nan |
| soft_pmode | +0.0022±0.0005 | +0.009±0.004 | +nan±nan |
| soft_pmm | -0.0003±0.0005 | -0.003±0.004 | +nan±nan |
| soft_pmmx | +0.0002±0.0003 | -0.001±0.003 | +nan±nan |

**EmoBank reader valence** (`_v7`, 30 cfgs; soft RPS 0.0861). Realised dose (changed fraction / mean TV of changed pairs / TV over all items): pmode 0.999 / 0.31 / 0.313; pmm 0.135 / 0.50 / 0.068; pmmx post-projection (T2c rule, TV > 1e-9): changed 0.135 / TV 0.500 / TV-all 0.068.

| arm − soft | RPS | KL | D partial |
|---|---|---|---|
| hard | +0.0042±0.0002 | +0.086±0.004 | +nan±nan |
| smooth | +0.0043±0.0002 | +0.067±0.003 | +nan±nan |
| sordz | +0.0043±0.0002 | +0.063±0.002 | +nan±nan |
| proto | +0.0022±0.0002 | +0.031±0.002 | +nan±nan |
| sordm | +0.0037±0.0004 | +0.132±0.004 | +nan±nan |
| mean2 | +0.0016±0.0001 | +0.023±0.002 | +nan±nan |
| cond | +0.0005±0.0001 | +0.006±0.002 | +nan±nan |
| shrunk | +0.0001±0.0001 | +0.001±0.002 | +nan±nan |
| shrunk_strong | +0.0003±0.0001 | +0.002±0.002 | +nan±nan |
| shrunk_res | +0.0004±0.0001 | +0.001±0.002 | +nan±nan |
| soft_pmode | +0.0048±0.0002 | +0.061±0.002 | +nan±nan |
| soft_pmm | +0.0006±0.0001 | +0.011±0.002 | +nan±nan |
| soft_pmmx | +0.0006±0.0001 | +0.009±0.002 | +nan±nan |


### T2c. Dose / support certificates (offline `dose_audit.py`; 18 cfgs per panel; identical split/cell/RNG logic to probe_mean2). Eleven ordinal rows: the ten primary panels plus SummEval relevance (auxiliary; T7 only). support = fraction of training items in mode(-and-mean) cells containing ≥ 2 histogram classes (upper bound for any bijection); changed = realised fraction; TV (all items) counts unchanged items as 0; zero-TV pairs must be 0; pmmx rows report the POST-PROJECTION dose.
| panel | arm | n_train | train raters | support (het. cells) | changed | TV (changed) | TV (all items) | zero-TV pairs | mean shift mean / max |
|---|---|---|---|---|---|---|---|---|---|
| bw | soft_pmm | 60 | 97 | 0.761 | 0.761 | 0.091 | 0.069 | 0 | 0.03 / 0.09 |
| bw | soft_pmmx | 60 | 97 | 0.761 | 0.761 | 0.089 | 0.068 | 0 | 0.00 / 0.00 |
| bw | soft_pmode | 60 | 97 | 0.994 | 0.994 | 0.140 | 0.139 | 0 | 0.27 / 1.13 |
| csc6 | soft_pmm | 1140 | 5 | 0.843 | 0.704 | 0.409 | 0.288 | 0 | 0.00 / 0.00 |
| csc6 | soft_pmmx | 1140 | 5 | 0.843 | 0.704 | 0.409 | 0.288 | 0 | 0.00 / 0.00 |
| csc6 | soft_pmode | 1140 | 5 | 1.000 | 1.000 | 0.332 | 0.332 | 0 | 0.57 / 2.40 |
| dices | soft_pmm | 210 | 80 | 0.993 | 0.990 | 0.043 | 0.042 | 0 | 0.03 / 0.10 |
| dices | soft_pmmx | 210 | 80 | 0.993 | 0.990 | 0.036 | 0.036 | 0 | 0.00 / 0.00 |
| dices | soft_pmode | 210 | 80 | 1.000 | 1.000 | 0.156 | 0.156 | 0 | 0.27 / 0.95 |
| dices990 | soft_pmm | 594 | 40 | 0.999 | 0.995 | 0.048 | 0.048 | 0 | 0.04 / 0.10 |
| dices990 | soft_pmmx | 594 | 40 | 0.999 | 0.985 | 0.042 | 0.042 | 102 | 0.00 / 0.00 |
| dices990 | soft_pmode | 594 | 40 | 1.000 | 1.000 | 0.135 | 0.135 | 0 | 0.23 / 1.00 |
| emobank_reader_v5 | soft_pmm | 1800 | 4 | 0.846 | 0.135 | 0.500 | 0.068 | 0 | 0.00 / 0.00 |
| emobank_reader_v5 | soft_pmmx | 1800 | 4 | 0.846 | 0.135 | 0.500 | 0.068 | 0 | 0.00 / 0.00 |
| emobank_reader_v5 | soft_pmode | 1800 | 4 | 0.999 | 0.999 | 0.314 | 0.313 | 0 | 0.39 / 1.50 |
| hs2_help5 | soft_pmm | 2870 | 3 | 0.456 | 0.280 | 0.667 | 0.186 | 0 | 0.00 / 0.00 |
| hs2_help5 | soft_pmmx | 2870 | 3 | 0.456 | 0.280 | 0.667 | 0.186 | 0 | 0.00 / 0.00 |
| hs2_help5 | soft_pmode | 2870 | 3 | 1.000 | 1.000 | 0.390 | 0.390 | 0 | 0.55 / 1.33 |
| popquorn_off8 | soft_pmm | 819 | 6 | 0.694 | 0.638 | 0.342 | 0.218 | 0 | 0.00 / 0.00 |
| popquorn_off8 | soft_pmmx | 819 | 6 | 0.694 | 0.638 | 0.342 | 0.218 | 0 | 0.00 / 0.00 |
| popquorn_off8 | soft_pmode | 819 | 6 | 1.000 | 1.000 | 0.295 | 0.295 | 0 | 0.48 / 2.00 |
| popquorn_pol5 | soft_pmm | 2214 | 4 | 0.664 | 0.417 | 0.500 | 0.209 | 0 | 0.00 / 0.00 |
| popquorn_pol5 | soft_pmmx | 2214 | 4 | 0.664 | 0.417 | 0.500 | 0.209 | 0 | 0.00 / 0.00 |
| popquorn_pol5 | soft_pmode | 2214 | 4 | 1.000 | 1.000 | 0.335 | 0.335 | 0 | 0.53 / 1.75 |
| scalabrino | soft_pmm | 74 | 6 | 0.698 | 0.509 | 0.340 | 0.173 | 0 | 0.00 / 0.00 |
| scalabrino | soft_pmmx | 74 | 6 | 0.698 | 0.509 | 0.340 | 0.173 | 0 | 0.00 / 0.00 |
| scalabrino | soft_pmode | 74 | 6 | 0.991 | 0.991 | 0.277 | 0.274 | 0 | 0.37 / 1.33 |
| summeval_coherence8 | soft_pmm | 960 | 6 | 0.863 | 0.728 | 0.378 | 0.273 | 0 | 0.00 / 0.00 |
| summeval_coherence8 | soft_pmmx | 960 | 6 | 0.863 | 0.728 | 0.378 | 0.273 | 0 | 0.00 / 0.00 |
| summeval_coherence8 | soft_pmode | 960 | 6 | 1.000 | 1.000 | 0.291 | 0.291 | 0 | 0.40 / 1.67 |
| summeval_relevance8 | soft_pmm | 960 | 6 | 0.824 | 0.651 | 0.383 | 0.248 | 0 | 0.00 / 0.00 |
| summeval_relevance8 | soft_pmmx | 960 | 6 | 0.824 | 0.651 | 0.383 | 0.248 | 0 | 0.00 / 0.00 |
| summeval_relevance8 | soft_pmode | 960 | 6 | 1.000 | 1.000 | 0.289 | 0.289 | 0 | 0.36 / 1.67 |


## T3b. LoRA 7B, SummEval coherence — CORRECTED OPTIMIZER/ASSIGNMENT BLOCK (frozen analysis_block_summeval.py; Qwen2.5-7B-Instruct; split 0). Three optimizer seeds, each paired with one item-assignment seed (2000/1000, 2001/2501, 2002/2502), across three fixed expert folds; roster chen / perm / perm_mode, histogram-class matching. The class-level matching flow and aggregate dose are deterministic given cell class sizes; seeds change item-level assignments within that flow (29–31 % of training items receive a different target between seeds). Intervals are 95 % percentile intervals from a crossed bootstrap over the three joint seed clusters, calibration documents with map refitting, and test documents; expert folds, split, evaluator set and base family are fixed. With only three seed clusters, intervals should be interpreted cautiously. Estimands: RAW primary | COMMON map (fixed three-arm roster) | ARM-specific. n_test_docs = 30 (480 rows), n_cal_docs = 10, B = 10,000.
| contrast | RAW | common | arm-specific | seeds (raw) | folds (raw) |
|---|---|---|---|---|---|
| perm − chen (mode+mean-preserving donor replacement) | **−0.0001 [−0.0011, +0.0011]** | +0.0000 [−0.0006, +0.0008] | +0.0003 [−0.0015, +0.0022] | −0.0007 / +0.0007 / −0.0002 | −0.0011 / +0.0000 / +0.0009 |
| perm_mode − chen (mode-only) | **+0.0120 [+0.0086, +0.0155]** | +0.0077 [+0.0053, +0.0109] | +0.0084 [+0.0051, +0.0121] | +0.0095 / +0.0130 / +0.0136 | +0.0172 / +0.0116 / +0.0073 |
| perm_mode − perm | +0.0121 [+0.0091, +0.0150] | +0.0077 [+0.0053, +0.0107] | +0.0081 [+0.0050, +0.0115] | +0.0102 / +0.0123 / +0.0138 | +0.0183 / +0.0116 / +0.0064 |
| perm_mode − chen: common − raw | −0.0045 [−0.0074, −0.0015] | | | | |
| perm_mode − chen: arm − raw | −0.0039 [−0.0077, −0.0002] | | | | |
Reading (Codex round 11 wording). On SummEval coherence, mode-and-mean-preserving replacement changed 81 % of training targets at mean TV 0.35 and produced a near-zero raw contrast, −0.0001 with a 95 % crossed-bootstrap interval of [−0.0011, +0.0011]. Its 90 % interval [−0.00092, +0.00088] lay within the post hoc ±.001, ±.002 and ±.003 sensitivity bands (±.002 frozen after the seed-2000 folds had been seen); this is exploratory evidence of a small average effect, not a confirmatory equivalence result. Common-map and arm-specific point estimates were also small, although only their 90 % intervals under the post hoc ±.002 band were contained (common [−0.00050, +0.00067]; arm-specific [−0.00117, +0.00177]). The nine raw seed × fold cell estimates range from −0.0025 to +0.0019; only the seed and fold marginal averages are near zero — do NOT write "in every seed and fold" for the null. By contrast, mode-only replacement increased raw RPS by +0.0120 [+0.0086, +0.0155], with positive estimates in all nine observed seed × fold cells. On the truncated λ ≤ .5 grid, calibration attenuated the mode-only contrast (common − raw −0.0045 [−0.0074, −0.0015]); λ = .5 was selected in 52.8 % of bootstrap fit events pooled over common and arm-specific fits (not independent observations) — Extended-grid sensitivity (λ ≤ .9, B = 4,000, analysis_block_summeval_lamext.json): λ = .9 selected in 3.0 % of fit events; perm_mode − chen common +0.0077 [+0.0041, +0.0109] (unchanged), arm-specific +0.0097 [+0.0058, +0.0128] (was +0.0084 on the λ ≤ .5 grid); common − raw −0.0049 [−0.0088, −0.0015] (robust), arm − raw −0.0028 [−0.0067, +0.0004] (no longer excludes 0). Reading: the common-map attenuation of the mode-only penalty is robust to the climatology grid; the arm-specific attenuation is grid-sensitive and should be described as 'attenuated by common-map calibration; arm-specific calibration gave a smaller, grid-dependent attenuation'. perm − chen is unaffected (raw −0.0001 [−0.0010, +0.0011]; common +0.0000; arm +0.0003 [−0.0015, +0.0025]). Dose certificates (every cell): perm changed 0.814 / 0.826 / 0.805 (folds 0–2, identical across seeds by construction), mean TV 0.351 / 0.335 / 0.345, n_tv_zero = 0; perm_mode changed 1.000, TV 0.319 / 0.296 / 0.302. Scope: one split, one base family; the three realisations couple a new optimizer realisation with a new item-level assignment under the same deterministic class-flow rule and cannot separate optimizer from assignment variability, nor test alternative class-pairing rules or dose patterns.
Superseded vector-matched single-seed row (s0_vecmatch; perm dose 0.73): perm − chen −0.0006 [−0.0012, +0.0001]; perm_mode − chen +0.0112 [+0.0083, +0.0143] — appendix audit row only. Other seed-2000 arms (hard, mean2, proto; unaffected by matching): hard − chen +0.0186 [+0.0141, +0.0229] raw / +0.0075 arm; chen − mean2 +0.0033 raw / −0.0013 arm; chen − proto −0.0122 raw.

## T3c. LoRA 7B, POPQUORN offensiveness — SECOND END-TO-END BLOCK (analysis_block_popquorn.py, adapted from the frozen SummEval analysis before any POPQUORN output existed; Qwen2.5-7B-Instruct; split 0; 1,366 items × 8 annotation positions, K = 5; train/calib/test 819/137/410 items). Same design as T3b: three optimizer seeds paired with item-assignment seeds (2000/1000, 2001/2501, 2002/2502) × three fixed position folds (evaluator = position 0/1/2; targets = the other 7), roster chen / perm / perm_mode, histogram-class matching, 2 epochs. Items are their own groups, so calibration and test resampling are item-level. Crossed bootstrap over seed clusters, calibration items (with map refitting) and test items; B = 10,000. Dose: perm changed 68.7–71.7 % of training targets, TV among changed 0.295–0.301, TV over all items 0.203–0.216, |Δmean| = 0, zero-TV pairs 0; perm_mode changed 100 %, TV 0.276–0.288.
| contrast | RAW | common | arm-specific | seeds (raw) | folds (raw) |
|---|---|---|---|---|---|
| perm − chen (mode+mean-preserving donor replacement) | **+0.0000 [−0.0009, +0.0009]** | +0.0000 [−0.0007, +0.0008] | −0.0000 [−0.0009, +0.0008] | −0.0002 / −0.0002 / +0.0005 | +0.0000 / −0.0002 / +0.0003 |
| perm_mode − chen (mode-only) | **+0.0029 [+0.0009, +0.0050]** | +0.0039 [+0.0022, +0.0060] | +0.0034 [+0.0016, +0.0053] | +0.0028 / +0.0024 / +0.0036 | +0.0030 / +0.0022 / +0.0037 |
| perm_mode − perm | +0.0029 [+0.0009, +0.0050] | +0.0038 [+0.0021, +0.0059] | +0.0035 [+0.0017, +0.0053] | +0.0030 / +0.0027 / +0.0031 | +0.0030 / +0.0023 / +0.0034 |
| perm_mode − chen: common − raw | +0.0011 [+0.0002, +0.0022] | | | | |
| perm_mode − chen: arm − raw | +0.0005 [−0.0007, +0.0018] | | | | |
Reading. The SummEval pattern replicates on a second dataset: mode-and-mean-preserving replacement of ~70 % of training targets (TV 0.30 among changed) gives a raw contrast of +0.0000 [−0.0009, +0.0009] (nine seed–fold cells −0.0017 … +0.0011; inside ±.001 by the 90 % CI criterion), while mode-only replacement raises RPS by +0.0029 [+0.0009, +0.0050], positive in all nine cells (+0.0001 … +0.0054). The mode-only penalty is about a quarter of SummEval's (+0.0120); POPQUORN offensiveness is floor-heavy (58 % of all ratings, 58–59 % of each evaluator position, at level 1), so mode-only replacement moves less location mass — a descriptive observation, not a tested explanation. Unlike SummEval, calibration does not shrink the mode-only penalty here (common − raw +0.0011). chen raw RPS per cell 0.118–0.124 (global-marginal baseline 0.148 on fold 0). Boundary hits of the calibration grid: 0 / 253,404 refits.
Rater-aware sensitivity (Codex round 16; `sensitivity_popquorn_users.py`). The loader assigns each item's ratings to positions by a seeded permutation and drops POPQUORN's user ids, so position folds hold out a *rating*, not a person: replaying the loader recovers the users exactly (262 distinct), and 100 % of the 201–205 test-evaluator users per fold also rate training targets. This is not input leakage (the judge never sees identity), but the T3c intervals condition on the realised finite rater panel. A pigeonhole item × user × seed bootstrap of the RAW estimand (B = 10,000; calibration maps not refitted; 255 evaluator users) widens the intervals: perm − chen +0.0000 [−0.0014, +0.0015] (90 % [−0.0012, +0.0013]); perm_mode − chen +0.0029 [−0.0004, +0.0065] (90 % [+0.0001, +0.0059]); perm_mode − perm +0.0029 [−0.0006, +0.0066]. Under rater-level resampling the POPQUORN mode-only penalty is directionally consistent (9/9 cells positive) but its 95 % interval includes 0, and the mode+mean contrast no longer falls inside ±.001. The pigeonhole bootstrap is conservative. SummEval is unaffected (its folds hold out persistent experts).

## T7. G × R check of the exploratory location explanation (heads; 18 cfgs per panel; histogram-class matching; group-disjoint splits). G = within-mode gain in location tracking from the item link (ρ_within(μ̂_soft, μ_train | z) − ρ_within(μ̂_pmode, μ_train | z), validation items); R = within-mode relevance of the training mean for held-out raters (ρ_within(μ_train, y_eval | z)); E = RPS(soft_pmode) − RPS(soft) on test items. PRESPECIFIED (PAPER_OUTLINE, after Codex round 6) as a held-out test on BW, DICES, HelpSteer2 and Scalabrino; the SummEval panels are the hypothesis-generating panels (the former commit panels were removed from the paper). No indifference region was prespecified. Panels are not independent (two SummEval criteria share documents).
| panel | role | G | R | G×R | E (pmode − soft, RPS) | sign |
|---|---|---|---|---|---|---|
| DICES Q_overall | held-out | +0.145±0.040 | +0.247±0.010 | +0.037±0.010 | +0.0039±0.0014 | nominally concordant in the prespecified stream; NOT RNG-robust (probe_mean2 streams gave −0.0015±0.0008 and +0.0022±0.0011) |
| HelpSteer2 helpfulness | held-out | +0.011±0.006 | +0.046±0.006 | +0.001±0.000 | +0.0003±0.0003 | same sign, but both ≈ 0 and no indifference region was prespecified — not a success |
| Buse–Weimer | held-out | +0.011±0.044 | +0.241±0.022 | +0.003±0.009 | −0.0009±0.0011 | discordant (both ≈ 0) |
| Scalabrino | held-out | −0.064±0.058 | +0.105±0.052 | −0.008±0.009 | +0.0017±0.0011 | discordant (both within 1 SEM of 0) |
| SummEval coherence | generating | +0.205±0.027 | +0.438±0.019 | +0.089±0.013 | +0.0061±0.0009 | concordant (generating) |
| SummEval relevance | generating | +0.169±0.023 | +0.306±0.016 | +0.054±0.009 | +0.0035±0.0006 | concordant (generating) |
**Held-out result (the prespecified test): the predicted sign occurred in 2/4 panels in the prespecified realisation, but one of those two — DICES — changed sign across otherwise comparable RNG streams, and the other (HelpSteer2) is a both-≈-0 case without a prespecified indifference region; Spearman(G×R, E) = 0.20. The held-out table therefore provides no robust validation of G×R; it remains an exploratory diagnostic.**  Paper sentence (Codex round 9): "On the four panels reserved for the prespecified check, the predicted sign held in two and the cross-panel Spearman correlation was 0.20. Both discordant cases had small G×R and small RPS contrasts, but no indifference region was prespecified. 55. Thus the results are qualitatively compatible with the proposed location account but do not validate a necessary condition or an effect-size predictor." G×R is therefore an exploratory explanatory diagnostic. The ">0.025 vs <0.01" split is post hoc and outcome-defined; it may be shown descriptively only.

## T4. Semi-synthetic sanity check (`_v8`: histogram-class matching AND injection applied separately within the realised training-position and evaluation-position panels, so mode and mean are preserved within each subset — Codex round 14; heads; 30 cfgs; D = Spearman of predicted vs reference disagreement; ± = descriptive SEM over paired configurations)
| panel | oracle resid gap (oracle_soft − oracle_mean2, D) | soft − mean2 (D) | pmm − soft (D) | learnable fraction (soft−mean2)/(oracle gap) |
|---|---|---|---|---|
| Buse–Weimer | +0.571±0.016 | +0.269±0.039 | -0.229±0.035 | 0.47 |
| Scalabrino | +0.023±0.015 (no positive oracle gap under this injection: no positive-control evidence) | -0.021±0.026 | +0.017±0.032 | — |
| POPQUORN offensiveness | -0.040±0.004 (no positive oracle gap under this injection: no positive-control evidence) | -0.002±0.003 | +0.007±0.002 | — |
| CSC sarcasm | D undefined (a single held-out annotation position gives no reference disagreement) | — | — | — |
Earlier versions (`_v6`/`_v7`) injected on the full annotation row before the position split, so mode and mean were not preserved within the realised panels (Codex round 14); they are superseded. Under the subset-wise injection the Scalabrino and POPQUORN offensiveness oracle gaps are ≈ 0 or negative (the feature-aligned injection is not recoverable from the reference positions there), and CSC's single held-out position leaves D undefined, so only Buse–Weimer supplies positive-control evidence.


## T5 (ChaosNLI MNLI). Nominal decomposition (heads, `_v6`: histogram-class matching, full dose certificate; m training annotations; KL to a FIXED 50-annotation reference panel; 9 configurations = 3 optimizer seeds × 3 item splits, annotation subsample tied to the item split; ± = descriptive SEM over the 9 dependent configurations). Constraint-certified `zc`/`pzc` targets (q_z = c, q_k ≤ c; 0 violations). Dose columns: donor-mapped fraction / support / mean final TV over all training items [effective-change sensitivity, TV > 1e-6]; zero donor-TV pairs = 0 in every configuration.
| m | soft − zc (KL) | soft − cond (KL) | soft − shrunk (KL) | pzc − soft (KL) | pmode − soft (KL) | resid ρ: soft − zc | resid ρ: pzc − soft | pzc dose (mapped / support / final TV-all) [eff. change] | pmode dose (changed / TV all) | fidelity resid ρ: m-hist / zc |
|---|---|---|---|---|---|---|---|---|---|---|
| 5 | -0.010±0.001 | -0.007±0.001 | -0.000±0.001 | +0.029±0.001 | +0.029±0.003 | +0.057±0.008 | -0.134±0.010 | 0.555 / 0.79 / 0.141 [0.555] | 1.00 / 0.299 | 0.54 / 0.36 |
| 10 | -0.008±0.001 | -0.006±0.001 | +0.001±0.001 | +0.018±0.001 | +0.021±0.003 | +0.056±0.010 | -0.091±0.011 | 0.784 / 0.94 / 0.123 [0.721] | 1.00 / 0.243 | 0.65 / 0.47 |
| 20 | -0.011±0.001 | -0.012±0.001 | -0.002±0.001 | +0.017±0.001 | +0.020±0.002 | +0.055±0.009 | -0.089±0.009 | 0.977 / 0.99 / 0.103 [0.828] | 1.00 / 0.209 | 0.73 / 0.50 |
| 50 | -0.014±0.002 | -0.013±0.001 | -0.002±0.002 | +0.016±0.002 | +0.020±0.002 | +0.064±0.009 | -0.052±0.011 | 0.997 / 1.00 / 0.088 [0.923] | 1.00 / 0.199 | 0.81 / 0.51 |

## T5 (ChaosNLI SNLI). Nominal decomposition (heads, `_v7`: histogram-class matching, full dose certificate; m training annotations; KL to a FIXED 50-annotation reference panel; 9 configurations = 3 optimizer seeds × 3 item splits, annotation subsample tied to the item split; ± = descriptive SEM over the 9 dependent configurations). Constraint-certified `zc`/`pzc` targets (q_z = c, q_k ≤ c; 0 violations). Dose columns: donor-mapped fraction / support / mean final TV over all training items [effective-change sensitivity, TV > 1e-6]; zero donor-TV pairs = 0 in every configuration.
| m | soft − zc (KL) | soft − cond (KL) | soft − shrunk (KL) | pzc − soft (KL) | pmode − soft (KL) | resid ρ: soft − zc | resid ρ: pzc − soft | pzc dose (mapped / support / final TV-all) [eff. change] | pmode dose (changed / TV all) | fidelity resid ρ: m-hist / zc |
|---|---|---|---|---|---|---|---|---|---|---|
| 5 | -0.022±0.001 | -0.021±0.002 | -0.002±0.002 | +0.052±0.003 | +0.053±0.006 | +0.069±0.009 | -0.226±0.017 | 0.411 / 0.65 / 0.108 [0.411] | 1.00 / 0.289 | 0.50 / 0.25 |
| 10 | -0.021±0.002 | -0.017±0.003 | +0.001±0.002 | +0.041±0.002 | +0.041±0.004 | +0.086±0.010 | -0.205±0.016 | 0.657 / 0.82 / 0.099 [0.583] | 1.00 / 0.236 | 0.60 / 0.33 |
| 20 | -0.023±0.002 | -0.021±0.002 | +0.001±0.001 | +0.036±0.003 | +0.045±0.003 | +0.099±0.007 | -0.158±0.016 | 0.894 / 0.91 / 0.088 [0.656] | 1.00 / 0.216 | 0.66 / 0.34 |
| 50 | -0.027±0.002 | -0.024±0.001 | +0.002±0.001 | +0.032±0.001 | +0.045±0.003 | +0.112±0.009 | -0.134±0.013 | 0.972 / 0.97 / 0.076 [0.769] | 1.00 / 0.195 | 0.72 / 0.36 |

## T5 (ChaosNLI αNLI (K = 2)). Nominal decomposition (heads, `_v7`: histogram-class matching, full dose certificate; m training annotations; KL to a FIXED 50-annotation reference panel; 9 configurations = 3 optimizer seeds × 3 item splits, annotation subsample tied to the item split; ± = descriptive SEM over the 9 dependent configurations). Constraint-certified `zc`/`pzc` targets (q_z = c, q_k ≤ c; 0 violations). Dose columns: donor-mapped fraction / support / mean final TV over all training items [effective-change sensitivity, TV > 1e-6]; zero donor-TV pairs = 0 in every configuration.
| m | soft − zc (KL) | soft − cond (KL) | soft − shrunk (KL) | pzc − soft (KL) | pmode − soft (KL) | resid ρ: soft − zc | resid ρ: pzc − soft | pzc dose (mapped / support / final TV-all) [eff. change] | pmode dose (changed / TV all) | fidelity resid ρ: m-hist / zc |
|---|---|---|---|---|---|---|---|---|---|---|
| 5 | +0.005±0.004 | -0.000±0.002 | +0.007±0.006 | -0.001±0.006 | +0.005±0.005 | +nan±nan | +nan±nan | 0.000 / 0.00 / 0.000 [0.000] | 0.72 / 0.195 | nan / 0.26 |
| 10 | +0.002±0.006 | +0.006±0.007 | +0.006±0.007 | -0.004±0.004 | +0.008±0.006 | +nan±nan | +nan±nan | 0.056 / 0.06 / 0.000 [0.000] | 0.98 / 0.209 | nan / 0.29 |
| 20 | -0.005±0.003 | +0.003±0.005 | +0.001±0.005 | +0.002±0.005 | +0.004±0.006 | +nan±nan | +nan±nan | 0.472 / 0.61 / 0.000 [0.000] | 1.00 / 0.184 | nan / 0.34 |
| 50 | -0.005±0.005 | +0.006±0.005 | +0.002±0.007 | +0.000±0.002 | +0.002±0.009 | +nan±nan | +nan±nan | 0.830 / 0.83 / 0.000 [0.000] | 1.00 / 0.132 | nan / 0.30 |


## T6. Stage A — rater conditioning (heads, DICES, 30 cfgs)
unseen-rater RPS at k = 0/4/16/64 support ratings: history-only prior .221/.208/.192/.185; item-only .219; additive .219/.200/.187/.184; interactive .221/.201/.189/.186; seen-rater ID ceiling .197 (trained on and evaluated against the training-rater population — not comparable to the unseen-rater rows). interactive − additive on unseen-rater RPS at k=64: +0.0017±0.0012; on population RPS: +0.0005±0.0009; interaction scramble Δ ≈ 0.

## T9. Finite-rater annotation-side analysis (learner-free; FINITE_RATER_PROTOCOL.md with amendments 1–2; finite_rater.py, finite_rater_summary.py, finite_rater_moderator.py). Scores: RPS (ordinal) / Brier (nominal) against held-out ratings. A1 = S(raw a-rater histogram) − S(T-only comparator): negative ⇔ the raw histogram's residual shape helps predict a new rater. Primary comparator = response-based smoother within mode (does not reproduce noisy T); A1x = exact-T comparator (reproduces mode and mean exactly; audit-aligned). Exact identity A1 = M − 2X with X the cross-panel agreement of the residual; ρ = X/M > ½ ⇔ A1 < 0. N = multinomial noise of h1, Δ = N − A1 = error of the T-comparator (not a residual-information quantity). A2 = annotation-side analogue of the audit's donor replacement (ITT). Item-cluster bootstrap B = 500 with nuisance refitting; rater-pool-conditional on persistent-rater panels.

### (a) a = m − 1 (one held-out rating per item, position drawn per item; 20 repetitions; item-cluster bootstrap B = 500)
| panel | m | A1 (smoothed T-comparator) | A1x (exact-T comparator) | M | X | ρ = X/M | N | Δ = N − A1 | A2 ITT (pmmx/pzc donor) [changed, TV] | heads pmmx − soft | LoRA perm − chen |
|---|---|---|---|---|---|---|---|---|---|---|---|
| SummEval coherence | 8 | +0.0075 [+0.0063, +0.0094] | +0.0015 [+0.0007, +0.0022] | 0.0140 | +0.0033 [+0.0024, +0.0037] | 0.23 [0.17, 0.26] | 0.0166 | 0.0091 | +0.0044 [+0.0031, +0.0063] [0.87, 0.32] | -0.0010±0.0003 | -0.0001 [-0.0011, +0.0011] |
| SummEval relevance | 8 | +0.0045 [+0.0032, +0.0061] | +0.0008 [+0.0000, +0.0014] | 0.0113 | +0.0034 [+0.0027, +0.0041] | 0.30 [0.24, 0.35] | 0.0140 | 0.0096 | +0.0034 [+0.0032, +0.0058] [0.79, 0.31] | — | — |
| POPQUORN offensiveness | 8 | +0.0056 [+0.0046, +0.0072] | +0.0030 [+0.0023, +0.0035] | 0.0133 | +0.0039 [+0.0032, +0.0042] | 0.29 [0.24, 0.32] | 0.0169 | 0.0112 | -0.0000 [-0.0008, +0.0018] [0.69, 0.30] | +0.0002±0.0002 | +0.0000 [-0.0009, +0.0009] |
| POPQUORN politeness | 5 | +0.0154 [+0.0149, +0.0169] | +0.0045 [+0.0038, +0.0050] | 0.0183 | +0.0015 [+0.0010, +0.0017] | 0.08 [0.05, 0.09] | 0.0308 | 0.0153 | +0.0004 [-0.0006, +0.0014] [0.42, 0.50] | +0.0002±0.0002 | — |
| CSC sarcasm | 6 | +0.0132 [+0.0119, +0.0158] | +0.0052 [+0.0044, +0.0059] | 0.0189 | +0.0028 [+0.0019, +0.0033] | 0.15 [0.10, 0.17] | 0.0275 | 0.0143 | +0.0004 [-0.0013, +0.0011] [0.72, 0.41] | +0.0002±0.0003 | — |
| Scalabrino readability | 9 | -0.0034 [-0.0056, +0.0088] | +0.0029 [+0.0015, +0.0058] | 0.0213 | +0.0123 [+0.0065, +0.0142] | 0.58 [0.30, 0.64] | 0.0160 | 0.0194 | -0.0004 [-0.0038, +0.0030] [0.69, 0.28] | -0.0003±0.0007 | — |
| HelpSteer2 helpfulness | 5 | +0.0264 [+0.0254, +0.0283] | +0.0038 [+0.0033, +0.0043] | 0.0297 | +0.0017 [+0.0012, +0.0018] | 0.06 [0.04, 0.06] | 0.0426 | 0.0162 | +0.0016 [+0.0006, +0.0026] [0.45, 0.50] | +0.0005±0.0001 | — |
| EmoBank valence | 5 | +0.0082 [+0.0071, +0.0095] | +0.0004 [-0.0000, +0.0008] | 0.0126 | +0.0022 [+0.0017, +0.0023] | 0.18 [0.13, 0.19] | 0.0175 | 0.0094 | +0.0018 [+0.0012, +0.0026] [0.14, 0.50] | +0.0006±0.0001 | — |
| Buse–Weimer readability | 121 | -0.0138 [-0.0173, -0.0051] | +0.0007 [-0.0004, +0.0011] | 0.0134 | +0.0136 [+0.0088, +0.0162] | 1.01 [0.68, 1.16] | 0.0011 | 0.0149 | -0.0011 [-0.0015, +0.0013] [0.89, 0.08] | -0.0024±0.0007 | — |
| DICES-350 | 104 | -0.0046 [-0.0060, -0.0020] | +0.0001 [-0.0001, +0.0002] | 0.0047 | +0.0047 [+0.0034, +0.0053] | 0.99 [0.67, 1.35] | 0.0018 | 0.0064 | -0.0002 [-0.0003, +0.0005] [1.00, 0.03] | -0.0018±0.0007 | — |
| DICES-990 | 60 | -0.0017 [-0.0025, -0.0005] | +0.0001 [+0.0000, +0.0003] | 0.0028 | +0.0023 [+0.0018, +0.0027] | 0.79 [0.57, 1.02] | 0.0030 | 0.0046 | -0.0000 [-0.0002, +0.0003] [1.00, 0.03] | -0.0001±0.0002 | — |
| ChaosNLI MNLI | 100 | -0.0226 [-0.0261, -0.0193] | -0.0210 [-0.0239, -0.0175] | 0.0240 | +0.0233 [+0.0209, +0.0254] | 0.97 [0.92, 1.06] | 0.0046 | 0.0272 | +0.0386 [+0.0284, +0.0440] [1.00, 0.09] | — | — |
| ChaosNLI SNLI | 100 | -0.0214 [-0.0239, -0.0176] | -0.0193 [-0.0219, -0.0160] | 0.0206 | +0.0210 [+0.0187, +0.0228] | 1.02 [0.92, 1.07] | 0.0035 | 0.0249 | +0.0308 [+0.0271, +0.0404] [0.99, 0.07] | — | — |

### (b) dense-panel curves (a ratings in P1, 20 held-out ratings in P2) and the prospective prediction test

chaosnli_mnli (m = 100, nominal/Brier)
| a | A1 [95 % CI] | A1x | ρ | N | Δ |
|---|---|---|---|---|---|
| 2 | +0.1326 [+0.1276, +0.1403] | +0.0027 | 0.07 | 0.2293 | 0.0966 |
| 3 | +0.0667 [+0.0626, +0.0706] | -0.0072 | 0.17 | 0.1524 | 0.0857 |
| 5 | +0.0206 [+0.0193, +0.0247] | -0.0128 | 0.33 | 0.0922 | 0.0716 |
| 8 | +0.0031 [+0.0016, +0.0053] | -0.0123 | 0.46 | 0.0576 | 0.0545 |
| 10 | -0.0031 [-0.0049, -0.0014] | -0.0138 | 0.55 | 0.0461 | 0.0493 |
| 15 | -0.0121 [-0.0137, -0.0104] | -0.0172 | 0.71 | 0.0307 | 0.0428 |
| 20 | -0.0138 [-0.0158, -0.0127] | -0.0170 | 0.77 | 0.0230 | 0.0368 |
| 30 | -0.0168 [-0.0184, -0.0152] | -0.0180 | 0.87 | 0.0154 | 0.0321 |
| 40 | -0.0180 [-0.0196, -0.0162] | -0.0189 | 0.91 | 0.0115 | 0.0295 |
fit on a ∈ [2, 5, 10, 20, 40]: v = 0.4603, δ∞ = 0.0329, c = 0.1365; observed A1 sign change at a ≈ 9.0
  a =  3: predicted +0.0751  observed +0.0667 [+0.0626, +0.0706]  NOT covered
  a =  8: predicted +0.0076  observed +0.0031 [+0.0016, +0.0053]  NOT covered
  a = 15: predicted -0.0113  observed -0.0121 [-0.0137, -0.0104]  covered
  a = 30: predicted -0.0221  observed -0.0168 [-0.0184, -0.0152]  NOT covered
Δ_ref (T from 40 independent ratings) = +0.0299 [+0.0278, +0.0314]; implied reference crossover v/Δ_ref ≈ 15.4 raters

chaosnli_snli (m = 100, nominal/Brier)
| a | A1 [95 % CI] | A1x | ρ | N | Δ |
|---|---|---|---|---|---|
| 2 | +0.0652 [+0.0604, +0.0704] | -0.0020 | 0.10 | 0.1716 | 0.1063 |
| 3 | +0.0259 [+0.0227, +0.0289] | -0.0083 | 0.26 | 0.1139 | 0.0880 |
| 5 | +0.0010 [+0.0000, +0.0040] | -0.0128 | 0.49 | 0.0690 | 0.0680 |
| 8 | -0.0050 [-0.0068, -0.0037] | -0.0111 | 0.61 | 0.0427 | 0.0477 |
| 10 | -0.0088 [-0.0101, -0.0071] | -0.0126 | 0.70 | 0.0342 | 0.0430 |
| 15 | -0.0139 [-0.0156, -0.0123] | -0.0158 | 0.83 | 0.0229 | 0.0368 |
| 20 | -0.0141 [-0.0158, -0.0128] | -0.0151 | 0.86 | 0.0171 | 0.0312 |
| 30 | -0.0159 [-0.0172, -0.0141] | -0.0165 | 0.92 | 0.0114 | 0.0273 |
| 40 | -0.0167 [-0.0178, -0.0147] | -0.0172 | 0.95 | 0.0085 | 0.0252 |
fit on a ∈ [2, 5, 10, 20, 40]: v = 0.3428, δ∞ = 0.0252, c = 0.1690; observed A1 sign change at a ≈ 5.5
  a =  3: predicted +0.0328  observed +0.0259 [+0.0227, +0.0289]  NOT covered
  a =  8: predicted -0.0034  observed -0.0050 [-0.0068, -0.0037]  NOT covered
  a = 15: predicted -0.0136  observed -0.0139 [-0.0156, -0.0123]  covered
  a = 30: predicted -0.0194  observed -0.0159 [-0.0172, -0.0141]  NOT covered
Δ_ref (T from 40 independent ratings) = +0.0250 [+0.0229, +0.0267]; implied reference crossover v/Δ_ref ≈ 13.7 raters

dices (m = 104, ordinal/RPS)
| a | A1 [95 % CI] | A1x | ρ | N | Δ |
|---|---|---|---|---|---|
| 2 | +0.0640 [+0.0572, +0.0698] | +0.0000 | 0.03 | 0.0906 | 0.0266 |
| 3 | +0.0374 [+0.0321, +0.0416] | +0.0005 | 0.03 | 0.0622 | 0.0249 |
| 5 | +0.0169 [+0.0149, +0.0198] | +0.0006 | 0.07 | 0.0371 | 0.0202 |
| 8 | +0.0087 [+0.0069, +0.0099] | +0.0010 | 0.12 | 0.0231 | 0.0144 |
| 10 | +0.0059 [+0.0048, +0.0071] | +0.0009 | 0.13 | 0.0186 | 0.0127 |
| 15 | +0.0029 [+0.0023, +0.0038] | +0.0007 | 0.19 | 0.0124 | 0.0095 |
| 20 | +0.0018 [+0.0012, +0.0023] | +0.0005 | 0.25 | 0.0093 | 0.0075 |
| 30 | +0.0007 [+0.0004, +0.0012] | +0.0003 | 0.35 | 0.0062 | 0.0055 |
| 40 | +0.0003 [+0.0000, +0.0006] | +0.0002 | 0.41 | 0.0046 | 0.0043 |
fit on a ∈ [2, 5, 10, 20, 40]: v = 0.1848, δ∞ = 0.0065, c = 0.0442; observed A1 sign change at a ≈ none in range
  a =  3: predicted +0.0403  observed +0.0374 [+0.0321, +0.0416]  covered
  a =  8: predicted +0.0110  observed +0.0087 [+0.0069, +0.0099]  NOT covered
  a = 15: predicted +0.0028  observed +0.0029 [+0.0023, +0.0038]  covered
  a = 30: predicted -0.0019  observed +0.0007 [+0.0004, +0.0012]  NOT covered
Δ_ref (T from 40 independent ratings) = +0.0042 [+0.0036, +0.0050]; implied reference crossover v/Δ_ref ≈ 43.5 raters

dices990 (m = 60, ordinal/RPS)
| a | A1 [95 % CI] | A1x | ρ | N | Δ |
|---|---|---|---|---|---|
| 2 | +0.0627 [+0.0598, +0.0673] | +0.0000 | 0.01 | 0.0863 | 0.0236 |
| 3 | +0.0380 [+0.0349, +0.0399] | +0.0002 | 0.02 | 0.0579 | 0.0199 |
| 5 | +0.0183 [+0.0166, +0.0196] | +0.0004 | 0.08 | 0.0348 | 0.0165 |
| 8 | +0.0090 [+0.0082, +0.0099] | +0.0008 | 0.07 | 0.0218 | 0.0128 |
| 10 | +0.0063 [+0.0057, +0.0071] | +0.0008 | 0.09 | 0.0175 | 0.0111 |
| 15 | +0.0033 [+0.0029, +0.0038] | +0.0006 | 0.13 | 0.0116 | 0.0083 |
| 20 | +0.0021 [+0.0018, +0.0024] | +0.0005 | 0.17 | 0.0087 | 0.0066 |
| 30 | +0.0010 [+0.0008, +0.0013] | +0.0003 | 0.24 | 0.0058 | 0.0048 |
| 40 | +0.0005 [+0.0004, +0.0008] | +0.0002 | 0.31 | 0.0044 | 0.0038 |
fit on a ∈ [2, 5, 10, 20, 40]: v = 0.1739, δ∞ = 0.0055, c = 0.0389; observed A1 sign change at a ≈ none in range
  a =  3: predicted +0.0395  observed +0.0380 [+0.0349, +0.0399]  covered
  a =  8: predicted +0.0114  observed +0.0090 [+0.0082, +0.0099]  NOT covered
  a = 15: predicted +0.0035  observed +0.0033 [+0.0029, +0.0038]  covered
  a = 30: predicted -0.0010  observed +0.0010 [+0.0008, +0.0013]  NOT covered
Δ_ref (T from 30 independent ratings) = +0.0048 [+0.0043, +0.0053]; implied reference crossover v/Δ_ref ≈ 36.5 raters

bw (m = 121, ordinal/RPS)
| a | A1 [95 % CI] | A1x | ρ | N | Δ |
|---|---|---|---|---|---|
| 2 | +0.0502 [+0.0436, +0.0550] | +0.0013 | 0.09 | 0.0678 | 0.0177 |
| 3 | +0.0294 [+0.0256, +0.0337] | +0.0089 | 0.10 | 0.0452 | 0.0158 |
| 5 | +0.0145 [+0.0118, +0.0169] | +0.0048 | 0.18 | 0.0275 | 0.0130 |
| 8 | +0.0072 [+0.0051, +0.0088] | +0.0036 | 0.24 | 0.0171 | 0.0099 |
| 10 | +0.0042 [+0.0031, +0.0063] | +0.0028 | 0.30 | 0.0137 | 0.0095 |
| 15 | +0.0011 [+0.0008, +0.0034] | +0.0018 | 0.43 | 0.0092 | 0.0081 |
| 20 | +0.0001 [-0.0014, +0.0012] | +0.0015 | 0.50 | 0.0069 | 0.0068 |
| 30 | -0.0007 [-0.0017, +0.0008] | +0.0011 | 0.57 | 0.0046 | 0.0053 |
| 40 | -0.0015 [-0.0019, +0.0003] | +0.0007 | 0.66 | 0.0035 | 0.0049 |
fit on a ∈ [2, 5, 10, 20, 40]: v = 0.1372, δ∞ = 0.0060, c = 0.0251; observed A1 sign change at a ≈ 20.8
  a =  3: predicted +0.0314  observed +0.0294 [+0.0256, +0.0337]  covered
  a =  8: predicted +0.0080  observed +0.0072 [+0.0051, +0.0088]  covered
  a = 15: predicted +0.0015  observed +0.0011 [+0.0008, +0.0034]  covered
  a = 30: predicted -0.0023  observed -0.0007 [-0.0017, +0.0008]  NOT covered
Δ_ref (T from 40 independent ratings) = +0.0045 [+0.0031, +0.0055]; implied reference crossover v/Δ_ref ≈ 30.4 raters

chaosnli_alphanli (m = 100, nominal/Brier)
| a | A1 [95 % CI] | A1x | ρ | N | Δ |
|---|---|---|---|---|---|
| 2 | +0.0188 [+0.0162, +0.0208] | +0.0000 | 0.01 | 0.0874 | 0.0686 |
| 5 | +0.0046 [+0.0039, +0.0049] | +0.0000 | 0.06 | 0.0353 | 0.0308 |
| 10 | +0.0014 [+0.0010, +0.0017] | +0.0000 | 0.21 | 0.0176 | 0.0161 |
| 20 | +0.0003 [+0.0001, +0.0004] | -0.0000 | 0.41 | 0.0088 | 0.0085 |

**Prediction test (prospective, Amendment 1 item 7):** coverage of the predicted A1 by the observed 95 % intervals — chaosnli_mnli 1/4; chaosnli_snli 1/4; dices 2/4; dices990 2/4; bw 3/4. ChaosNLI and DICES miss a = 8 and a = 30 (ChaosNLI also a = 3); Buse–Weimer misses only a = 30. The two-term approximation N = v/a, Δ = δ∞ + c/a is therefore not supported at this precision (discrete/noisy T and comparator adaptation); no model-based crossover is claimed. Empirical sign-change brackets of A1 (smoothed comparator, point estimates): MNLI a = 8–10, SNLI a = 5–8, Buse–Weimer a = 20–30 (95 % intervals include 0 from a = 20), none through a = 40 on DICES-350 and DICES-990. With the exact-T comparator (A1x) the residual-bearing histogram never wins on any dense ordinal panel through a = 40 (BW +0.0007 at a = 40), whereas on ChaosNLI it wins from a = 2–3. v/Δ_ref is a model-implied reference-panel benchmark only.

### (d) Prospectively specified secondary moderator: replicable bimodality (ordinal) / two-label concentration (nominal) — dense panels only
Four disjoint 10-rating subsets per item (P0 shape score B, P1 comparator T, P2/P3 cross-product δ); δ ~ β·B_std + N̂ + entropy(P0) + location-bin FE; R = 20 assignments, B = 500 group-bootstrap replicates.
| panel | β (per SD of B) [95 % CI] | δ by B tertile (low / mid / high) |
|---|---|---|
| dices | +0.00026 [-0.00380, +0.00270] | 0.0114 / 0.0133 / 0.0153 |
| dices990 | +0.00026 [-0.00177, +0.00199] | 0.0087 / 0.0118 / 0.0127 |
| bw | -0.00005 [-0.00294, +0.00277] | 0.0112 / 0.0095 / 0.0108 |
| chaosnli_mnli | +0.00199 [-0.00162, +0.00601] | 0.0435 / 0.0499 / 0.0575 |
| chaosnli_snli | +0.00563 [-0.00140, +0.01256] | 0.0238 / 0.0496 / 0.0635 |
| **pooled_ordinal** (inverse-variance) | +0.00019 [-0.00131, +0.00169] | |
| **pooled_nominal** (inverse-variance) | +0.00288 [-0.00050, +0.00626] | |

Reading: neither pooled β excludes 0 (ordinal +0.00019 [−0.00131, +0.00169]; nominal +0.00288 [−0.00050, +0.00626]); the raw tertile gradient on ChaosNLI does not survive the prespecified covariates. Replicable bimodality does not detectably moderate the residual's cross-panel agreement on these panels.
