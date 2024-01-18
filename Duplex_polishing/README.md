## Step 1. Finding the potential modification sites

```shell
hammerhead --ref <assembly> --read <R10.4.1_reads>
```
After running the Hammerhead pipeline with your ` R10.4.1 `reads, you will receive a file named `potential_modification_site_detail.bed`. This file includes the positions of the potential modification sites that have been identified in your assembly.



## Step 2. Polishing sites using duplex reads

```shell
python duplex_polishing.py --read <duplex_reads> --bed <position_sites> --ref <assembly>
```

After executing this script, you will obtain a file named `corrected_site.bed`. This file contains information about the sites that require replacement.

```shell
#the details of corrected_site.bed
#chr	pos	base	N_A	N_T	N_G	N_C	P_A	P_T	P_G	P_C	polish_base
contig_4	29153	T	0	1	0	13	0.0	0.07142857142857142	0.0	0.9285714285714286	C
contig_6	155419	A	1	0	20	0	0.047619047619047616	0.0	0.9523809523809523	0.0	G
contig_7	60990	A	4	0	24	0	0.14285714285714285	0.0	0.8571428571428571	0.0	G	*
contig_7	118348	G	25	0	7	0	0.78125	0.0	0.21875	0.0	A
contig_7	123180	C	0	19	0	2	0.0	0.9047619047619048	0.0	0.09523809523809523	T
contig_7	344011	C	0	19	0	4	0.0	0.8260869565217391	0.0	0.17391304347826086	T
```

`chr`, `pos`, `base`  are the base type and position in the reference of potential modification sites.

`N_A`, `N_T`, `N_G`, `N_C` are the number of reads which were mapped as A, T, G, and C base at potential modification sites.

`P_A`, `P_T`, `P_G`, `P_C` are the proportion of reads which were mapped as A, T, G, and C base at potential modification sites.

`polish_base`  is the base after polished. 

**Note**: The sites that are identified in the results are selected based on the proportion of errors. If you believe that any of the sites are correct, please manually remove them. The presence of an **asterisk (*)** indicates this is an ambiguous site that is challenging to determine as an error.



## Step 3. Replacing  erroneous bases in the assembly with correct counterparts

```shell
cat corrected_site.bed | grep -v pos | awk '{if ($12 == "C") print $0}' | awk '{print $1 "\t" $2-1 "\t" $2}' > C.bed
cat corrected_site.bed | grep -v pos | awk '{if ($12 == "G") print $0}' | awk '{print $1 "\t" $2-1 "\t" $2}' > G.bed
cat corrected_site.bed | grep -v pos | awk '{if ($12 == "T") print $0}' | awk '{print $1 "\t" $2-1 "\t" $2}' > T.bed
cat corrected_site.bed | grep -v pos | awk '{if ($12 == "A") print $0}' | awk '{print $1 "\t" $2-1 "\t" $2}' > A.bed

bedtools maskfasta -fi <assembly> -bed A.bed -mc A -fo tmp1.fasta
bedtools maskfasta -fi tmp1.fasta -bed T.bed -mc T -fo tmp2.fasta
bedtools maskfasta -fi tmp2.fasta -bed G.bed -mc G -fo tmp3.fasta
bedtools maskfasta -fi tmp3.fasta -bed C.bed -mc C -fo final.fasta

# remove the temporaryte files
rm tmp1.fasta tmp2.fasta tmp3.fasta A.bed T.bed G.bed C.bed
```

The `final.fasta`  is the final polished genome assembler.



## Tool showcase

To demonstrate the effectiveness of the polishing strategy in correcting substitution error types (`G2A` and `C2T`) caused by DNA modifications in assemblies, we present the substitution rates of 15 assemblies. These assemblies were generated using 40-， 50-, and 60-fold random subsampling *Acinetobacter pittii* R10.4.1 reads. We compared the results obtained from different polishing approaches with the reference chromosome.

- Assembly with No Polishing
- Assembly with Potential Modification Sites Polished with approximate 10-fold Duplex Reads
- Assembly with 50-fold Next-Generation Sequencing (NGS) Reads



![alt text](../figure_demo/Demo_4.png)

