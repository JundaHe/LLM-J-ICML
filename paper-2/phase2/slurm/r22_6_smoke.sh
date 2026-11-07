#!/bin/bash
# ROUND22 R22-6 smoke: disp path must reproduce R22-3 exactly; polar path runs.
#SBATCH -J r22-6s
#SBATCH -p normal
#SBATCH -c 2
#SBATCH --mem=8G
#SBATCH -t 1:00:00
#SBATCH -o /scratch/jundahe/LLM-J-ICML/paper-2/phase2/logs/r22_6_smoke_%j.log
cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2; export OMP_NUM_THREADS=2; PY=/scratch/jundahe/venvs/llmj/bin/python
$PY decode_decomp.py --panel dices --a 40 --R 10 --B 0 --tag _r22smoke --plant 0.4 --plant_seed 0
$PY decode_decomp.py --panel dices --a 40 --R 10 --B 0 --tag _r22psmoke --plant 0.4 --plant_seed 0 --plant_kind polar
echo DONE
