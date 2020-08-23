#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH -p gpucpuM
#SBATCH --mem 8000
#SBATCH -c 2
#SBATCH -t 800
#SBATCH -o out_batch
#SBATCH -e err_batch

# Comment this out or modify it if you don't use a virtual environment named "venv"
source venv/bin/activate

python3 qlearning_learn.py $1 $2
