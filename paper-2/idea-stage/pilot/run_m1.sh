#!/bin/bash
# M1 exact commit-Why gate: one GPU runs its share sequentially; skips completed runs.
GPU=$1; shift
cd /mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/pilot
for job in "$@"; do
  arm=${job%%:*}; fold=${job##*:}; out=results_v2/why/s0/f$fold/$arm
  if [ -f "$out/P_test.npy" ]; then echo "skip $out"; continue; fi
  mkdir -p "$out"
  CUDA_VISIBLE_DEVICES=$GPU HF_HUB_OFFLINE=1 conda run -n vespa --no-capture-output python train_judge_v2.py --criterion why --fold $fold --split 0 --arm $arm --out $out > $out/train.log 2>&1
  echo "finished $out $(date +%H:%M)"
done
