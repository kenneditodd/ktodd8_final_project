#!/usr/local/bin/python3
import cgi, json
import os
import sys
import jinja2
import mysql.connector
from pandas import DataFrame


# This line tells the template loader where to search for template files
templateLoader = jinja2.FileSystemLoader( searchpath="." )

# This creates your environment and loads a specific template
env = jinja2.Environment(loader=templateLoader)
template = env.get_template('results.html')


########################
# GET VALUES FROM FORM #
########################

# initialize
input_genes = "off"
input_name = "off"
input_no_name = "off"
filter_protein = "off"
output_summary = "off"
output_unique = "off"
output_common = "off"

#print("Content-Type: application/json\n\n")
form = cgi.FieldStorage()

input = form.getvalue('group1')
filter_protein = form.getvalue('protein')
output_summary = form.getvalue('summarybox')
output_common = form.getvalue('commonGenes')
output_unique = form.getvalue('uniqueGenes')


#print(filter_protein)
# manually set values
if input == "allGenes": 
	input_genes = "on"
elif input == "allWithName":
	input_name = "on"
elif input == "noName":
	input_no_name = "on"

if filter_protein == "protein": 
	filter_protein = "on"
if output_summary: 
	output_summary = "on"
if output_common: 
	output_common = "on"
if output_unique: 
	output_unique = "on"

################################################
# INITIALIZE VARIABLES TO SEND TO RESULTS.HTML #
################################################

parameters = ""
E_summary = ""
N_summary = ""
com = ""
stats = []
E_uni = ""
N_uni = ""
Nc_unique = []
En_unique = []

############################
# OUTPUT USER'S PARAMETERS #
############################

# simultaneously create WHERE clause for each annotation file
E_whereVar = None
N_whereVar = None

# output user input
if input_genes == "on":
	parameters = "INPUT: ALL GENES\n"
elif input_no_name == "on":
	parameters = "INPUT: NO NAME GENES\n"
	E_whereVar = " WHERE name LIKE 'NA'"
	N_whereVar = " WHERE name LIKE 'LOC%'"
elif input_name == "on":
	parameters = "INPUT: NAMED GENES\n"
	E_whereVar = " WHERE name NOT LIKE 'NA'"
	N_whereVar = " WHERE name NOT LIKE 'LOC%'"
#print(parameters)
#print(E_whereVar)
#print(N_whereVar)

# output user filters
if filter_protein == "on":
	parameters += "FILTER: PROTEIN CODING\n"
	if (E_whereVar != None):
		E_whereVar += " AND biotype like 'protein_coding'"
	else:
		E_whereVar = " WHERE biotype like 'protein_coding'"
	if (N_whereVar != None):
		N_whereVar += " AND gene_biotype like 'protein_coding'"
	else:
		N_whereVar = " WHERE gene_biotype like 'protein_coding'"
else:
	parameters += "FILTER:\n"

# no WHERE clause when whereVar is empty
if (E_whereVar == None):
	E_whereVar = ""
if (N_whereVar == None):
	N_whereVar = ""

# output user output
output = list()
if output_summary == "on":
	output.append("SUMMARY")
if output_common == "on":
	output.append("COMMON GENES")
if output_unique == "on":
	output.append("UNIQUE GENES")
string = str("OUTPUT: " + ', '.join(output))
parameters += string  # SEND TO RESULTS.HTML
#print(parameters)
#print(E_whereVar)
#print(N_whereVar)


###############
# GET SUMMARY #
###############

# connect to mysql database
conn = mysql.connector.connect(user='ktodd8', password='Wildcats19!', host='localhost', database='ktodd8')
curs = conn.cursor()

# only output summary if specified
if output_summary == "on":

	# ENSEMBL ANNOTATION FILE
	# get total # of features
	E_total_genes = "SELECT COUNT(*) FROM Ensembl_Sscrofa "
	E_total_genes += E_whereVar
	curs.execute(E_total_genes,)
	E_total_genes = curs.fetchall()
	E_numFeatures = E_total_genes[0][0]
	E_summary = "FEATURES:\n" + str(E_numFeatures) + "\n"

	#get biotype breakdown
	E_biotype = "SELECT biotype FROM Ensembl_Sscrofa "
	E_biotype += E_whereVar
	curs.execute(E_biotype,)
	E_biotype = curs.fetchall()
	E_biotype = [item[0] for item in E_biotype]
	df = DataFrame(E_biotype, columns=['biotype'])
	E_breakdown = df.biotype.value_counts()
	E_breakdown = E_breakdown.to_string()
	E_summary += "\nBIOTYPE FREQUENCY:\n" + E_breakdown  # SEND TO RESULTS.HTML
	#print(E_summary)


	# NCBI ANNOTATION FILE
	# get total # of features
	N_total_genes = "SELECT COUNT(*) FROM NCBI_Sscrofa "
	N_total_genes += N_whereVar
	curs.execute(N_total_genes,)
	N_total_genes = curs.fetchall()
	N_numFeatures = N_total_genes[0][0]
	N_summary = "FEATURES:\n" + str(N_numFeatures) + "\n"

	#get biotype breakdown
	N_biotype = "SELECT gene_biotype FROM NCBI_Sscrofa "
	N_biotype += N_whereVar
	curs.execute(N_biotype,)
	N_biotype = curs.fetchall()
	N_biotype = [item[0] for item in N_biotype]
	df = DataFrame(N_biotype, columns=['biotype'])
	N_breakdown = df.biotype.value_counts()
	N_breakdown = N_breakdown.to_string()
	N_summary += "\nBIOTYPE FREQUENCY:\n" + N_breakdown  # SEND TO RESULTS.HTML
	#print("\n" + N_summary)


#####################
# FIND COMMON GENES #
#####################

# only output common genes if specified
if output_common == input_no_name == "on":
	sys.exit("\nGenes shared between the two annotation files are compared by the gene names. For this reason, no name genes cannot be taken as input for common gene analysis.")
if output_common == input_genes == "on":
	com = "Genes shared between the two annotation files are compared by the gene names.\n"
	com += "Only genes with names will be considered despite selecting 'all genes' (only for common gene analysis.\n"
if output_common == "on":

	# ENSEMBL
	# get all gene names
	E_stats = "SELECT name FROM Ensembl_Sscrofa "
	E_stats += E_whereVar
	curs.execute(E_stats,)
	E_stats = curs.fetchall()
	E_stats = [item[0] for item in E_stats]
	E_stats = sorted(E_stats, key=str.lower)
	#print(E_stats)

	# NCBI
	# get all gene names
	N_stats = "SELECT name FROM NCBI_Sscrofa "
	N_stats += N_whereVar
	curs.execute(N_stats,)
	N_stats = curs.fetchall()
	N_stats = [item[0] for item in N_stats]
	N_stats = sorted(N_stats, key=str.lower)
	#print(N_stats)

	# compare lists for common gene names
	# remove duplicate names and sort
	def intersection(lst1, lst2):
		return list(set(lst1) & set(lst2))

	common_genes = intersection(E_stats, N_stats)
	common_nodups = list(set(common_genes))
	stats = sorted(common_nodups, key=str.lower)
	com = "Note:  Ensembl no name genes are called 'NA'.  NCBI no name genes start with 'LOC'.\n\n"
	com += "Total genes in common: " + str(len(common_nodups)) + "\n"
	com += "Common gene list:\n"
	#print(com)
	#print(stats)
	# com and stat can be sent to html file


#####################
# FIND UNIQUE GENES #
#####################

# only output unique genes if specified
if output_unique == input_no_name == "on":
	sys.exit("\nGenes shared between the two annotation files are compared by the gene names. For this reason, no name genes cannot be taken as input for unique gene analysis.")
if output_unique == input_genes == "on":
	E_uni = "Genes shared between the two annotation files are compared by the gene names.\n"
	E_uni += "Only genes with names will be considered despite selecting 'all genes' (only for unique analysis).\n"

if output_unique == "on":
	# ENSEMBL
	# get all gene names
	En_stats = "SELECT name FROM Ensembl_Sscrofa "
	En_stats += E_whereVar
	curs.execute(En_stats,)
	En_stats = curs.fetchall()
	En_stats = [item[0] for item in En_stats]
	En_stats = sorted(En_stats, key=str.lower)
	#print(En_stats)

	# NCBI
	# get all gene names
	Nc_stats = "SELECT name FROM NCBI_Sscrofa "
	Nc_stats += N_whereVar
	curs.execute(Nc_stats,)
	Nc_stats = curs.fetchall()
	Nc_stats = [item[0] for item in Nc_stats]
	Nc_stats = sorted(Nc_stats, key=str.lower)
	#print(Nc_stats)

	# get unique gene lists by comparing lists to each other
	Nc_unique = []
	for x in Nc_stats:
		if x not in En_stats:
			Nc_unique.append(x)
		
	En_unique = []
	for x in En_stats:
		if x not in Nc_stats:
			En_unique.append(x)
		
	#print(Nc_unqiue)
	#print(En_unique)

	# create Ensembl header
	E_uni = "Note:  Ensembl no name genes are called 'NA'.\n\n"
	E_uni += "Total unique genes:\n"
	E_uni += "\tThere are " + str(len(En_unique)) + " Ensembl genes.\n"
	E_uni += "Unique gene list:\n"
	#print(E_uni)

	# create NCBI header
	N_uni = "Note:  NCBI no name genes start with 'LOC'.\n\n"
	N_uni += "Total unique genes:\n"
	N_uni += "\tThere are " + str(len(Nc_unique)) + " NCBI genes.\n"
	N_uni += "Unique gene list:\n"
	#print(N_uni)

# close database
curs.close()
conn.close()


########################
# SEND RESULTS TO HTML #
########################

print("Content-Type: text/html\n\n")
print(template.render(parameters=parameters, com=com, stats=stats, E_summary=E_summary, N_summary=N_summary, E_uni=E_uni, N_uni=N_uni,En_unique=En_unique,Nc_unique=Nc_unique))


