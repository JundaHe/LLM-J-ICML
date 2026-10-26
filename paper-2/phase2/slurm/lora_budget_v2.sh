#!/bin/bash
# Fixed-budget LoRA block on SummEval coherence (SHRINKAGE_PROTOCOL.md Amendment 3). One optimizer seed per job (one GPU each); finished cells (P_test.npy) are skipped.
# Usage: sbatch slurm/lora_budget.sh <opt_seed>
#SBATCH -J lora-bv2
#SBATCH -p normal
#SBATCH --gres=gpu:1
#SBATCH -c 4
#SBATCH --mem=12G
#SBATCH -t 12:00:00
#SBATCH -o /scratch/jundahe/LLM-J-ICML/paper-2/phase2/logs/slurm_lora_bv2_%j.log
cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2; PY=/scratch/jundahe/venvs/llmj/bin/python; export OMP_NUM_THREADS=4
SEED=$1; nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
for design in "7 1.0" "1 1.0" "2 0.5" "7 0.142857"; do
  set -- $design; A=$1; F=$2
  for fold in 0 1 2; do
    out=results/lora_budget_v2/summeval_coherence8/a${A}_F${F}/s${SEED}/f${fold}/chen
    [ -f $out/P_test.npy ] && { echo "skip $out"; continue; }; mkdir -p $out
    $PY train_judge_v3.py --panel summeval_coherence8 --eval_raters 0,1,2 --fold $fold --split 0 --arm chen --max_steps 240 --opt_seed $SEED $( [ "$A" = 7 ] && [ "$F" = 1.0 ] || echo "--train_pos $A --train_frac $F" ) --out $out > $out/train.log 2>&1
    echo "finished $out $(date +%H:%M) $(grep -c Traceback $out/train.log) tracebacks $(grep -oE 'rating budget [0-9]+' $out/train.log)"
  done
done
echo DONE
