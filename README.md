# JHU_Final_Project
The goal of this project is to compare two annotation files.  The Swine Genome Sequencing Consortium (SGSC) has released *Sus scrofa* assembly 11.1.  The Ensembl and NCBI gene annotation files of this assembly will be compared.  The pig genome is not well annotated and there are many genes that do not have any names.  This will highlight the importance of gene annotation selection which will have a great impact on downstream applications such as differential gene expression.

## Details
The NCBI and Ensembl gene annotation files are downloaded.  The upload_annotation.py will read in both annotation files, parse them and create new tables in the ktodd8 MySQL database.  A user will then be given a link to an html form to fill out and specify the desired information when comparing the two gene annotation files.  The form contents will be sent to the XXX.cgi script.  The script will connect to the MySQL database and query the two gene annotation files.  The results will be displayed in the XXX.html template.

1. Download *Sus scrofa* gene annotation files from Ensembl and NCBI.
```
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/003/025/GCF_000003025.6_Sscrofa11.1/GCF_000003025.6_Sscrofa11.1_genomic.gff.gz
wget http://ftp.ensembl.org/pub/release-103/gff3/sus_scrofa/Sus_scrofa.Sscrofa11.1.103.gff3.gz
gunzip *.gz
```
2. Download all files in the scripts folder.
3. Run the script upload_annotation.py to upload the two gene annotation files to the MySQL database.  Make sure the script and annotation files are in the same directory.
```
./upload_annotation.py
```
