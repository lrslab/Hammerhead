#!/bin/bash
#SBATCH --partition=gpu_7d1g
#SBATCH --nodes=1                # 1 computer nodes
#SBATCH --ntasks-per-node=1      # 1 MPI tasks on EACH NODE
#SBATCH --cpus-per-task=4        # 4 OpenMP threads on EACH MPI TASK
#SBATCH --gres=gpu:1             # Using 2 GPU card
#SBATCH --time=48:00:00        # Time limit day-hrs:min:sec
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

mkdir wgactc
bonito basecaller dna_r10.4.1_e8.2_400bps_sup@v4.2.0 ./R1041_wga/ --save-ctc --reference ./kp1.fa > ./wgactc/basecalls.sam

# train one
bonito train --epochs 40 --lr 5e-4 --batch 32 --pretrained ./dna_r10.4.1_e8.2_400bps_sup@v4.2.0 --directory ./wgactc/ ./fine-tuned-model_e40
#recall
bonito basecaller ./fine-tuned-model_e40 ./R1041_wga/ >./ecoli_wga_e40.sam
bonito basecaller ./fine-tuned-model_e40 ./R1041_wgs/ >./ecoli_wgs_e40.sam

# train another
bonito train --epochs 3 --lr 5e-4 --batch 32 --pretrained ./dna_r10.4.1_e8.2_400bps_sup@v4.2.0 --directory ./wgactc/ ./fine-tuned-model_e3
#recall
bonito basecaller ./fine-tuned-model_e3 ./R1041_wga/ >./ecoli_wga_e3.sam
bonito basecaller ./fine-tuned-model_e3 ./R1041_wgs/ >./ecoli_wgs_e3.sam
