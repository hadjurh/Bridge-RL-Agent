#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --mem 8000
#SBATCH -c 2
#SBATCH -t 300
#SBATCH -o out_batch
#SBATCH -e err_batch

source venv/bin/activate

python3 agent_play.py $1 $2