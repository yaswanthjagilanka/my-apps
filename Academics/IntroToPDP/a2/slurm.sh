#!/bin/bash

####### BASIC SPECIFICATION
#SBATCH --clusters=faculty
#SBATCH --partition=planex
#SBATCH --qos=planex
#SBATCH --account=cse570f21
#SBATCH --exclusive
#SBATCH --mem=64000

####### CUSTOMIZE THIS SECTION FOR YOUR JOB
####### NOTE: --ntasks-per-node SHOULD BE SET TO INCLUDE ALL CORES IN A NODE
####### YOU CAN CONTROL CORE-TO-EXECUTOR RATIO VIA SPARK_ARGS
#SBATCH --job-name="A2_PDP"
#SBATCH --nodes=3
#SBATCH --ntasks-per-node=20
#SBATCH --output=%j.stdout
#SBATCH --error=%j.stderr
#SBATCH --time=06:00:00

# IF SET TO 1 SPARK MASTER RUNS ON A SEPARATE NODE
exclude_master=0

# ADD EXTRA MODULES HERE IF NEEDED
# CHECK WHICH SPARK MODUKE TO LOAD
module load spark/2.4.0-py37

# SET YOUR COMMAND AND ARGUMENTS
PROG="a2.py"
ARGS="/panasas/scratch/grp-jzola/intropdp/T0.txt /panasas/scratch/grp-cse570f21/yjagilan/output50"

# SET EXTRA OPTIONS TO spark-submit
# EXAMPLE OPTIONS:
# --num-executors
# --executor-cores
# --executor-memory
# --driver-cores
# --driver-memory
# --py-files
SPARK_ARGS="--conf spark.default.parallelism=40 --num-executors 8  --executor-cores 5 --executor-memory 12G"



####### DO NOT EDIT BELOW
SPARK_PATH=$SPARK_HOME

# GET LIST OF NODES
NODES=(`srun hostname | sort | uniq`)

NUM_NODES=${#NODES[@]}
LAST=$((NUM_NODES - 1))

# FIRST NODE IS MASTER
ssh ${NODES[0]} "export SPARK_LOG_DIR=$SLURMTMPDIR; export SPARK_LOCAL_DIRS=$SLURMTMPDIR; export SPARK_WORKER_DIR=$SLURMTMPDIR; cd $SPARK_PATH; ./sbin/start-master.sh"
MASTER="spark://${NODES[0]}:7077"

WHO=`whoami`

echo -e "\n**********"
echo -e "UI tunnel:\nssh $WHO@vortex.ccr.buffalo.edu -L 4040:${NODES[0]}:4040 -N"
echo -e "**********\n"

TEMP_OUT_DIR=$SLURM_SUBMIT_DIR/spark-$SLURM_JOB_ID

# ALL NODES ARE WORKERS
mkdir -p $TEMP_OUT_DIR
for i in `seq $exclude_master $LAST`; do
  ssh ${NODES[$i]} "export SPARK_LOG_DIR=$SLURMTMPDIR; export SPARK_LOCAL_DIRS=$SLURMTMPDIR; export SPARK_WORKER_DIR=$SLURMTMPDIR; cd $SPARK_PATH; nohup ./bin/spark-class org.apache.spark.deploy.worker.Worker $MASTER &> $TEMP_OUT_DIR/nohup-${NODES[$i]}.$i.out" &
done

# SUBMIT JOB
export SPARK_LOG_DIR=$SLURMTMPDIR
export SPARK_LOCAL_DIRS=$SLURMTMPDIR
export SPARK_WORKER_DIR=$SLURMTMPDIR

$SPARK_PATH/bin/spark-submit --master $MASTER $SPARK_ARGS $PROG $ARGS

# CLEAN SPARK JOB
ssh ${NODES[0]} "cd $SPARK_PATH; ./sbin/stop-master.sh"

for i in `seq 0 $LAST`; do
  ssh ${NODES[$i]} "killall java"
done
