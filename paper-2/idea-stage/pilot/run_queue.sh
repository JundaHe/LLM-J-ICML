#!/bin/bash
# usage: run_queue.sh GPU CRITERION job ...   (job = arm:fold:split[:model_tag]); CRITERION=readability selects the readability panel; skips completed runs
GPU=$1; CRIT=$2; shift 2
cd /mnt/hdd2/jundahe/LLM-J/paper-2/idea-stage/pilot
for job in "$@"; do
  IFS=: read arm fold split tag <<< "$job"; tag=${tag:-qwen}
  out=results_v2/$CRIT/s$split/$( [ "$tag" = "qwen" ] && echo "" || echo "$tag/" )f$fold/$arm
  if [ -f "$out/P_test.npy" ]; then echo "skip $out"; continue; fi
  mkdir -p "$out"; model="Qwen/Qwen2.5-Coder-7B-Instruct"; [ "$tag" = "llama" ] && model="meta-llama/Llama-3.1-8B-Instruct"; [ "$tag" = "deepseek" ] && model="deepseek-ai/deepseek-coder-6.7b-instruct"
  CUDA_VISIBLE_DEVICES=$GPU HF_HUB_OFFLINE=1 conda run -n vespa --no-capture-output python train_judge_v2.py --panel $( [ "$CRIT" = "readability" ] && echo readability || echo commit ) --criterion $CRIT --fold $fold --split $split --arm $arm --model $model --out $out > $out/train.log 2>&1
  echo "finished $out $(date +%H:%M)"
done
