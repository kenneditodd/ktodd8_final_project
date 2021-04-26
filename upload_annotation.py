#!/usr/local/bin/python3
import re
import mysql.connector


class NCBI_gene:
    def __init__(self, seqid, source, type, start, end, score, strand, phase, id, dbxref, name, gbkey, gene, gene_biotype, description):
        self.seqid = seqid
        self.source = source
        self.type = type
        self.start = start
        self.end = end
        self.score = score
        self.strand = strand
        self.phase = phase
        self.id = id
        self.dbxref = dbxref
        self.name = name
        self.gbkey = gbkey
        self.gene = gene
        self.gene_biotype = gene_biotype
        self.description = description


class Ensembl_gene:
    def __init__(self, seqid, source, type, start, end, score, strand, phase, id, biotype, gene_id, description, name):
        self.seqid = seqid
        self.source = source
        self.type = type
        self.start = start
        self.end = end
        self.score = score
        self.strand = strand
        self.phase = phase
        self.id = id
        self.biotype = biotype
        self.gene_id = gene_id
        self.name = name
        self.description = description


# get paths to Ensembl and NCBI gene annotation files
Ensembl_path = "Sus_scrofa.Sscrofa11.1.103.gff3"
NCBI_path = "GCF_000003025.6_Sscrofa11.1_genomic.gff"

#######################################
# extract genes from annotation files #
#######################################

Ensembl_gff = open(Ensembl_path, 'r')
Ensembl_genes = list()
for line in Ensembl_gff.readlines():
    if line.__contains__('\tgene\t'):
        Ensembl_genes.append(line)
Ensembl_gff.close()
# print(len(Ensembl_genes)) # CHECK: HOW MANY GENES FROM ENSEMBL

NCBI_gff = open(NCBI_path, 'r')
NCBI_genes = list()
for line in NCBI_gff.readlines():
    if line.__contains__('\tgene\t'):
        NCBI_genes.append(line)
NCBI_gff.close()
# print(len(NCBI_genes)) # CHECK: HOW MANY GENES FROM NCBI

###########################################
# separate the NCBI gene list into fields #
###########################################

# seqid/source/type/start/end/score/strand/phase/attributes
NCBI_gene_info = []
for item in NCBI_genes:
    split = item.split('\t')

    # get all 9 columns
    seqid = split[0]
    source = split[1]
    type = split[2] # gene
    start = split[3]
    end = split[4]
    score = split[5]
    strand = split[6]
    phase = split[7]
    attributes = split[8]

    # further separate the attributes column
    id = re.findall(r'ID=(gene-.*?);', attributes)[0]
    dbxref = re.findall(r'Dbxref=(.*?);', attributes)[0]
    name = re.findall(r'Name=(.*?);', attributes)[0]
    gbkey = re.findall(r'gbkey=(.*?);', attributes)[0]
    gene = re.findall(r'gene=(.*?);', attributes)[0]
    gene_biotype = re.findall(r'gene_biotype=(.*)', attributes)[0]
    description = re.findall(r'description=(.*?);', attributes)
    if len(description) == 0:
        description = "NA"
    else:
        description = description[0]

    # store data in object
    NCBI_gene_info.append(NCBI_gene(seqid, source, type, start, end, score, strand, phase, id, dbxref, name, gbkey, gene,
                                    gene_biotype, description))

#################################################
### Separate the Ensembl gene list into fields ##
#################################################

# seqid/source/type/start/end/score/strand/phase/attributes
Ensembl_gene_info = []
for item in Ensembl_genes:
    split = item.split('\t')

    # get all 9 columns
    seqid = split[0]
    source = split[1]
    type = split[2]  # gene
    start = split[3]
    end = split[4]
    score = split[5]
    strand = split[6]
    phase = split[7]
    attributes = split[8]

    # further separate the attributes column
    id = re.findall(r'ID=(gene:.*?);', attributes)[0]
    biotype = re.findall(r'biotype=(.*?);', attributes)[0]
    gene_id = re.findall(r'gene_id=(.*?);', attributes)[0]
    description = re.findall(r'description=(.*?);', attributes)
    if len(description) == 0:
        description = "NA"
    else:
        description = description[0]
    name = re.findall(r'Name=(.*?);', attributes)
    if len(name) == 0:
        name = "NA"
    else:
        name = name[0]

    # store data in object
    Ensembl_gene_info.append(Ensembl_gene(seqid, source, type, start, end, score, strand, phase, id, biotype, gene_id,
                                          description, name))

###########################################################
## Connect to mysql database and upload annotation files ##
###########################################################

# connect to database
conn = mysql.connector.connect(user='ktodd8', password='Wildcats19!', host='localhost', database='ktodd8')
curs = conn.cursor()

# Create Ensembl table
create_Ensembl = '''
                    create table Ensembl_Sscrofa(
                       seqid INT NOT NULL,
                       source VARCHAR(100) NOT NULL,
                       type VARCHAR(40) NOT NULL,
                       start INT,
                       end INT,
                       score VARCHAR(10),
                       strand VARCHAR(10),
                       phase VARCHAR(10),
                       id VARCHAR(100),
                       biotype VARCHAR(100),
                       gene_id VARCHAR(100),
                       description VARCHAR(300),
                       name VARCHAR(100)
                    );
                '''
curs.execute(create_Ensembl)

# Populate Ensembl table
for item in Ensembl_gene_info:
    insert_Ensembl = '''
    INSERT INTO Ensembl_Sscrofa (seqid, source, type, start, end, score, strand, phase, id, biotype, gene_id, description, name)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    curs.execute(insert_Ensembl, (item.seqid, item.source, item.type, item.start, item.end, item.score, item.strand, item.phase,
                                   item.id, item.biotype, item.gene_id, item.description, item.name,))

# Create NCBI table
create_NCBI = '''
                    create table NCBI_Sscrofa(
                       seqid INT NOT NULL,
                       source VARCHAR(100) NOT NULL,
                       type VARCHAR(40) NOT NULL,
                       start INT,
                       end INT,
                       score VARCHAR(10),
                       strand VARCHAR(10),
                       phase VARCHAR(10),
                       id VARCHAR(100),
                       dbxref VARCHAR(100),
                       name VARCHAR(100),
                       gbkey VARCHAR(100),
                       gene VARCHAR(100),
                       gene_biotype VARCHAR(100),
                       description VARCHAR(300)
                    );
                '''
curs.execute(create_NCBI)

# Populate NCBI table
for item in NCBI_gene_info:
    insert_NCBI = '''
    INSERT INTO NCBI_Sscrofa (seqid, source, type, start, end, score, strand, phase, id, dbxref, name, gbkey, gene, gene_biotype, description)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    curs.execute(insert_NCBI, (item.seqid, item.source, item.type, item.start, item.end, item.score, item.strand, item.phase,
                                   item.id, item.dbxref, item.name, item.gbkey, item.gene, item.gene_biotype, item.description,))

conn.commit()
curs.close()
