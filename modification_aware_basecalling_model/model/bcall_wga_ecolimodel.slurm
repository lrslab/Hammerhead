#!/bin/bash
#SBATCH --partition=stingy
#SBATCH --nodes=1                # 1 computer nodes
#SBATCH --ntasks-per-node=1      # 1 MPI tasks on EACH NODE
#SBATCH --cpus-per-task=4        # 4 OpenMP threads on EACH MPI TASK
#SBATCH --gres=gpu:1             # Using 2 GPU card
#SBATCH --time=6:00:00        # Time limit day-hrs:min:sec
#SBATCH --output=gpujob_%j.log   # Standard output
#SBATCH --error=gpujob_%j.err    # Standard error log
#SBATCH --mem=64GB


OUTPUT=./bonito_out
hostname > ./hostname
nvidia-smi > ./nvidia-smi
eval "$(conda shell.bash hook)"
cd .
source /home/runsheli/miniconda3/bin/activate bonito
conda activate bonito
which python > ./pythonenv

bonito basecaller /home/runsheli/scratch/data/CCWGG_test/ecoli/fine-tuned-model40 ./R1041_wga/ >./kp1_ecolimodel_wga_model_e40.sam

