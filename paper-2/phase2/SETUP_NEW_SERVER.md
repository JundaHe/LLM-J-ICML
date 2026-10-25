# Moving paper-2 to another server

Everything paper 2 needs is in this repository (`JundaHe/LLM-J-ICML`, branch `main`) except the items listed under "Not included".

## 1. Clone
```bash
git clone --recurse-submodules git@github.com:JundaHe/LLM-J-ICML.git
cd LLM-J-ICML
# (if cloned without --recurse-submodules) the three datasets are git submodules pinned to upstream commits:
git submodule update --init
# two feature files > 100 MB are stored as split parts
bash paper-2/phase2/restore_features.sh
```

## 2. Paths
All scripts derive the repository root from their own location (`paper-2/phase2/paths.py`). Override with `export LLMJ_ROOT=/path/to/LLM-J-ICML` only if you move `paper-2/` out of the repository.

## 3. Python environments
- GPU / training / analysis: `pip install -r paper-2/phase2/requirements-gpu.txt` (Python 3.12, CUDA 12.x). Model: `Qwen/Qwen2.5-7B-Instruct` from the Hugging Face Hub.
- Figures, LaTeX tables and build: `pip install -r paper-2/phase2/requirements-cpu.txt`, plus `pandoc`, `pdflatex`, `bibtex`.

## 4. What is where (paper-2/phase2)
| what | path |
|---|---|
| manuscript (markdown source → LaTeX → PDF) | `PAPER_DRAFT.md`, `build_latex.py` → `latex/main.pdf` |
| all result tables | `RESULTS_TABLES.md` (T2b heads, T3b SummEval LoRA, T3c POPQUORN LoRA, T5 ChaosNLI, T9 finite-rater) |
| hourly log / decisions | `PROGRESS.md` |
| reviews (Codex rounds), novelty checks | `reviews/`, `novelty/` |
| raw datasets | `data/` (3 submodules + plain files) |
| frozen Qwen2.5-7B features for the heads | `features/<panel>/Qwen2.5-7B-Instruct.npz` |
| heads results | `results/probe_mean2/`, `results/probe_mean/`, `results/probe_nominal/` (`runs.jsonl`) |
| LoRA predictions + certificates | `results/lora/<panel>/<seed>/f<fold>/<arm>/` (`P_test.npy`, `P_calib.npy`, `items_*.csv`, `meta.json`, `train.log`) |
| finite-rater analysis | `FINITE_RATER_PROTOCOL.md`, `finite_rater*.py`, `results/finite_rater/` |
| artefact hashes | `results/MANIFEST.json` (`python manifest.py`) |

## 5. Common commands (from paper-2/phase2)
```bash
python check_consistency.py            # manuscript numbers vs artefacts (GPU env)
python make_latex_tables.py && python make_figures.py && python build_latex.py   # CPU env
python finite_rater.py --panel chaosnli_mnli --ref                     # learner-free analysis (CPU)
python finite_rater_summary.py
PY=$(which python) bash lora_chain_popquorn.sh <gpu> 2000 2001 2002    # retrain the POPQUORN LoRA block
python analysis_block_popquorn.py; python sensitivity_popquorn_users.py
```

## Not included
- LoRA adapter weights (`results/lora/**/lora/`, ≈150 MB each): retrain with the chain scripts if needed; all predictions used by the paper are included.
- `logs/` and `*.log` except LoRA `train.log`.
- Features of the removed commit panels; the heavy idea-stage pilot artefacts under `paper-2/idea-stage/pilot/results*` (commit panels, removed from the paper).
