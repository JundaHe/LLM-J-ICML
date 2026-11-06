#!/bin/bash
# ROUND22 R22-5: dices a = 40 decoding with Qwen3 and OLMo-2 features (CPU).
#SBATCH -J r22-5
#SBATCH -p normal
#SBATCH -c 2
#SBATCH --mem=8G
#SBATCH -t 2:00:00
#SBATCH -o /scratch/jundahe/LLM-J-ICML/paper-2/phase2/logs/r22_5_%j.log
cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2; export OMP_NUM_THREADS=2; PY=/scratch/jundahe/venvs/llmj/bin/python
$PY decode_decomp.py --panel dices --a 40 --R 10 --B 0 --feat_model Qwen3-8B --tag _a40_qwen3_r22 && echo "done qwen3"
$PY decode_decomp.py --panel dices --a 40 --R 10 --B 0 --feat_model OLMo-2-1124-7B-Instruct --tag _a40_olmo_r22 && echo "done olmo"
echo DONE
