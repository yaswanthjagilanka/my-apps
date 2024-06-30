#!/bin/bash

#SBATCH --output=%j.stdout
#SBATCH --error=%j.stderr
#SBATCH --job-name="a3_PDP"
#SBATCH --gres=gpu:tesla_v100-pcie-16gb:1
# --gres=gpu:tesla_v100-pcie-16gb:1(S:0)
# --gres=gpu:tesla_v100-pcie-32gb:1(S:1)
# --gres-flags=disable-binding
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:10:00

module load gcc/6.3.0
module load cuda

./a3 100000 1
./a3 200000 1
./a3 400000 1
./a3 800000 1
./a3 1600000 1
./a3 3200000 1