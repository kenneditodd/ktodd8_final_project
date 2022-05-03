# JHU_Final_Project
The goal of this project is to compare two annotation files.  The Swine Genome Sequencing Consortium (SGSC) has released *Sus scrofa* assembly 11.1.  The Ensembl and NCBI gene annotation files of this assembly will be compared.  The pig genome is not well annotated and there are many genes that do not have any names.  This will highlight the importance of gene annotation selection which will have a great impact on downstream applications such as differential gene expression.

## Details
Download the NCBI and Ensembl gene annotation files.  The **upload_annotation.py** script will read in both annotation files, parse them and create two new gene tables, Ensembl_Sscrofa and NCBI_Sscrofa, in the ktodd8 MySQL database.  Make sure to only run this script once!  The **form.html** will gather input, filtering, and output options from a user.  The form contents will be sent to the **compare_annotations.cgi** script.  This script will connect to the MySQL database, query the two gene annotation files and report summaries and statistics.  The results are sent the **results.html** template to be displayed.  The **format.css** file will aid in formatting for the results.

1. Download *Sus scrofa* gene annotation files from Ensembl and NCBI using the wget command.
```
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/003/025/GCF_000003025.6_Sscrofa11.1/GCF_000003025.6_Sscrofa11.1_genomic.gff.gz
wget http://ftp.ensembl.org/pub/release-103/gff3/sus_scrofa/Sus_scrofa.Sscrofa11.1.103.gff3.gz
gunzip *.gz
```
2. Download the following scripts/templates:
      - upload_annotation.py
      - form.html
      - compare_annotations.cgi
      - results.html
      - format.css
3. Run the script upload_annotation.py to upload the two gene annotation files to the MySQL database.  Make sure the script and annotation files are in the same directory.  Only run this once.
```
./upload_annotation.py
```
4. Use the link below to compare the two gene annotation files.
      - http://bfx3.aap.jhu.edu/ktodd8/final/form.html
