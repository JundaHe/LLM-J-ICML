#!/bin/bash
# ROUND21 CPU jobs. Usage: sbatch -o logs/<name>.log slurm/r21_cpu.sh <script.py> <args...>
#SBATCH -J r21
#SBATCH -p normal
#SBATCH -c 1
#SBATCH --mem=3G
#SBATCH -t 16:00:00
cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2; export OMP_NUM_THREADS=1
/scratch/jundahe/venvs/llmj/bin/python "$@"
