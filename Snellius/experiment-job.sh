#!/bin/bash
#Set job requirements
#SBATCH --nodes=1
#SBATCH --ntasks=75
#SBATCH --partition=rome
#SBATCH --time=48:00:00

#Loading modules
module load 2022
module load Python/3.10.4-GCCcore-11.3.0
pip install numpy

# Define the experiment parameters for each task (once, outside the loop)
declare -a param1=("[5]" "[5]" "[5]" "[5]" "[5]" "[6]" "[6]" "[6]" "[6]" "[6]" "[7]" "[7]" "[7]" "[7]" "[7]")
declare -a param2=("[10]" "[15]" "[20]" "[25]" "[30]" "[10]" "[15]" "[20]" "[25]" "[30]" "[10]" "[15]" "[20]" "[25]" "[30]")
declare -a param3=(300 300 300 300 300 300 300 300 300 300 300 300 300 300 300)
declare -a param4=("" "" "" "" "" "" "" "" "" "" "" "" "" "" "")

# Repeat the job in 5 different runs
for run in {1..5}; do
    # Create a new directory for this run based on the run number and change to this directory
    run_dir="/gpfs/home3/wknibbe/ATSP_hillForHard/Snellius/${SLURM_JOB_ID}_run${run}"
    mkdir -p $run_dir
    cd $run_dir

    # Execute the program 15 times, as per the ntasks
    for i in $(seq 0 $(($SLURM_NTASKS-1))); do
        srun --ntasks=1 --nodes=1 --cpus-per-task=1 python -u /gpfs/home3/wknibbe/ATSP_hillForHard/Snellius/experiment.py ${param1[$i]} ${param2[$i]} ${param3[$i]} ${param4[$i]} &
    done

done
wait