#!/bin/bash
#SBATCH -J p3-ask
#SBATCH -p normal
#SBATCH --gres=gpu:1
#SBATCH -c 2
#SBATCH --mem=20G
#SBATCH -t 03:00:00
#SBATCH -o /scratch/jundahe/LLM-J-ICML/paper-3/logs/slurm_ask_%j.log
cd /scratch/jundahe/LLM-J-ICML/paper-3; PY=/scratch/jundahe/venvs/llmj/bin/python; export OMP_NUM_THREADS=2
for p in dices dices990 popquorn_off8 popquorn_pol5 summeval_coherence8 bw; do [ -f results/ask/$p.npz ] && continue; $PY ask_disagreement.py --panel $p; done; echo DONE
