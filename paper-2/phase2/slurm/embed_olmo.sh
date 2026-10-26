#!/bin/bash
#SBATCH -J embed-olmo
#SBATCH -p normal
#SBATCH --gres=gpu:1
#SBATCH -c 4
#SBATCH --mem=24G
#SBATCH -t 06:00:00
#SBATCH -o /scratch/jundahe/LLM-J-ICML/paper-2/phase2/logs/slurm_embed_olmo_%j.log
# Third base family (non-Qwen): OLMo-2-7B-Instruct features for the main panels.
set -e; cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2; PY=/scratch/jundahe/venvs/llmj/bin/python; export OMP_NUM_THREADS=4
M=allenai/OLMo-2-1124-7B-Instruct; $PY -c "from huggingface_hub import snapshot_download; snapshot_download('$M')"
for p in summeval_coherence8 popquorn_off8 chaosnli_mnli hs2_help5 emobank_reader_v5 csc6 dices990 dices bw dorn_java scalabrino; do
  [ -f features/$p/OLMo-2-1124-7B-Instruct.npz ] && { echo "skip $p"; continue; }; $PY embed_items.py --panel $p --model $M
done; echo DONE
