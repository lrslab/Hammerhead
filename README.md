# Hammerhead
This project is designed to find potential modification sites.



## Workflow

![alt text](figure_demo/Demo_1.png)



The Hammerhead was developed specifically to identify potential modification sites using Nanopore R10.4.1 simplex reads. It leverages the strand-specific error pattern observed in these reads to detect modifications.

The pipeline utilizes a self-defined metric called the difference index to quantify the discrepancy in observed accuracy between the forward and reverse strands at individual sites. This difference index serves as a measure of the potential modification probability. A higher value of the difference index indicates a higher likelihood of modification at the corresponding site.



## Dependence

To use this script, you'll need to install additional tools for read processing, including samtools and minimap2. The following commands can help you install dependencies.

```shell
# test verison for dependences
# minimap2	2.17
# samtools	1.17

conda install -c bioconda -c conda-forge minimap2 samtools
```



## General usage

`Hammerhead` can be run using a simple command:

```
python hammerhead.py -ref <reference> -read <input_fastq>
```

The help for `Hammerhead`:

```
python hammerhead.py -h
usage: hammerhead.py [-h] --ref  --read  [--cpu] [--cut] [--min_depth] [--min_depth_strand]

A tool help to find the potential modification sites

optional arguments:
  -h, --help           show this help message and exit
  --ref                Input reference (FASTA)
  --read               Input reads (FASTQ)
  --cpu                CPU number. (default:10)
  --cut                Cutoff value [0, 1]. (default:0.35)
  --min_depth          The minimum depth. (default:50)
  --min_depth_strand   The minimum depth for forward strand and reverse strand. (default:25)
```


## Results

The results file for `Hammerhead`:

```
├── test.fastq
├── ref.fasta
├── mapping.mpileup.txt
├── mapping.sort.bam
├── potential_modification_site_detail.bed
└── potential_modification_site_detail.txt
```

- `test.fastq` - input fastq reads

- `ref.fasta` - reference

- `mapping.sort.bam` - aligned bam file

- `potential_modification_site_detail.bed` - the position for potential modification sites

- `potential_modification_site_detail.txt` - the details for potential modification sites

  ```
  Chr	Pos	Difference_index	Dif_A	Dif_T	Dif_G	Dif_C	A,T,G,C,a,t,g,c
  contig_2	2541	0.386	0.0	0.386	0.0	0.386	0,2,0,191,0,25,0,38
  contig_2	2836	0.395	0.395	0.0	0.279	0.116	52,0,24,10,129,0,0,0
  contig_2	2837	0.475	0.474	0.029	0.413	0.033	37,1,40,0,0,5,112,4
  ```

​		A, T, G, C, a, t, g, c  is the number of reads mapped as the  A/T/G/C in the forward strand and T/A/C/G in the reverse strand.



**All rights reserved.**
