#!/bin/bash
#SBATCH -J embed-jester
#SBATCH -p normal
#SBATCH --gres=gpu:1
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -t 01:00:00
#SBATCH -o /scratch/jundahe/LLM-J-ICML/paper-2/phase2/logs/slurm_embed_jester_%j.log
# Paper 4 Stage 14 (PROTOCOL_STAGE14.md §1.2): frozen Qwen2.5-7B-Instruct features of the 128 Jester jokes (one row per joke).
set -e
cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2
nvidia-smi --query-gpu=name,memory.total --format=csv
/scratch/jundahe/venvs/llmj/bin/python embed_items.py --panel jester_items
echo DONE
