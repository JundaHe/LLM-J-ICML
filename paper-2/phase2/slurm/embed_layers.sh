#!/bin/bash
#SBATCH -J embed-layers
#SBATCH -p normal
#SBATCH --gres=gpu:1
#SBATCH -c 4
#SBATCH --mem=48G
#SBATCH -t 04:00:00
#SBATCH -o /scratch/jundahe/LLM-J-ICML/paper-2/phase2/logs/slurm_embed_layers_%j.log
cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2; PY=/scratch/jundahe/venvs/llmj/bin/python; export OMP_NUM_THREADS=4
for p in summeval_coherence8 popquorn_off8 chaosnli_mnli hs2_help5 emobank_reader_v5 csc6; do
  [ -f features_layers/$p/*.npz ] && { echo "skip $p"; continue; }
  $PY embed_layers.py --panel $p
done
echo DONE
