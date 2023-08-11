# Mokarran
This project is designed to find the potential modification sites.



## Dependence

To use this software, you'll need to install additional tools for read processing, including samtools and minimap2. The following commands can help you install both the software package and its dependencies.

```shell
# test verison for dependences
# minimap2	2.17
# samtools	1.17

conda install -c bioconda -c conda-forge minimap2 samtools
```



## General usage
`mokarran` can be run using simple command:

```
python mokarran.py -ref <reference> -read <input_fastq>
```

The help for `hammerhead`:

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

The results file for `mokarran`:

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
  Chr	Pos	MAE	absA	absT	absG	absC	A,T,G,C,a,t,g,c
  contig_2	2541	0.386	0.0	0.386	0.0	0.386	0,2,0,191,0,25,0,38
  contig_2	2836	0.395	0.395	0.0	0.279	0.116	52,0,24,10,129,0,0,0
  contig_2	2837	0.475	0.474	0.029	0.413	0.033	37,1,40,0,0,5,112,4
  ```

​		MAE is the differnece index for each site.

​		the absA/T/G/C is the absolute difference for A/T/G/C base.

​		A,T,G,C,a,t,g,c  is the number of reads mapped as the  A/T/G/C in forward strand and T/A/C/G in reverse starnd.

