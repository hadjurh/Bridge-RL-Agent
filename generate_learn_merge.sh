#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --mem 8000
#SBATCH -c 2
#SBATCH -t 600
#SBATCH -o out_batch
#SBATCH -e err_batch

source venv/bin/activate

python3 main_generate.py $1 $2
python3 main_learn.py $3
python3 merge_dictionaries.py $4