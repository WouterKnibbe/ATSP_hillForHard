#!/bin/bash
#Set job requirements
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --partition=rome
#SBATCH --time=06:00:00
 
#Loading modules
module load 2022
module load Python/3.10.4-GCCcore-11.3.0
pip install numpy

# Define the experiment parameters for each task
declare -a param1=("[30]" "[50]" "[70]" "[100]")
declare -a param2=("[10000]" "[10000]" "[10000]" "[10000]")
declare -a param3=(500 500 500 500)

# Function to monitor the directory and copy files as they are created
function monitor_and_copy {
    local watch_dir="$1"
    local target_dir="$2"

    inotifywait -m -e close_write --format '%w%f' "$watch_dir" | while read newfile
    do
        echo "New file detected: $newfile"
        # Copy the new file to the target directory
        cp "$newfile" "$target_dir/"
    done
}

# Start monitoring in the background
monitor_and_copy "./" "$SLURM_SUBMIT_DIR" &

# Execute the program N times, where N=ntasks requested to SLURM. In this example we request all the cores availables on the node.
# The '&' sign is used to start each program in the background, so that the programs start running concurrently.
for i in $(seq 0 $(($SLURM_NTASKS-1))); do
    srun --ntasks=1 --nodes=1 --cpus-per-task=1 python /gpfs/home3/wknibbe/ATSP_hillForHard/Snellius/experiment.py ${param1[$i]} ${param2[$i]} ${param3[$i]} &
done
wait

# Kill the monitor process after the jobs are done
kill $!