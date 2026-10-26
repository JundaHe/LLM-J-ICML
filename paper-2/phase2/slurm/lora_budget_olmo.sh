#!/bin/bash
# Fixed-budget LoRA block with a non-Qwen base (OLMo-2-7B-Instruct), SummEval coherence; key designs only (SHRINKAGE_PROTOCOL Amendment 3, cross-family addendum).
#SBATCH -J lora-olmo
#SBATCH -p normal
#SBATCH --gres=gpu:1
#SBATCH -c 4
#SBATCH --mem=16G
#SBATCH -t 12:00:00
#SBATCH -o /scratch/jundahe/LLM-J-ICML/paper-2/phase2/logs/slurm_lora_olmo_%j.log
cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2; PY=/scratch/jundahe/venvs/llmj/bin/python; export OMP_NUM_THREADS=4
SEED=$1; M=allenai/OLMo-2-1124-7B-Instruct
for design in "7 1.0" "1 1.0" "2 0.5" "7 0.142857"; do
  set -- $design; A=$1; F=$2
  for fold in 0 1 2; do
    out=results/lora_budget_olmo/summeval_coherence8/a${A}_F${F}/s${SEED}/f${fold}/chen
    [ -f $out/P_test.npy ] && continue; mkdir -p $out
    if [ "$A" = "7" ] && [ "$F" = "1.0" ]; then EXTRA=""; else EXTRA="--train_pos $A --train_frac $F"; fi
    $PY train_judge_v3.py --panel summeval_coherence8 --model $M --eval_raters 0,1,2 --fold $fold --split 0 --arm chen --max_steps 240 --opt_seed $SEED $EXTRA --out $out > $out/train.log 2>&1
    echo "finished $out $(date +%H:%M) $(grep -c Traceback $out/train.log) tracebacks"
  done
done; echo DONE
