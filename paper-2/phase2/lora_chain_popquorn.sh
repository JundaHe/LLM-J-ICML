#!/bin/bash
# POPQUORN-offensiveness LoRA block (second end-to-end dataset): chen / perm / perm_mode × 3 position folds × joint seeds
# {opt 2000/perm 1000 → s0, 2001/2501 → s0_seed2001, 2002/2502 → s0_seed2002}. Same trainer flags as the SummEval block (chain7b).
# Usage: bash lora_chain_popquorn.sh <gpu> <opt_seed> [<opt_seed> ...]   e.g. one GPU per seed:  bash lora_chain_popquorn.sh 1 2000
# Finished cells (P_test.npy present) are skipped, so the script is safe to re-run after an interruption.
GPU=$1; shift
cd "$(dirname "$(readlink -f "$0")")"; export CUDA_VISIBLE_DEVICES=$GPU; unset HF_HUB_OFFLINE; PY=${PY:-python}   # set PY to the env with torch/transformers/peft
for seed in "$@"; do for arm in chen perm perm_mode; do for fold in 0 1 2; do
  if [ $seed = 2000 ]; then out=results/lora/popquorn_off8/s0/f$fold/$arm; ps=1000; else out=results/lora/popquorn_off8/s0_seed$seed/f$fold/$arm; ps=$((seed+500)); fi
  [ -f $out/P_test.npy ] && continue; mkdir -p $out
  $PY train_judge_v3.py --panel popquorn_off8 --eval_raters 0,1,2 --fold $fold --split 0 --arm $arm --epochs 2 --opt_seed $seed --perm_seed $ps --out $out > $out/train.log 2>&1
  echo "finished $out on GPU $GPU $(date +%H:%M) $(grep -c Traceback $out/train.log) tracebacks"
done; done; done
