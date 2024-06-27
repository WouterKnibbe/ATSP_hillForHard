# Where the really hard problems actually are
> *Hill-climbing the Assymmetric Travelling Salesman Problem for hardness*

This repository contains the code used for the experiments and plots in the thesis "Where the Really Hard Problems Actually Are" by Wouter Knibbe. The thesis investigates the hardness of the Asymmetric Traveling Salesman Problem (ATSP) and how it can be increased through hill-climbing techniques.

## Overview

The Asymmetric Traveling Salesman Problem (ATSP) is a classic combinatorial optimization problem where the goal is to find the shortest possible route that visits a set of cities once and returns to the origin city. Unlike the symmetric version, the distance from city A to city B is not necessarily the same as from city B to city A. This repository explores the hardness of ATSP instances using randomly generated distance matrices and hill-climbing methods.

## Repository Structure

- **Snellius/**: Contains job scripts and Python programs for running experiments.
  - `algorithm.py`: Implements the main algorithm used to solve ATSP, Little's algorithm. Courtesy of [Sleegers et al.](https://github.com/Joeri1324/Littles-Algorithm-Sleegers-et-al.).
  - `experiment.py`: Runs the experiment using the hill-climbing approach.
  - `experiment-job.sh`: Bash script for submitting jobs to the Snellius supercomputer.
  - `Progress/v1/`: Directory for storing intermediate results.
  
- **Data Files**: JSON files storing distance matrices and their hardness metrics.
  - `easy_y_values_wstd_30.json`, `easy_y_values_wstd_50.json`, `easy_y_values_wstd_70.json`: Matrices and hardness values for starting instances.
  - `last_y_values_30.json`, `last_y_values_50.json`, `last_y_values_70.json`: Final hardness values for different city sizes.
  - `animation30.gif`, `animation50.gif`, `animation70.gif`: Visual animations of the hill-climbing process for various matrix sizes.

- **Notebooks**: Jupyter notebooks for data analysis and visualization.
  - `Early experiments.ipynb`: Initial experimental setup and results.
  - `GetLastMatrix.ipynb`: Retrieves the final matrices so they can be continued in a second run.
  - `Plots.ipynb`: Generates the core content and plots for the thesis.

## Getting Started

### Prerequisites

To run the code in this repository, you will need:
- Python 3.7 or later
- NumPy
- Matplotlib
- Jupyter Notebook
- The various libraries mentioned at the top of each notebook

### Repository Usage

The main code files for running experiments are located in the `Snellius` directory. The job script (`experiment-job.sh`) is designed to be executed on the Snellius supercomputer, which schedules and runs the hill-climbing experiments. The Python files implement the core functionality of the algorithm and handle the experimental logic.

### Data Analysis

The JSON files store the results of the experiments, including the hardness values of various ATSP instances. The Jupyter notebooks provide a comprehensive analysis and visualization of the data, which can be used to generate plots and insights for research purposes.

## Results

The thesis found that hill-climbing ATSP distance matrices can effectively increase problem hardness. The hill-climber improved the hardness of all matrices, with some instances showing a median increase in hardness by over 1,000 times. Phase transitions in problem hardness were observed, with smaller city sizes experiencing these transitions at lower random maximum values (randmax).

## References

For a detailed explanation of the methodology and results, please refer to the thesis [Where the Really Hard Problems Actually Are](https://github.com/WouterKnibbe/ATSP_hillForHard).
