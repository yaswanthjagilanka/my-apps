#!/bin/bash

####### PLANEX SPECIFIC - DO NOT EDIT THIS SECTION
#SBATCH --partition=general-compute
#SBATCH --qos=general-compute
#SBATCH --exclusive
#SBATCH --mem=64000
#SBATCH --output=%j.stdout
#SBATCH --error=%j.stderr

####### CUSTOMIZE THIS SECTION FOR YOUR JOB
#SBATCH --job-name="changeme"
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --time=00:15:00

module load intel-mpi/2019.5

# if using Intel MPI add need this
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so

srun --mpi=pmi2 /user/yjagilan/A1/A1/a1 320000
