Most main-text corrections are fixed. This checks the supplied extraction; visual PDF defects remain unverified.

| Round-9 item | Status | Revised evidence |
|---|---|---|
| Readability budgets | **FIXED** | “Buse–Weimer, \(k=20\) … Dorn, \(k=10\)” (p.6). |
| Aspect-conflict denominator and adaptation budget | **FIXED** | “all training ratings … +0.10”; “+0.03 at \(k=20\)”; “4.0 % of held-out non-tie comparisons” (p.5). |
| Five versus 25 splits | **FIXED** | “5 paired splits” (p.3); “the other crossings are not used” (p.17). Native PRISM likewise specifies “5 paired user and conversation folds” (p.6). |
| Configuration behind the +1.9 simulation benchmark | **FIXED** | “the \(c=1\) covariance-prior learner: +1.9 points implied … +0.13 realised” (p.7). |
| Percentage of likelihood gap closed | **FIXED** | “close about 55 %” (p.4), consistent with the printed reference scores. |
| Categorical ranking claims | **FIXED** | “mainly reshape predicted intensity and ties; changes in the preferred side are small” (Figure 1, p.3); “consistent with offsets acting mainly on intensity and ties” (p.4). |
| Unsupported VPL-plus-offset “tie” | **FIXED** | “non-inferiority not established” (p.5); “recovers most of the point-estimate gain” (p.8). |
| Compressed/full-feature distinctions | **PARTLY** | Main text now specifies “with PCA-256 features” (p.5) and “compressed features weaken PAL-B” (p.8). But p.14 still generalises: “make the published methods weaker detectors than they need to be,” despite reporting full-feature VPL collapse. |
| Universal power statement | **FIXED** | “No evaluated method met the pre-specified detection criterion” (p.5). |
| Appendix mechanism/failure claims | **PARTLY** | The aggregate comparison now “does not demonstrate content adaptation” (p.14). However, “the limitation lies in finding the dimension rather than in the number of ratings” (p.15) remains too exclusive; “points to where the failure lies” (p.19) retains that diagnosis despite its scope qualifier. |
| Scope of decomposition | **FIXED** | “Within this decomposition” (p.2). |
| Reversed LoRe decision rule | **FIXED** | “also meets the ranking-null criterion” (p.7). |
| S13-3 interpretation | **FIXED; remains correct** | “accuracy-positive under user clustering and likelihood-inconclusive”; the rule “requires both lower bounds above 0” (p.7). Table 5 agrees (p.8). |
| TRV versus isotropic conclusion | **FIXED; remains restrained** | “the estimated covariance shows no advantage over isotropic shrinkage” (p.7). |
| Swapped figure references | **FIXED** | “Figure 1 illustrates the effect”; “Figure 2 shows the gain … as a function of \(k\)” (p.3). |
| Uncaptioned main-text tables | **FIXED** | Tables 1–5 now have identifying captions (pp.4–8), including “Table 2. Replications at \(k=20\)” (p.5). |
| Clipped final table | **PARTLY** | Extraction now contains the complete “rank-2, same attributes” header and “+0.17 [−0.17, +0.51]” cell (Table 6, p.20). The page remains sparse; the rendered right edge is unverified. |
| Missing bibliographic attribution | **PARTLY** | “Buse & Weimer, 2010” and “Dorn, 2012” appear on p.5, with entries on p.9. WIMHF now cites “Movva et al., 2025” (p.8; entry p.10), but remains unexpanded in the main text. |
| Undefined TRV | **NOT FIXED** | “TRV, covariance-calibrated” (Table 5, p.8) supplies a description, but no explicit acronym expansion. |
| Math/axis inspection | **PARTLY; visually unverified** | Extraction still shows “RˆK” and “A B … B A” (p.3), duplicate “0.1” ticks (p.4), and “ρ < 12” (p.17). These cannot be certified as PDF defects from extraction alone. |
| Missing Stage-13 methods | **FIXED** | “Stage 13 methods (PROTOCOL STAGE13.md)” describes S13-1, S13-2 and S13-3 (p.19). |
| LoRA +0.092 versus +0.100 | **FIXED; remains explained** | “adaptation draw 0 only” versus “averaged over five draws” (p.5). Rounded-entry subtraction likewise warrants no new flag. |

Additional issues visible in this version:

- **PRISM “tie” contradicts the formal result.** Appendix B says H3r “is a tie on PRISM under the tuned prior” (p.12), whereas Table 2 explicitly says “formally not non-inferior: bound −0.006 < −0.005” (p.5). Align the appendix wording.
- **Table 5 mixes absolute accuracy and accuracy gains under one unit heading.** “Accuracy, points” contains “62.2 %” for assignment and “+0.70” for benefit (p.8). Label these as absolute accuracy (%) versus gain (percentage points).
- **Minor count mismatch:** “Three caveats” (p.13) introduces four limitations, the last continuing as “annotators may have aligned their aspect labels with their overall label” (p.14).

No stale table-number references or broken author–year citations are apparent.

Apart from the 2027 template swap, pages 1–8 are substantively ready and need only a small editorial pass for acronym expansion and table units. The single most useful change would be to clarify Table 5’s accuracy heading: distinguishing absolute assignment accuracy from improvement over a comparator would make the paper’s central distinction between predictability and benefit easier to read.