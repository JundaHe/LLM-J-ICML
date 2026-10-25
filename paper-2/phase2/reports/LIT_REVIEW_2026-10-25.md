# Literature review refresh for the ICML push (2026-10-25)

Scope: work since the 2026-09-17 review (`paper-2/lit-review/`, 63 papers) and the 2026-10-12/23 novelty checks (`novelty/NOVELTY_REPORT.md`), focused on what an ICML reviewer will compare us to and on the two candidate extensions (residual decoding; reliability-shrunk targets).
Status tags: **[abs]** abstract/landing page read in this session; **[snip]** search snippet only (verify before citing).

## A. Closest work on *what soft labels teach* (direct competitors)
| paper | what it shows | delta to us |
|---|---|---|
| Gheibi & Ghazizadeh, *Same Target, Different Basins* (arXiv 2605.20642; **EIML workshop @ ICML 2026**) [abs] | hard-label delivery (multipass, stochastic label sampling) matches soft labels; **with few annotations per item hard-label delivery beats soft-label training, more so when the sparse empirical target is far from the full distribution**; shuffled-SLS control breaks the item↔distribution link; CIFAR-10H | Their sparse-annotation result is the image-classification cousin of our finite-rater finding (A1x > 0 at 5–9 raters). They do not decompose the distribution (mode/mean vs residual), give no dose certificates, no ordinal/LLM-judge setting, no cross-panel reliability. **Must be cited as concordant evidence and positioned as complementary**; our A/G analysis explains *why* (residual reliability ρ < ½). |
| Kohli, *Metric-Dependent Annotation Saturation* (2605.29797) [abs] | ChaosNLI subsampling: KL saturates by ~10 annotators, entropy correlation needs 20–50; soft labels beat smoothing | Nominal only; learner-side curves. Our finite-rater curves are learner-free, ordinal + nominal, and isolate the residual beyond mode/mean; consistent with their ~10–20 rater scale on ChaosNLI (our crossover 5–10, reference ~14–15). |
| Singh et al., *Distributions In, Distributions Out* (2511.14117) [abs] | soft labels: −32 % KL, +61 % entropy correlation vs hard | no decomposition; our audit says the ordinal gain is location + calibration |
| Pavlovic, Paun & Poesio (2605.18648, rev. Oct 2026) [abs] | human soft labels act mainly as calibration regularisers on hard items | supports our reading |
| Benito-Santos & Ghajari, *Beyond Averages* (EMNLP 2025) [abs] | full ordinal distribution beats the averaged score on STS | baseline is a point/mean target, not a mode+mean-matched distribution → compatible with location sufficiency; **reviewer will raise it** |
| Behrens & Zdeborová (ICLR 2026) [abs] | within-class reassignment of teacher soft labels (distillation) | teacher labels, memorisation; no exact mode+mean preservation |
| Chen et al., *Beyond Single-Point Judgment* (NeurIPS 2025, 2505.12301) [abs] | the distributional judge objective we audit | — |

## B. LLM-as-a-judge and human disagreement (2026)
- Li, Yu & Li, *How Many Humans Are 32 LLM Judges Worth?* (2609.21277, Sep 2026) [abs]: a 32-judge panel ≈ 2.3–3.8 humans (distributional) / 4.2–6.5 (spectral). Evaluation-side "effective number of raters" — natural companion to our finite-rater framing (how many *human* raters a training target needs).
- Ni et al., *Can reasoning help LLMs capture annotator disagreement?* (EACL 2026) [snip]; Wang et al. 2503.03064 (judgment-distribution inference) [snip]; Kohli *Nine Judges, Two Effective Votes* (2605.29800) [snip]; Steindl et al. NAPHA (2609.01073) [abs earlier]; *Reliability without Validity* (2606.19544) [snip]; IRT diagnosis of judges (2602.00521) [snip].
- Zhang et al., *Diverging Preferences* (ICML 2025, 2410.14632) [snip]: distributional RMs identify disagreement items weakly (AUROC .58–.65 with 3–5 raters) — consistent with low ρ at small m.

## C. Pluralistic alignment / preference distributions (positioning, not competitors)
- *Pairwise Calibrated Rewards for Pluralistic Alignment* (2506.06298) [snip]; *Hidden Consensus: Preference-Validity Compression* (2606.10569) [abs]: plural-valid answers collapsed by RLHF; *Welfare-Aware Preference Acquisition* (2610.19035) [snip]; MixDPO (2026) [snip]. Our message for this audience: with few raters, the *distributional* signal beyond location is mostly sampling noise on ordinal scales — pluralistic methods need either many raters or stable structure.

## D. Prior art for the candidate method (reliability-shrunk targets)
- Label smoothing as shrinkage / noise mitigation (Lukasik et al., ICML 2020) [snip]; class-conditional noise identifiability (Scott & Blanchard) [snip]; crowd soft-label aggregation for uncertainty under shift (PMC12148080) [snip]; noisy-label calibration with multiple unreliable labels (2610.19543, Oct 2026) [snip]; Ushio, Ishida & Sugiyama (ICLR 2026) — Bayes-error estimation with corrupted soft labels via isotonic calibration [abs]; Dawid–Skene / annotator models (classic).
- **Gap we found:** no work shrinks the *residual* of an empirical rating distribution toward a *statistic-preserving (mode+mean) comparator* with the shrinkage weight estimated from *cross-panel residual agreement* (λ* = X/M, from the exact identity A1 = M − 2X). Closest in spirit: label smoothing (shrinks toward uniform, tuned), empirical-Bayes multinomial smoothing (Dirichlet prior, not statistic-preserving). Novelty plausible but **needs a Codex + targeted search pass before claiming**.

## E. Implications for the ICML plan
1. The workshop paper by Gheibi & Ghazizadeh at ICML 2026 means the ICML community already finds "soft labels with few annotators are noisy" interesting — and that a main-track paper must go beyond it: decomposition (what part), mechanism (why: reliability), and a usable fix.
2. Our strongest differentiators: exact statistic-preserving decomposition with dose certificates; ordinal *and* nominal; end-to-end LLM judges; learner-free finite-rater identity linking annotation-side signal to learner contrasts.
3. Weakest points a reviewer will hit: null-centred headline; one base model family; POPQUORN rater-pool caveat; failed 1/a prediction; no positive method.
