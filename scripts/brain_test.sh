#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH -p gpucpuM
#SBATCH --mem 100G
#SBATCH -c 2
#SBATCH -t 300
#SBATCH -o out_batch
#SBATCH -e err_batch

# Comment this out or modify it if you don't use a virtual environment named "venv"
source venv/bin/activate

python3 agent_play.py $1 $2 $3
