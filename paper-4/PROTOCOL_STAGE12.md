# Paper 4 — Stage 12: frozen evaluation of transfer-calibrated adaptation on untouched Community Alignment turns (frozen before any second-turn data are embedded or analysed)
Committed 2026-11-03 23:55, after the fourth review with gpt-6.1-sol (`reviews/codex_round04_gpt-6.1-sol.md`: "independently evaluate the complete Amendment-4 procedure… freeze the existing procedure rather than adding another adaptation family"). Stage 11 Am. 1–4 developed the procedure (TRV) on the CA first turns after inspecting test results; its +0.49 [+0.20, +0.77] choice points and +0.0088 nats are exploratory. This stage evaluates it, unchanged, on CA **second turns**, which no analysis of this project has read (no features, no labels, no counts beyond the number of non-missing preferences, 83,238, read to establish availability). The users are the same people as in Stages 8–11 (no CA user is untouched), so this is a frozen evaluation on **new prompts and conversation turns of previously studied users**, and is described as such. Any change after the first result is logged under "Amendments" and does not alter the readings below.

## Panel (fixed now)
Second turn of each CA conversation with four second-turn responses and a preferred one; the chosen response paired with each of the three others (A/B side randomised, seed 0); label = native choice; choice event = the conversation's second turn; prompt group = the second-turn prompt text; the user folds of Stage 8 (country-stratified, seed 0) and prompt-group folds (seed 0) and validation flag (seed 1), all re-derived on this panel by the same code. **Features:** Qwen2.5-7B-Instruct last-layer final-token state of the chat-formatted (second-turn prompt, response) and of the second-turn prompt alone, each text truncated at 4,000 characters; the first turn is not included in the context (stated limitation: second-turn responses were generated with the conversation context). Attributes: the 24 `attr_feats.py` differences with the second-turn prompt as the prompt text.

## Procedure (TRV, exactly Stage 11 Am. 4)
Per fold: population model = ridge logistic regression on the PCA-256 response difference (λ by validation in {1, 10, 100, 1000}) plus per-language attribute weights μ_ℓ; Ĉ = the symmetrised, PSD-projected uncentred cross-moment of one-step deviations over two halves with disjoint prompt groups (seed 5; users with ≥ 10 events; ridge 10⁻³), for the attribute set; pseudo-new-user selection (20 % of training users, seeds 3 + f, 40 + f; base and μ refitted without them; 20 support events, rest scored) of the attribute set {length; length, paragraphs, list/heading lines} and prior scale c ∈ {1, 0.5, 0.25, 0.125, 0.0625, 0} by mean log-likelihood; θ̂_u − μ = c Ĉ (I + c I_u Ĉ)⁻¹ s_u from the user's k = 20 support events (training prompt groups), Ĉ from all training users. Test: held-out prompt groups of test-fold users with ≥ 20 support events; 5 support draws (seeds 10,000 f + d).
**Comparators**, each with its adaptation strength (including none) selected on the same pseudo-new users: (a) μ (no adaptation); (b) **validated isotropic attribute prior** — the same rule with Ĉ replaced by τ² I over the same selected-set candidates, τ² ∈ {0.01, 0.03, 0.1, 0.3, 1, 0}; (c) the tuned rank-2 model of Stage 9 Am. 6 (`sap_ca.py` ATTR-LR-bin, its grid). Also reported: the half-specific means and centred cross-covariance of the one-step deviations, overall and within language.

## Outcomes and decision rules (fixed now)
Primary: own − μ choice accuracy (points) and log-likelihood (nats per pair), user bootstrap (seed 17, 2,000 resamples, users weighted by test pairs); prompt-group/user two-way bootstrap as a secondary interval.
- **Reproducible predictive benefit** if both own − μ accuracy and log-likelihood have lower 95 % bounds above 0.
- **Practically meaningful choice gain** if the accuracy lower bound is above +1 point.
- **Sub-threshold** for this procedure and population if the accuracy upper bound is below +1 point.
- **Advantage over ordinary validated shrinkage** if TRV − (b) accuracy has a lower bound above 0; over the rank-2 model likewise against (c).
- Otherwise inconclusive. Outcomes failing these conditions are reported without further test-driven revision.
Secondary: the same per language; Stage 8's LoRe and LoRe-reg are not rerun.

## Forbidden statements
"Untouched users"; "replication on new data" without the qualification above; any claim about turns three and four; "calibration gain" for a log-likelihood gain (it is a predictive log-likelihood gain).

## Amendments

## Result (2026-11-04 09:35, job 12569; read by the frozen rules, no revision)
1,702 test users, CA second turns, k = 20 events. Selected on pseudo-new users: TRV {length, c = 1; prim3, 0.25; length, 0.25; length, 1; prim3, 0.125}; isotropic {length, 0.3; prim3, 0.1; length, 0.03; prim3, 0.03; prim3, 0.03}; rank-2 adaptation c = 0.1 in folds 0–1 and **no adaptation** in folds 2–4.
- **TRV own − μ: +0.38 [+0.13, +0.64] choice points; +0.0046 [+0.0031, +0.0063] nats per pair** (two-way prompt-group × user interval: accuracy [−0.04, +0.83], LL [+0.0018, +0.0074]).
- Isotropic own − μ: +0.31 [+0.05, +0.58] points, +0.0038 [+0.0021, +0.0057] nats. Rank-2: −0.05 [−0.34, +0.24], −0.0013 nats.
- TRV − isotropic: +0.07 [−0.07, +0.22] points, +0.0008 [−0.0000, +0.0016] nats. TRV − rank-2: +0.43 [+0.15, +0.74] points.
- Per language (accuracy): en +0.21, fr +0.49, hi +0.44, it +0.35, pt +0.61; every interval covers 0.
- One-step diagnostics: length cross-moment 0.12–0.19 in every fold (centring and within-language centring change it by < 1 %); paragraphs 0.09–0.68; list/heading negative in two folds (−0.53, −0.34 centred).
**Decisions:** reproducible predictive benefit — **met**; practically meaningful choice gain — **not met**; **sub-threshold** for this procedure and population — **met** (upper bound +0.64 < +1); advantage over ordinary validated shrinkage — **not met**; advantage over the rank-2 model — met (in three of five folds the tuned rank-2 model selects no adaptation, so this is largely TRV vs μ). The primary user-bootstrap interval excludes 0; the secondary two-way interval does not.
