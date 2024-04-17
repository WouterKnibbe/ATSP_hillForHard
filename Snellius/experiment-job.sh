#!/bin/bash
#Set job requirements
#SBATCH --nodes=1
#SBATCH --ntasks=10
#SBATCH --partition=rome
#SBATCH --time=48:00:00
 
#Loading modules
module load 2022
module load Python/3.10.4-GCCcore-11.3.0
pip install numpy

# Define the experiment parameters for each task
declare -a param1=("[30]" "[30]" "[50]" "[50]" "[70]" "[70]" "[70]" "[100]" "[100]" "[100]")
declare -a param2=("[100]" "[1000]" "[100]" "[1000]" "[10]" "[100]" "[1000]" "[10]" "[100]" "[1000]")
declare -a param3=(2000 2000 2000 2000 2000 2000 2000 2000 2000 2000)
declare -a param4=("[(30,100)]" "[(30,1000)]" "[(50,100)]" "[(50,1000)]" "[(70,10)]" "" "" "[(100,10)]" "" "")


# Execute the program N times, where N=ntasks requested to SLURM. In this example we request all the cores availables on the node.
# The '&' sign is used to start each program in the background, so that the programs start running concurrently.
for i in $(seq 0 $(($SLURM_NTASKS-1))); do
    srun --ntasks=1 --nodes=1 --cpus-per-task=1 python -u /gpfs/home3/wknibbe/ATSP_hillForHard/Snellius/experiment.py ${param1[$i]} ${param2[$i]} ${param3[$i]} ${param4[$i]} &
done
wait