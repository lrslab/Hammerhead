The new basecalling model was fine-tuned from the original DNA super accuracy model (SUP) using [bonito](https://github.com/nanoporetech/bonito) (V0.7.2) with the following parameters “--epochs 40 --lr 5e-4 --batch 32 --pretrained dna_r10.4.1_e8.2_400bps_sup@v4.2.0”.
The model file is available at here.

**Note**: To prepare the input “sam” file for training, the parameter “save-ctc” has to be enabled in the bonito basecaller.   

