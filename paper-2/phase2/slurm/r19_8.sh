#!/bin/bash
#SBATCH -J r19_8
#SBATCH -p normal
#SBATCH -c 4
#SBATCH --mem=6G
#SBATCH -t 6:00:00
cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2
export OMP_NUM_THREADS=4
/scratch/jundahe/venvs/llmj/bin/python decode_validity.py "$@"
