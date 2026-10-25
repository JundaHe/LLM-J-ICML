# Rater quality and the reliability of disagreement shape — protocol, frozen before any result
Committed 2026-10-26 after the user's question: when the shape of a few-rater histogram is unreliable (ρ = X/M small), how much of that is inattentive / random annotation ("瞎标") rather than genuine subjectivity, and can an LLM judge help identify such annotators without biasing the data toward the judge's own view? CPU only; uses existing ratings and the existing zero-shot Qwen2.5-7B score distributions (`Q0` in features/<panel>/*.npz); no model is trained.

## Q1 — does removing flagged annotators raise shape reliability? (DICES-350; learner-free)
DICES-350 ships 123 raters, of whom 19 failed the authors' quality checks (data_panels.DICES_REMOVED); every analysis so far used the 104 retained raters. Compute the T9(a)/(b) quantities (A1, A1x, M, X, ρ at a = m − 1 and on the dense curve a ∈ {2, 3, 5, 8, 10, 15, 20, 30, 40}) on (i) the 104-rater panel (existing results) and (ii) the full 123-rater panel (`dices_raw`), and (iii) a control panel of 104 raters drawn at random from the 123 (R = 5 draws) so that the comparison is not confounded by panel size. Estimand: Δρ(a) = ρ_104(a) − ρ_123(a) with the item-cluster bootstrap of finite_rater.py; positive ⇔ the flagged raters lowered the reproducibility of the shape.
Secondary, same construction where persistent identities and metadata exist: Dorn (experience.csv: ρ within the top vs bottom experience tercile of raters, equal rater counts), Buse–Weimer (no flags; per-rater self-consistency only).

## Q2 — can inattentive raters be identified, and does an LLM judge help? (DICES-350; the 19 flagged raters are the labelled positive set)
Per rater r, three scores computed from the items r rated:
- **H (human-only)**: leave-one-rater-out agreement — mean over r's items of 1 − |y_r − median(others)| / (K − 1) (ordinal) — the classical signal;
- **L (judge-only)**: mean over r's items of 1 − |y_r − argmax Q0| / (K − 1), and the mean log-probability Q0[y_r] (two variants);
- **H_high / L_high**: the same restricted to **high-consensus items** (items whose other-rater histogram has modal share ≥ 0.8 — the stratum where paper 1's CSJE finds a held-out human and the judge agree), to protect legitimate minority raters: disagreement on contested items is not counted against anyone.
Evaluation: AUROC of each score for the flagged set (19 vs 104), with a rater-level bootstrap (B = 2,000) for intervals; comparisons H vs L vs H_high vs L_high vs the rank-average of H_high and L_high. The question "does the judge add information" is answered by AUROC(rank-avg) − AUROC(H_high) and by the partial AUROC at ≤ 10 % false-positive rate.
Positive control: inject S = 10 synthetic raters per replicate (uniform random labels over the K levels on a random subset of items matching the real raters' item counts) and report the same AUROCs for synthetic-vs-retained; a usable detector must separate synthetic raters almost perfectly.
Bias check (mandatory): among the retained 104 raters, the correlation between L and the rater's mean deviation from the panel median signed toward the judge's modal answer — a strong correlation would mean "judge agreement" measures "agreeing with the judge", not attentiveness; report it and, if |r| > 0.5, do not recommend L.
Transfer (descriptive only): apply the H_high / L_high scores to Dorn raters (sparse: 5–14 ratings each) and report their distribution and the ρ of the panel after removing the lowest decile, as an exploratory indication; no claim of validity without flagged labels.

## Forbidden statements
"Annotators who disagree with the LLM are low quality"; any removal of raters from the main analyses of the paper based on L alone; any claim that spamming explains the low ρ of a panel without the Q1 contrast on that panel.

## Amendments
(none)
