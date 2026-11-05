#!/bin/bash
#SBATCH -J r19_7_brier
#SBATCH -p normal
#SBATCH --gres=gpu:1
#SBATCH -c 4
#SBATCH --mem=16G
#SBATCH -t 12:00:00
#SBATCH -o logs/r19_7_brier.log
cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2
export OMP_NUM_THREADS=4
for p in chaosnli_snli chaosnli_alphanli chaosnli_mnli; do for m in 5 10 20 50; do
  /scratch/jundahe/venvs/llmj/bin/python probe_nominal.py --panel $p --m $m --tag _v7b > logs/r19_7_${p}_m$m.log 2>&1 || echo "FAIL $p $m"
  echo "done $p $m $(date +%T)"
done; done
