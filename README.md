# JHU_Final_Project
The goal of this project is to compare two annotation files.  The Swine Genome Sequencing Consortium (SGSC) has released *Sus scrofa* assembly 11.1.  The Ensembl and NCBI gene annotation files of this assembly will be compared.  The pig genome is not well annotated and there are many genes that do not have any names.  This will highlight the importance of gene annotation selection which will have a great impact on downstream applications such as differential gene expression.

## Details
Download the NCBI and Ensembl gene annotation files.  The **upload_annotation.py** script will read in both annotation files, parse them and create new tables in the ktodd8 MySQL database.  Make sure to only run this script once!  The **user_input.html** form will prompt a user to specify the desired information when comparing the two gene annotation files.  The form contents will be sent to the **XXX.cgi** script.  This script will connect to the MySQL database, query the two gene annotation files and report statistics.  The results will be displayed using the **results.html** template.

1. Download *Sus scrofa* gene annotation files from Ensembl and NCBI using the wget command.
```
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/003/025/GCF_000003025.6_Sscrofa11.1/GCF_000003025.6_Sscrofa11.1_genomic.gff.gz
wget http://ftp.ensembl.org/pub/release-103/gff3/sus_scrofa/Sus_scrofa.Sscrofa11.1.103.gff3.gz
gunzip *.gz
```
2. Download the following scripts/templates:
      - upload_annotation.py
      - user_input.html
      - XXX.cgi
      - results.html
4. Run the script upload_annotation.py to upload the two gene annotation files to the MySQL database.  Make sure the script and annotation files are in the same directory.
```
./upload_annotation.py
```
