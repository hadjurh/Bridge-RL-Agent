#!/bin/bash
#SBATCH --gres=gpu:1
#SBATCH --mem 8000
#SBATCH -c 2
#SBATCH -t 180
#SBATCH -o out_batch
#SBATCH -e err_batch

venv/bin/python main_learn.py $1