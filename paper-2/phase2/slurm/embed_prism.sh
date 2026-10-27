#!/bin/bash
#SBATCH -J embed-prism
#SBATCH -p normal
#SBATCH --gres=gpu:1
#SBATCH -c 2
#SBATCH --mem=20G
#SBATCH -t 10:00:00
#SBATCH -o /scratch/jundahe/LLM-J-ICML/paper-2/phase2/logs/slurm_embed_prism_%j.log
cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2; PY=/scratch/jundahe/venvs/llmj/bin/python; export OMP_NUM_THREADS=2
for p in prism; do [ -f features/$p/Qwen2.5-7B-Instruct.npz ] || $PY embed_items.py --panel $p; done; echo DONE
