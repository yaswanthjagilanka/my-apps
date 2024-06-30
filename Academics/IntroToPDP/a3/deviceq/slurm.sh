#!/bin/bash

#SBATCH --output=%j.stdout
#SBATCH --error=%j.stderr
#SBATCH --job-name="a3_PDP"
#SBATCH --gres=gpu:tesla_v100-pcie-16gb:1
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:10:00

module load gcc/6.3.0
module load cuda

./dq