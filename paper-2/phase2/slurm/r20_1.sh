#!/bin/bash
#SBATCH -J r20_1
#SBATCH -p normal
#SBATCH -c 1
#SBATCH --mem=3G
#SBATCH -t 16:00:00
cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
/scratch/jundahe/venvs/llmj/bin/python decode_decomp.py "$@" --R 10 --B 200 --R_boot 3
