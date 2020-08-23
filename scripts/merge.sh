#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH -p gpucpuM
#SBATCH --mem 15000
#SBATCH -c 2
#SBATCH -t 1000
#SBATCH -o out_batch
#SBATCH -e err_batch

# Comment this out or modify it if you don't use a virtual environment named "venv"
source venv/bin/activate

python3 merge_dictionaries.py $1 $2
