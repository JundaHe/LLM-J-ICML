# Stage 15 protocol — the three analyses asked for in Codex round 11

Written 2026-11-23, before any Stage 15 run. Everything here is **post hoc**: it follows the Stage 14 results (PROTOCOL_STAGE14.md, Amendment 1) and the
review in `reviews/codex_round11_gpt-6.1-sol.md`. Nothing in this stage may replace a Stage 14 number; it adds calibration, a decomposition and wider
intervals. The configuration of the corrected latent models is frozen as adopted in Stage 14: **rung a** (`--whiten_adapt`, penalties by validation
log-likelihood, adaptation strength by k-shot validation on held-out training raters). **Rung b** (`--whiten_adapt --sel_conc 20`) stays a sensitivity analysis.

## 0. Why

Round 11 lists three gaps, in this order:

1. The corrected detectors were shown on one synthetic draw per strength. Detection limit and false-alarm behaviour need the existing seeds and injection families.
2. The paper says the latent's gains on PRISM and Dorn are scale use ("rater shift"), but the latent and the offsets model were never compared with the
   *same* offsets, and the latent's item-independent component was never separated from its content interaction.
3. The corrected real-panel contrasts have rater-bootstrap intervals only and no declared multiplicity family. Two of them are small
   (PRISM DF − DL −0.0037 [−0.0065, −0.0008] nats; DICES L concordance +0.50 [+0.09, +0.96]).

## 1. S15-1 — corrected detectors over the existing synthetic draws

**Panels** (all exist under `results/synth/`; none is regenerated; realised oracle gains from `synth_meta*.json`):

| family | injected axes | draws | strengths |
|---|---|---|---|
| null | none | t0, t0s11, t0s12, t0s13 | 0 |
| random | length + random direction | t5/t10, +s11, s12, s13 | ≈ +5, ≈ +10 |
| in-span | direction inside the feature span | x5/x10, +s11, s12, s13 | ≈ +5, ≈ +10 |
| semantic | formatting + hedging | sem5/sem10, +s11, s12, s13 | ≈ +5, ≈ +10 |

Rung-a and rung-b runs of t0, t5, t10 exist (Stage 14 A1-4) and are reused unchanged. New runs: 25 panels × 5 folds, same command as A1-4
(`--models D,DFs,DL,T0,F,L --ks 0,20,50 --concord --adapt_tune --perm_control`). Rung a is run on all four families. Rung b is run on the null, random
and semantic families (the three the review names); it is not run on the in-span family.

**Statistics** per panel, latent (DL, L) and rung, k = 20, rater bootstrap over (fold, rater), B = 2000, seed 17 (as `s14_real.py`): direction accuracy
own − other (primary), direction own − k = 0, concordance own − other, concordance own − k = 0, log-likelihood latent − scale-use comparator (DFs / F).

**Rules** (the first two are the Stage 14 A1-4 rules, unchanged):

- *Detection in a draw*: lower bound of own − other (direction) > +1 point.
- *Null sound in a draw*: the interval of own − other intersects [−0.5, +0.5] (the rule as coded in Stage 14). Also reported: whether the interval excludes 0.
- *Frequency* (Stage 7 Amendment 4 convention): a detector **detects** a family × strength if the detection rule fires in ≥ 3 of 4 draws, **fails** if in
  ≤ 1 of 4, and is **unstable** otherwise. A detector is **null-sound** if the detection rule fires in 0 of 4 null draws and every null draw is sound.
- The same counts are reported for own − k = 0 (net gain over no personalisation) as a second column; it has no rule.
- Pooled over the four draws of a family × strength: own − other with raters resampled jointly across draws (the draws share raters). Descriptive.

**Expectation, written in advance.** Null: sound for both latents and both rungs. Random +10: L rung a detects (single draw: lower bound +2.02); DL rung a
fails (single draw +0.62 [+0.17, +1.06]); both detect under rung b. Random +5: nobody detects. In-span +10: DL detected already in the original
configuration (3 of 4 draws), so both latents should detect under rung a; +5 open. Semantic: no directional expectation (the original configuration
detected neither strength). Net gain own − k = 0 is expected to be smaller than own − other and often not above 0.

**What it changes.** The paper's sentence on the detection limit ("between +5 and +10 oracle points") is kept only if the frequency rule supports it for
the family it names; otherwise it is rewritten per family. A null that is not sound is reported as a defect of the control, not explained away.

## 2. S15-2 — scale use against the content interaction, with the same offsets

### 2.1 Stage-wise models (new code, `factorised_rm.py`, kinds `DFL` and `FL`)

- `DFL` (softmax family): logits = text head + b + **B_r** + Σ_d (x W)_d z_rd. The text head and the offsets B_r are those of the fitted `DF` model, frozen;
  only the interaction map W and the latent z are fitted on top. No constant column: the features are centred over items, so the interaction has no
  item-independent part.
- `FL` (ordinal family): μ = xβ + **δ_r** + (xW)·z_r, log-scale **s_r**; β, cut-points, δ, s from the fitted `F` model, frozen.
- Selection: (λ_r, λ_W) on the Stage 2 grid by validation log-likelihood on top of the base fitted on the same training rows (rung a).
- New raters: the offsets are **the base model's adapted offsets, copied** (same k ratings, same tuned strength). Then z is adapted with the whitened prior,
  strength tuned on the Stage 14 grid by k-shot validation on held-out training raters, again on top of the base's adapted offsets.
- A stage-wise model with the latent at its prior mean differs from its base only by a text-side term (the mean interaction).

Reported per panel and family, k = 20 (Dorn k = 10), log-likelihood ×100, direction and concordance in points:

| contrast | meaning |
|---|---|
| staged − base | everything the interaction adds, offsets identical |
| staged − staged(z at prior mean) | the personal part of the interaction |
| staged − staged(another rater's z, own offsets) | own − other on the interaction alone |

### 2.2 Decomposition of the adopted latent models (no refit)

For the rung-a `DL` and `L` fits, after whitening, the rater term is (constant column)·u_r + (x W)·u_r. With the adapted u of the rater ("own") and of
another test rater ("other", the derangement of the permutation control), four extra predictions are scored:

| name | item-independent part | interaction part |
|---|---|---|
| `sh` | own | prior mean |
| `ia` | prior mean | own |
| `xi` | own | other |
| `xs` | other | own |

own − `xi` is the value of the rater's own interaction with the own shift held; own − `xs` is the value of the own shift with the own interaction held.

### 2.3 Panels

Real: MultiPref, DICES, PRISM, Dorn (5 folds, rung a, `--ks 0,20`, Dorn `0,10`; `DF` is the base on every panel; on MultiPref `DFs` is also reported).
Positive control: the existing synthetic draws t0, t5, t10 (5 folds) with the same model list. The stage-wise models are new, so **a null on a real panel
is read only if the control passes**: at t10, own − other on the interaction (direction, own offsets held) has lower bound > +1 point for the family, and at
t0 its interval intersects [−0.5, +0.5].

### 2.4 Reading rule (fixed now; rater-bootstrap intervals, then the two-way intervals of S15-3)

For each panel × family:

- **interaction adds**: staged − base log-likelihood has lower bound > 0 **and** own − other on the interaction has lower bound > 0 in log-likelihood or concordance.
- **no interaction beyond the offsets**: staged − base log-likelihood has upper bound ≤ +0.5 (×100 nats) **and** concordance own − other on the interaction has upper bound < +1 point.
- **inconclusive** otherwise.

For the adopted latents: the personal gain is **shift** if own − `xs` has lower bound > 0 (log-likelihood) while own − `xi` has upper bound ≤ +0.5 (×100 nats)
and concordance upper bound < +1 point; **interaction** if own − `xi` has lower bound > 0; both can hold.

**Expectation.** PRISM: the softmax latent's small likelihood lead over DF is a pooled low-rank shift — own − `xs` > 0, own − `xi` ≈ 0, DFL − DF ≈ 0.
Dorn: the same for L / FL. MultiPref: no interaction. DICES: open (L's concordance lead +0.50 could reappear as FL own − other).

## 3. S15-3 — two-way intervals and a declared multiplicity family

The S15-2 real-panel runs carry `--dump_ratings` (per-rating log-likelihood, direction, expected score, rating). They contain the rung-a `D, DF, DFs, DL,
T0, F, L` fits; the per-rater values must reproduce the Stage 14 `_wa` runs (|difference of the pooled contrast| ≤ 1e-3 per rating, as in Stage 2
Amendment 9). If they do not, S15-3 is reported as failed, not adjusted.

**Resampling.** Raters and item clusters (the panel's `groups`: prompts / conversations / snippets) resampled independently (pigeonhole bootstrap), B = 2000,
seed 9; the five adaptation draws averaged within rating. Log-likelihood and direction: ratio estimators with weight w_r·w_g. Concordance: pairs within
rater weighted w_r·w_g(i)·w_g(j) (w_r·w_g for two items of one cluster). Rater-only intervals are printed next to them.

**Families** (k = 20, Dorn k = 10; 4 panels × 2 latents each):

- Family A — corrected Stage 14 contrasts (24): log-likelihood latent − scale-use comparator; direction own − other; concordance own − other.
- Family B — Stage 15 contrasts (24): log-likelihood staged − base; log-likelihood own − other on the interaction; concordance own − other on the interaction.

p-values two-sided from the normal approximation with the two-way bootstrap standard error (as `multiplicity.py`). Holm within each family and over the
union of 48. Every contrast is printed with its nominal interval and both adjusted decisions; nothing is dropped.

**Expectation.** PRISM DF − DL and the DICES concordance lead do not survive Holm over Family A; the two-way intervals are wider than the rater-only ones
and may include 0 for both.

## 4. Order, compute, outputs

1. This file is committed and pushed before any run.
2. Code: two new kinds and the decomposition in `factorised_rm.py` (only when asked for with `--models` / `--decomp`; default runs unchanged), checked by a
   smoke run on one synthetic fold and by the S15-3 reproduction check.
3. Runs through Slurm, one thread per process. Summaries: `s15_synth.py` → `results/stage15_synth.{json,md}`; `s15_decomp.py` → `results/stage15_decomp.{json,md}`;
   `s15_twoway.py` → `results/stage15_twoway.{json,md}`.
4. CLAIMS.md and the draft are changed only after all three summaries exist; the main text stays within 8 pages.
