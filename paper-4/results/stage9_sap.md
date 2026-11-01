# Stage 9 — screened attribute personalisation (SAP)

| panel | own − μ, dir, k = 20 | own − other, dir, k = 20 | own − μ, dir, k = 50 | own − μ, LL ×100, k = 20 | selected in ≥ 4/5 folds (null-calibrated) |
|---|---|---|---|---|---|
| t0 | -0.19 [-0.50, +0.14] | +0.06 [-0.26, +0.39] | -0.50 [-0.92, -0.09] | -0.10 [-0.18, -0.01] | (null reference) |
| t5 | +1.36 [+0.73, +1.98] | +2.54 [+1.88, +3.24] | +1.41 [+0.59, +2.26] | +1.45 [+0.99, +1.97] | length, prompt overlap, second person, type-token ratio |
| t10 | +3.89 [+2.74, +5.04] | +6.19 [+5.06, +7.39] | +4.14 [+2.94, +5.54] | +3.76 [+2.74, +4.90] | code blocks, length, list/heading lines, paragraphs, prompt overlap, type-token ratio |
| sem5 | +2.69 [+1.70, +3.64] | +5.00 [+4.03, +5.99] | +3.98 [+2.70, +5.22] | +2.78 [+2.00, +3.60] | digits, hedging/refusal, list/heading lines, prompt overlap |
| sem10 | +7.53 [+5.92, +9.10] | +12.23 [+10.63, +13.82] | +9.35 [+7.60, +11.05] | +8.73 [+6.97, +10.57] | digits, evidence phrases, headings, hedging/refusal, length, list/heading lines, prompt overlap, safety/disclaimer, second person |
| real | +0.17 [-0.19, +0.55] | +0.45 [+0.03, +0.86] | +0.13 [-0.45, +0.63] | +0.22 [+0.03, +0.41] | bold/italic, code blocks, digits, first person, headings, hedging/refusal, length, paragraphs, prompt overlap, safety/disclaimer, second person, type-token ratio |

**Rules:** {"M1_no_false_detection": true, "M2_detect": {"sem5": true, "sem10": true}, "M2_select": {"sem5": true, "sem10": true}, "M3_real_content_personalisation": false}

Null thresholds (max σ² over t0 folds): length 0.0021, list/heading lines 0.0022, hedging/refusal 0.0018, code blocks 0.0023, bold/italic 0.0019, digits 0.0016, question marks 0.0018, exclamation marks 0.0018, first person 0.0013, second person 0.0015, sentence length 0.0028, word length 0.0016, paragraphs 0.0020, URLs 0.0036, examples 0.0016, safety/disclaimer 0.0016, summary markers 0.0015, emojis 0.0058, evidence phrases 0.0016, politeness 0.0016, strict refusal 0.0018, type-token ratio 0.0021, prompt overlap 0.0014, headings 0.0015
