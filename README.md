# Hammerhead
<a href="https://pypi.python.org/pypi/Hammerhead-View" rel="pypi">![PyPI](https://img.shields.io/pypi/v/Hammerhead-View?color=green) </a> 
[![License: GPL v2](https://img.shields.io/badge/License-GPL_v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)

This project is designed to find potential modification sites.



## Workflow

![alt text](figure_demo/Demo_1.png)



The Hammerhead was developed specifically to identify potential modification sites using Nanopore R10.4.1 simplex reads. It leverages the strand-specific error pattern observed in these reads to detect modifications.



The pipeline utilizes a self-defined metric called the difference index to quantify the discrepancy in observed accuracy between the forward and reverse strands at individual sites. This difference index serves as a measure of the potential modification probability. A higher value of the difference index indicates a higher likelihood of modification at the corresponding site.



## Installation

To use this tool, you'll need to install additional tools or packages for read processing, including samtools and minimap2. The following command can help you install dependencies.

```shell
# test verison for dependences
# minimap2	2.17
# samtools	1.17
# bedtools	2.30.0

conda install -c bioconda -c conda-forge minimap2 samtools bedtools
```

To install this tool, please using the following command.
```shell
pip install Hammerhead-View
```




## General usage

`Hammerhead` can be run using a simple command:

```
hammerhead --ref <reference> --read <input_fastq>
```

The help for `Hammerhead`:

```
hammerhead -h
usage: hammerhead [-h] --ref  --read  [--cpu] [--cut] [--min_depth] [--min_depth_strand]

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
├── mapping.mpileup.txt
├── mapping.sort.bam
├── potential_modification_site_detail.bed
├── potential_modification_site_detail.txt
├── enrichment.bed
└── enrichment.fa
```

- `mapping.mpileup.txt` - the mpileup file

- `mapping.sort.bam` - the aligned bam file

- `enrichment.bed` - the position of sequences around the potential modification sites used for the motif enrichment analysis (-9 bp, +10 bp).

- `enrichment.fa` - the sequences around the potential modification sites used for the motif enrichment analysis (-9 bp, +10 bp).

- `potential_modification_site_detail.bed` - the position for potential modification sites

- `potential_modification_site_detail.txt` - the details for potential modification sites

  ```
  Chr	Pos	Difference_index	Dif_A	Dif_T	Dif_G	Dif_C	A,T,G,C,a,t,g,c
  contig_2	2541	0.386	0.0	0.386	0.0	0.386	0,2,0,191,0,25,0,38
  contig_2	2836	0.395	0.395	0.0	0.279	0.116	52,0,24,10,129,0,0,0
  contig_2	2837	0.475	0.474	0.029	0.413	0.033	37,1,40,0,0,5,112,4
  ```

​		A, T, G, C, a, t, g, c  is the number of reads mapped as the  A/T/G/C in the forward strand and T/A/C/G in the reverse strand.



## Tool showcase

To show the potential of Hammerhead to identify the modifications in the bacterium. Here, two datasets from  *E. coli* were used to call methylation including whole-genome sequencing (WGS) and whole-genome amplification (WGA) R10.4.1 simplex reads. The *dam* and *dcm* genes were found in the genome of the used *E. coli* strain. These two genes are associated with the G6mATC and C5mCWGG methylation.





![alt text](figure_demo/Demo_2.png)

The distribution of difference index for sites in *E. coli* genome. The WGA reads were used as a negative control due to the lack of inherent methylation information. Based on the background noise of WGA reads, the sites with a difference index over 0.35 were regarded as potential modification sites.





![alt text](figure_demo/Demo_3.png)

The motif of C<u>C</u>WGG and G<u>A</u>TC was enriched using the sequence near these potential modification sites (-10 bp to +9 bp). 



**Note:** Two datasets are available at the [here](https://figshare.com/articles/dataset/_i_E_coli_i_datasets/24298663). Both datasets were basecalled using the modification aware model, which is available in the directory of `modification_aware_basecalling_model`.




**All rights reserved.**
