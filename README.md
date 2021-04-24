# JHU_Final_Project
The goal of this project is to compare two annotation files.  The Swine Genome Sequencing Consortium (SGSC) has released *Sus scrofa* assembly 11.1.  The Ensembl gene annotation and NCBI gene annotation of this assembly will be compared.  The pig genome is not well annotated.  So, there are many genes that do not have any names.  The gene annotation selection will have a great impact on downstream applications such as differential gene expression.

1. Download *Sus scrofa* gene annotation files from Ensembl and NCBI.
```
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/003/025/GCF_000003025.6_Sscrofa11.1/GCF_000003025.6_Sscrofa11.1_genomic.gff.gz
wget http://ftp.ensembl.org/pub/release-103/gff3/sus_scrofa/Sus_scrofa.Sscrofa11.1.103.gff3.gz
gunzip *.gz
```
