#!/bin/bash
# Generic CPU runner: runs every line of a command file with xargs -P $PAR inside one Slurm allocation (threads per command = SLURM_CPUS_PER_TASK / PAR).
# Usage: sbatch -c <cpus> -J <name> slurm/run_cpu.sh <commands.txt> <PAR>
#SBATCH -p normal
#SBATCH --mem=24G
#SBATCH -t 23:00:00
#SBATCH -o /scratch/jundahe/LLM-J-ICML/paper-2/phase2/logs/slurm_%x_%j.log
cd /scratch/jundahe/LLM-J-ICML/paper-2/phase2
CMDS=$1; PAR=${2:-1}; T=$(( ${SLURM_CPUS_PER_TASK:-4} / PAR )); [ $T -lt 1 ] && T=1
export OMP_NUM_THREADS=$T OPENBLAS_NUM_THREADS=$T MKL_NUM_THREADS=$T
echo "job $SLURM_JOB_ID: $(wc -l < $CMDS) commands, parallel $PAR, $T threads each"; date
xargs -P $PAR -I{} bash -c '{}' < $CMDS
echo DONE; date
