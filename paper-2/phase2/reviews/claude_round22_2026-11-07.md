# Round-22 adversarial pre-review (Claude subagent, 2026-11-07)

Codex is out of quota until 2026-11-11 21:45, so an independent Claude subagent reviewed the draft after ROUND22. It had read-only access and checked the numbers against the result JSONs. This is a faithful condensation; the author's verification notes are in [brackets].

**Verdict: weak reject.** The round-21 statistical repairs are real. But ROUND22 removed the flagship ordinal example, and §1 (ii), §2.2, §4, the guidance and contribution (4) still lean on it.

## Round-21 issues
**Resolved:** N2, N7, N8, N9, N10, N12, N13, N15, N17, N18; also the LOW items "35–70 %" and "0.00060".

**Partly resolved:**
- N1: Table 2 still shows percentile G/X, and the plant detections use the percentile ci95.
- N3: the SummEval verdict is still stated on the X scale, and there is no NLI plant.
- N5: the 0.00048 correction comes from an M2 simulation that cannot produce the duplicates.
- N19: should read "low", not "not".
- LOW: the abstract is 359 words.

**Resolved, then undone by R22:** N4. The a = 4 contrast's only ordinal partner is full-panel SummEval.

**Not resolved:**
- N6: the guidance threshold ">900 items, every comparison but one". SummEval 480×2 beats 960×1 in Table 5, and POPQUORN has 819 items. [Verified.]
- N14: §5 opens with the shared-assignment block; Table 6 is stale.
- LOW: the header names only rounds 19–20.

## Where ROUND22 has not been carried through
- (a) CRITICAL, l. 18/21. Relevance stays in the ordinal list despite R22-1's frozen removal. The no-dup ratios are not shown. "ChaosNLI at a = 4 against ≤ 2.5 % on SummEval" has no valid ordinal partner. [Verified.]
- (b) HIGH, l. 23/49. "So the SummEval null is informative", "bracketing 0.00038" and the corrected 0.00048 all still assert informativeness. [Verified.]
- (c) HIGH, l. 63. "SummEval retains a small residual … is what the decoder cannot read" contradicts the caveat. [Verified.]
- (d) HIGH, l. 75 guidance. It uses the SummEval dilution contrasts as budget evidence. [Verified.]
- (e) HIGH, l. 25 contribution (4). "Items-first significant in one of three": that one is a SummEval dilution block. [Verified.]
- (f) MEDIUM, l. 61. "Half of the small panels" counts full-panel SummEval; it is 2 of 8 with the no-dup rows. [Verified: EmoBank, HS2.]
- (g) MEDIUM, l. 65. SummEval's λ̂ ≈ 0.4 is driven by the duplicates.
- (h) MEDIUM. The (iii) LoRA audit null cannot discriminate: neither LoRA panel has a detectable own-shape.
- (i) HIGH, l. 83 §7. "SummEval's small unexplained residual" is stale; the duplication, r ≈ 0.04 and the unverified provenance are missing. §2.1 also lacks the crowd–expert note.
- (j) Table 1/2. There is no duplication note in the captions.

## Number spot-check
About 30 numbers match. The mismatches:
- l. 73 "+0.020 on every fold": the per-fold values are +0.023 / +0.025 / +0.014.
- l. 21 "at least 32 % on NLI": this holds only at a = 20. At a = 4 the MNLI net lower bound is 0.268.
- Abstract "prospective LoRA blocks on POPQUORN": there is only one.

## New issues
- **CRITICAL.** The ordinal side of finding (ii) has collapsed. SummEval has no own-shape; Dorn is location-sized with an uninformative plant; DICES-350 a = 40 is detectable only conditional on the rater pool, and it has no plant. The honest headline is "no robustly reproducible ordinal shape beyond location, so nothing to decode".
- **HIGH.** Batches contradict each other: l. 73/83 say "within one batch" and "cross-batch not used", but the R20-7 arms are compared with R20-5c (another batch). [Verified: r207_compare.py uses lora_budget_r20_rerun.]
- **HIGH.** The guidance threshold is false (see N6).
- **MEDIUM.** The plants use the percentile bootstrap. Table 6 is stale, and the LaTeX bodies date from Oct 27.
- **LOW.** The l. 10 motivating example is SummEval coherence. Abstract: "on any panel where it is detectable".

## Three most valuable changes
1. Reframe (ii) and the abstract around "no robustly reproducible ordinal shape beyond location". Respect R22-1 and drop or relabel the a = 4 contrast.
2. Purge SummEval from the budget guidance and contribution (4). Add the duplication limitation to §2.1 and §7. Fix the cross-batch contradiction.
3. Rebuild Tables 2 and 6, and add a duplication caption to Table 1. Run a DICES-350 plant at a = 40, or state that the 1 % has no power calibration.
