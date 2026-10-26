#!/bin/bash
#SBATCH -J embed-q3
#SBATCH -p normal
#SBATCH --gres=gpu:1
#SBATCH -c 4
#SBATCH --mem=24G
#SBATCH -t 06:00:00
#SBATCH -o /scratch/jundahe/LLM-J-ICML/paper-2/phase2/logs/slurm_embed_qwen3_%j.log
# Second base family for the frozen-feature instruments (addresses the one-family limitation): Qwen3-8B (2025) features for the main panels.
set -e; cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2; PY=/scratch/jundahe/venvs/llmj/bin/python; export OMP_NUM_THREADS=4
M=Qwen/Qwen3-8B; $PY -c "from huggingface_hub import snapshot_download; snapshot_download('$M')"
for p in summeval_coherence8 popquorn_off8 chaosnli_mnli hs2_help5 emobank_reader_v5 csc6 dices990 dices bw dorn_java scalabrino; do
  [ -f features/$p/Qwen3-8B.npz ] && { echo "skip $p"; continue; }; $PY embed_items.py --panel $p --model $M
done; echo DONE
