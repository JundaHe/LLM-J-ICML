# Data provenance — code readability human annotations

These are the **original human-annotated code-readability datasets** used by the paper
*Human-Aligned Code Readability Assessment with Large Language Models* (the CoReEval
benchmark, [arXiv:2510.16579](https://arxiv.org/abs/2510.16579)). Per request, the data
is taken from the **cited source papers**, not from CoReEval's repackaging.

All three were obtained from Simone Scalabrino's readability replication site, which
hosts the canonical copies (it re-distributes the Buse–Weimer and Dorn sets together with
its own): <https://dibt-research.unimol.it/report/readability/> (base for downloads:
`.../files/`). Raw downloads (zips + ARFF feature tables) are archived under `raw/`.

## Datasets

### 1. `buse_weimer/` — Buse & Weimer
- **100 short Java snippets**, each rated by **~121 annotators** (CS students), 1–5 Likert.
- `snippets/*.jsnp` — the code snippets; `oracle.csv` — one row per annotator
  (`annotatorID, group, score_snippet_1 … score_snippet_100`).
- **Cite:** R. P. L. Buse and W. R. Weimer. *Learning a Metric for Code Readability.*
  IEEE Transactions on Software Engineering, 36(4):546–558, 2010. (orig. FSE 2008.)

### 2. `dorn/` — Dorn
- **360 real-world snippets**: Java (121), Python (119), CUDA (120), rated by **5,000+
  developers** (sparse — each annotator rated a subset), 1–5 Likert.
- `snippets/{java,python,cuda}/` — the snippets;
  `scores/{java,python,cuda}.csv` — sparse annotator × snippet score matrices;
  `experience.csv` — annotator experience metadata.
- **Cite:** J. Dorn. *A General Software Readability Model.* MS thesis, University of
  Virginia, 2012.

### 3. `scalabrino/` — Scalabrino et al.
- **200 method-level Java snippets** (jUnit, Hibernate, ArgoUML, jFreeChart), each rated by
  **9 CS students**, 1–5 Likert.
- `Snippets/*.jsnp` — the snippets; `scores.csv` — evaluator × snippet matrix
  (rows `Evaluator1…Evaluator9`, columns `Snippet1…Snippet200`).
- **Cite:** S. Scalabrino, M. Linares-Vásquez, R. Oliveto, and D. Poshyvanyk.
  *A Comprehensive Model for Code Readability.* Journal of Software: Evolution and Process,
  30(6):e1958, 2018. (orig. ICPC 2016: *Improving Code Readability Models with Textual
  Features*.)

## `raw/` (archived downloads)
`Dataset.zip` (Scalabrino), `DatasetBW.zip` (Buse–Weimer), `DatasetDorn.zip` (Dorn), and the
matching `DATASET_*_EXTENSION.arff` feature tables (Weka ARFF: computed readability metrics
plus the aggregated readable/unreadable oracle label per snippet).

## Score scale
All three use a **5-point Likert scale** (1 = very unreadable … 5 = very readable). Because
per-annotator scores are preserved, these datasets support **human-disagreement /
uncertainty analysis** (multiple raters per snippet), unlike single-vote preference data.

> In the LLM-J-ICML (paper 2) repository only `buse_weimer/`, `scalabrino/` and `coreeval_snippets/Scalabrino_java_Code.csv` are kept — the files paper 2 loads.
