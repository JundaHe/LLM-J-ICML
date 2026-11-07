# v3 compression self-review (subagent, read-only), 2026-11-07

Scope: v3 main text (Abstract–§7) checked sentence by sentence against PAPER_DRAFT_v2.md v2.5.

## Result

No wrong numbers: every main-text number matches v2.5 and is attached to the right panel and quantity.

Findings, all applied in the same commit:

### HIGH
- **Conclusion: "items first is the right default".** This contradicts v2.5 and v3 §6 (LoRA on POPQUORN: two ratings are the safer default; the budget result is not derived from the mechanism). Rewritten as an observation, with both learners.
- **§7: "three model families" for decoding.** Own-shape decoding on all three families covers only SummEval, MNLI and DICES-350. Restored the scope.
- **§7: "the end-to-end budget result replicates on OLMo-2".** Only the SummEval (dilution) contrasts replicate on OLMo-2; the POPQUORN block and the audit are Qwen2.5 only. Corrected.
- **Intro (ii) and Conclusion: "not in the text".** Restored "linearly decodable from the frozen features we tested".

### MED
- §6 guidance: added the scope (POPQUORN) and the exceptions (SummEval flat; HelpSteer2 on OLMo-2).
- §4/§5 rater-side claims: restored "on panels with persistent rater identities" and "established only on DICES-350, conditional on its rater pool".
- Intro (iii): restored the qualifier on the four panels.
- §4 DICES-350 sentence: restored "within the observed rater pool" and "for a planted shape of this size and construction".
- §4: nonlinear probe scoped to SummEval and POPQUORN only.
- Abstract/intro "detectable only on DICES-350" vs §4 "two panels detectable" (Dorn): now "beyond location".

### LOW
- Abstract: restored "(95 % bounds)".
- Related work: restored "for KL".
- §4 reference-strength rule: X_own is used for Dorn and DICES-350; the prespecified rule for SummEval and POPQUORN is stated on X.
- Intro: positive control and plant listed separately.
- §6: corrected which block reproduces which.
- §5: added the location-plus-dispersion models for position panels.
- Fixed Appendix references (A–B, Appendix C) and renumbered the A.1–A.3 subheads.

### Not changed
- §7 "POPQUORN budget effects of 0.006–0.009" (v2.5 has "+0.02"). Kept deliberately: v3 limits budget evidence to POPQUORN.
