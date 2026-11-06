#!/bin/bash
# ROUND22 R22-3: dices plants at a = 40 (sequential, CPU).
#SBATCH -J r22-3
#SBATCH -p normal
#SBATCH -c 2
#SBATCH --mem=8G
#SBATCH -t 8:00:00
#SBATCH -o /scratch/jundahe/LLM-J-ICML/paper-2/phase2/logs/r22_3_%j.log
cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2; export OMP_NUM_THREADS=2; PY=/scratch/jundahe/venvs/llmj/bin/python
for g in 0 0.1 0.2 0.3 0.4; do for s in 0 1 2 3 4; do
  f=results/decode_decomp/dices_r22_plant${g}_s${s}.json; [ -f $f ] && { echo "skip $f"; continue; }
  $PY decode_decomp.py --panel dices --a 40 --R 10 --B 0 --tag _r22 --plant $g --plant_seed $s && echo "done $g $s $(date +%H:%M)"
done; done; echo DONE
