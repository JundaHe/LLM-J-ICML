#!/bin/bash
#SBATCH -J embed-se
#SBATCH -p normal
#SBATCH --gres=gpu:1
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -t 04:00:00
#SBATCH -o /scratch/jundahe/LLM-J-ICML/paper-2/phase2/logs/slurm_embed_se_%j.log
# Frozen features for the SE panels added 2026-10-26 (Qwen2.5-Coder-7B-Instruct, as for the other code panels). Idempotent: skips panels whose .npz exists.
set -e
cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2
PY=/scratch/jundahe/venvs/llmj/bin/python
nvidia-smi --query-gpu=name,memory.total --format=csv
$PY -c "from huggingface_hub import snapshot_download; snapshot_download('Qwen/Qwen2.5-Coder-7B-Instruct')"
for p in dorn_java dorn_python dorn_cuda jb_naming crupi_ca; do
  if [ -f features/$p/Qwen2.5-Coder-7B-Instruct.npz ]; then echo "skip $p"; continue; fi
  $PY embed_items.py --panel $p
done
# panels that share texts with one above: copy the features (same prompt text, same model) instead of recomputing
for p in jb_logical_separation jb_sufficient_info jb_style_guide jb_short jb_clear_goal; do mkdir -p features/$p; [ -f features/$p/Qwen2.5-Coder-7B-Instruct.npz ] || $PY - <<PYEOF
import numpy as np, data_panels
src=np.load("features/jb_naming/Qwen2.5-Coder-7B-Instruct.npz",allow_pickle=True); P=data_panels.load("$p"); assert np.array_equal(src["item_ids"].astype(str), np.asarray(P["item_ids"]).astype(str))
np.savez("features/$p/Qwen2.5-Coder-7B-Instruct.npz", **{k: src[k] for k in src.files}); print("copied jb_naming features ->", "$p")
PYEOF
done
for p in crupi_conc crupi_flu; do mkdir -p features/$p; [ -f features/$p/Qwen2.5-Coder-7B-Instruct.npz ] || $PY - <<PYEOF
import numpy as np, data_panels
src=np.load("features/crupi_ca/Qwen2.5-Coder-7B-Instruct.npz",allow_pickle=True); P=data_panels.load("$p"); assert np.array_equal(src["item_ids"].astype(str), np.asarray(P["item_ids"]).astype(str))
np.savez("features/$p/Qwen2.5-Coder-7B-Instruct.npz", **{k: src[k] for k in src.files}); print("copied crupi_ca features ->", "$p")
PYEOF
done
echo DONE
