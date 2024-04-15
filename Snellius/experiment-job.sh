#!/bin/bash
#Set job requirements
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --partition=rome
#SBATCH --time=26:00:00
 
#Loading modules
module load 2022
module load Python/3.10.4-GCCcore-11.3.0
pip install numpy

# Define the experiment parameters for each task
declare -a param1=("[30]" "[30]" "[50]" "[70]" "[100]" "[30]" "[50]" "[50]")
declare -a param2=("[10]" "[1000]" "[10]" "[10]" "[10]"  "[100]" "[100]" "[1000]")
declare -a param3=(1500 2000 1200 900 900 2000 1500 1500)
declare -a param4=("[(30,10)]" "[(30,1000)]" "[(50,10)]" "[(70,10)]" "[(100,10)]")


# Execute the program N times, where N=ntasks requested to SLURM. In this example we request all the cores availables on the node.
# The '&' sign is used to start each program in the background, so that the programs start running concurrently.
for i in $(seq 0 $(($SLURM_NTASKS-1))); do
    srun --ntasks=1 --nodes=1 --cpus-per-task=1 python -u /gpfs/home3/wknibbe/ATSP_hillForHard/Snellius/experiment.py ${param1[$i]} ${param2[$i]} ${param3[$i]} ${param4[$i]} &
done
wait