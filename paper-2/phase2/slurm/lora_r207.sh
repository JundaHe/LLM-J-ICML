#!/bin/bash
# ROUND20 R20-7: rater-subset targets (experts2, crowd5) on SummEval, Qwen2.5. Usage: sbatch slurm/lora_r207.sh <opt_seed>
#SBATCH -J lora-r207
#SBATCH -p normal
#SBATCH --gres=gpu:1
#SBATCH -c 4
#SBATCH --mem=16G
#SBATCH -t 20:00:00
#SBATCH -o /scratch/jundahe/LLM-J-ICML/paper-2/phase2/logs/slurm_lora_r207_%j.log
cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2; PY=/scratch/jundahe/venvs/llmj/bin/python; export OMP_NUM_THREADS=4
SEED=$1; nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
for arm in "experts2 0,1,2" "crowd5 3,4,5,6,7"; do
  set -- $arm; NAME=$1; COLS=$2
  for fold in 0 1 2; do
    out=results/lora_budget_r207/summeval_coherence8/${NAME}/s${SEED}/f${fold}/chen
    [ -f $out/P_test.npy ] && { echo "skip $out"; continue; }; mkdir -p $out
    $PY train_judge_v3.py --panel summeval_coherence8 --eval_raters 0,1,2 --fold $fold --split 0 --arm chen --max_steps 240 --opt_seed $SEED --train_cols $COLS --out $out > $out/train.log 2>&1
    echo "finished $out $(date +%H:%M) $(grep -c Traceback $out/train.log) tracebacks $(grep -oE 'rating budget [0-9]+' $out/train.log | tail -1)"
  done
done
echo DONE
