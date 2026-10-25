# Related work — citation list TO VERIFY before use (each entry: what we need it to support; verify venue/year/claim; do not cite from memory)

## Distributional / soft-label training of judges and classifiers
- Chen et al. 2025 — soft-label (KL to empirical histogram + adversarial perturbation) fine-tuning of LLM judges; the objective we replicate as `chen` and its no-adversary control `chen0`. CLAIM: prior work reports lower proper-scoring loss from distributional objectives on several benchmarks. VERIFY exact title, venue, reported benchmarks and metrics; confirm there is no released code (our LoRA note says "no released code to parity-test").
- Label smoothing (Szegedy et al. 2016; Müller, Kornblith & Hinton 2019 "When does label smoothing help?") — the `smooth` reference arm. CLAIM: uniform smoothing is a non-item-linked regulariser.
- SORD — Díaz & Marathe 2019 "Soft labels for ordinal regression" (CVPR). CLAIM: Gaussian/ordinal soft targets centred on a label; our `sordz`/`sordm` arms.
- Learning from soft labels / crowd distributions: Peterson et al. 2019 (CIFAR-10H, "Human uncertainty makes classification more robust", ICCV); Uma et al. 2021 survey "Learning from disagreement: a survey" (JAIR). CLAIM: training on label distributions improves calibration/robustness; motivates the "learns how people disagree" reading we audit.
- Fornaciari et al. 2021 "Beyond black & white: leveraging annotator disagreement via soft-label multi-task learning" (NAACL). CLAIM: soft-label auxiliary tasks help.

## Annotator disagreement as signal; perspectivism
- Nie, Zhou & Bansal 2020 — ChaosNLI (EMNLP). CLAIM: 100 annotations per item on SNLI/MNLI/αNLI; the dataset of our nominal panel; their finding that model distributions diverge from human distributions.
- Pavlick & Kwiatkowski 2019 "Inherent disagreements in human textual inferences" (TACL). CLAIM: NLI disagreement is systematic, not noise.
- Plank 2022 "The 'problem' of human label variation" (EMNLP); Basile et al. 2021 perspectivist manifesto (Bender & Friedman?) — VERIFY authors: "We need to consider disagreement in evaluation" (Basile, Fell, Fornaciari, Hovy, Paun, Plank, Poesio, Uma 2021). CLAIM: calls to model variation rather than aggregate it.
- Aroyo & Welty 2015 "Truth is a lie: crowd truth and the seven myths of human annotation" (AI Magazine). CLAIM: disagreement is informative.
- DICES — Aroyo et al. 2023 "DICES dataset: diversity in conversational AI evaluation for safety" (NeurIPS D&B). CLAIM: our DICES panel; per-rater demographics; Q_overall.
- SummEval — Fabbri et al. 2021 (TACL). CLAIM: expert and crowd annotations per summary; our coherence/relevance panels (3 experts; 5 turkers → 8 raters).
- HelpSteer2 — Wang et al. 2024 (NVIDIA). CLAIM: multiple annotators per response, helpfulness 0–4; our hs2_help5 panel.
- Buse & Weimer 2010 "Learning a metric for code readability" (TSE); Scalabrino et al. 2016/2018 (ICPC/JSEP) comprehensive readability model. CLAIM: dense multi-rater code readability panels (121 and 9 raters).
- Commit-message quality benchmark (CM-benchmark; Zeng et al.? VERIFY — the "What/Why" criteria and the 6-rater panel; source of our commit panels and of the paper-1 pipeline).

## Rater-conditioned / per-annotator models
- Davani, Díaz & Prabhakaran 2022 "Dealing with disagreements: looking beyond the majority vote in subjective annotations" (TACL) — multi-annotator (per-annotator heads) models. CLAIM: identity conditioning; our Stage A found identity buys severity only (T6).
- Gordon et al. 2022 "Jury learning" (CHI). CLAIM: per-annotator prediction and aggregation.
- Fleisig, Abebe & Klein 2023 "When the majority is wrong: modeling annotator disagreement for subjective tasks" (EMNLP). CLAIM: predicting individual annotators.
- Mixture-of-raters / rater embeddings (e.g., Resnick/Kwiatkowski? VERIFY) — only if a concrete paper is found.

## Randomisation / ablation controls for supervision signals
- Zhang et al. 2017 "Understanding deep learning requires rethinking generalization" (ICLR) — label randomisation. CLAIM: permuting labels as a control for what supervision provides.
- Permutation-based feature/signal importance (Breiman 2001 random forests permutation importance; Fisher, Rudin & Dominici 2019 "model class reliance"). CLAIM: permuting a signal while preserving marginals measures its predictive use; our donor replacement preserves selected item-level statistics instead of marginals.
- Conditional permutation / knockoffs (Candès et al. 2018 "Panning for gold") — CLAIM: conditional randomisation tests preserve dependence on retained covariates; analogy to our within-cell replacement. Use only if the analogy is stated carefully.
- Negative controls / placebo tests in causal inference (Lipsitch, Tchetgen Tchetgen & Cohen 2010). CLAIM: positive-control construction (our injected-shape control).

## Calibration and evaluation of judges / proper scoring
- Gneiting & Raftery 2007 "Strictly proper scoring rules" (JASA); Epstein 1969 RPS. CLAIM: RPS as the ordinal proper score.
- Guo et al. 2017 "On calibration of modern neural networks" (ICML) — temperature scaling. CLAIM: our calibration map (temperature + climatology shrinkage).
- LLM-as-judge calibration/bias surveys (Zheng et al. 2023 "Judging LLM-as-a-judge" NeurIPS D&B; Gu et al. 2024 survey) — CLAIM: context for learned judges.
- Equivalence testing / TOST (Schuirmann 1987; Lakens 2017 "Equivalence tests: a practical primer"). CLAIM: the 90 % CI criterion we use as an exploratory sensitivity; post hoc margins caveat.

## Our own prior work
- Paper 1 (ICSE 2027 submission; LLM-J) — the rater-level evaluation protocol and the commit/readability panels. CLAIM: provenance of panels and the held-out-rater evaluation.

## Additions and corrections from the final review (2026-10-12)
- ADD Geng 2016 "Label Distribution Learning" (IEEE TKDE) — foundational LDL; CLAIM: training on label distributions as a learning paradigm.
- ADD Zhou, Nie & Bansal 2022 "Distributed NLI" (Findings of ACL) — direct distributional NLI prediction; CLAIM: closest prior on ChaosNLI distribution prediction.
- ADD Baan et al. 2024 (EACL short) — model confidence vs human label variation; CLAIM: the distinction we rely on when scoring against held-out annotations.
- ADD Elangovan et al. 2025 (ICLR) — LLM-judge evaluation against human uncertainty; CLAIM: judge evaluation under rater disagreement.
- ADD LeWiDi, SemEval 2023 (Leonardelli et al.) — learning-with-disagreement shared task; CLAIM: community benchmark for soft-label learning.
- ADD Prabhakaran et al. 2021 (LAW) "On releasing annotator-level labels and information in datasets"; CLAIM: annotator-level label retention/release.
- ADD Wang, Zhang & Choi 2025 (Findings of EMNLP) — distributional judge inference from output-token distributions; CLAIM: distinguish token-distribution judging from supervision with empirical human histograms.
- CORRECT Chen et al. 2025: cite with the exact objective (hybrid 0.8·KL + 0.2·CE(mode) plus target-distribution adversarial perturbation); DROP the "no released code" claim (the paper states code/data in supplemental material) — our note must say we re-implemented with LoRA from the paper's description and did not parity-test.
- CORRECT "Basile et al. (Bender & Friedman?)" → Basile, Fell, Fornaciari, Hovy, Paun, Plank, Poesio, Uma 2021, "We need to consider disagreement in evaluation" (BPPF workshop, ACL Anthology 2021.bppf-1.3).
- CORRECT Peterson et al. 2019 → supports robustness findings only; Uma et al. 2021 → emphasises dataset/evaluation dependence; do not jointly cite for "soft labels improve calibration and robustness".
- CORRECT Lipsitch et al. 2010 → epidemiological negative controls; does not justify our injected-shape experiment; call ours a "semi-synthetic sanity check" and cite nothing for it unless a direct source is found.
- CORRECT Breiman 2001 / Fisher et al. 2019 (evaluation-time permutation importance) and Zhang et al. 2017 (label randomisation → memorisation) → analogies only; say so.
- CORRECT Guo et al. 2017 → temperature scaling only; the temperature + climatology mixture is paper-specific.
- DELETE the "Resnick/Kwiatkowski?" placeholder.
- CORRECT commit dataset source → Zeng et al., "Evaluating Generated Commit Messages with Large Language Models", ICSE 2026 (arXiv 2507.10906).
- RESOLVE Scalabrino placeholder to one exact dataset source (the CoReEval subset we use; cite both the original Scalabrino et al. study and the CoReEval compilation if that is the data path).
- Citations must be inserted into the draft before submission; the absence of citations is itself a submission veto.
