
# a version of blast_chewer.py that was completely suggested by the chatGPT according to a following query:

# We have input file of blast results looking basically like tab separated table. Now we want to do the following: 
# Read the data row by row and store them in the most handy format to be approached for whatever we need later
# Group data according to qseqid and sseqid; if there are cases of more than one pair of identical qseqid - sseqid pairs, keep the one with lowest e-value
# Polish the column with taxonomy from the NCBI, so that it only stores readable taxonomical hierarchy, without the accession number that is repeated at the beginning of this section
# Transform the original table into dictionary of dictionaries that looks like this: {sseqid: {qseqid: value, bitscore: value, taxonomy: value of the 3rd level of the hierarchy}
# For each accession compute its mean bitscore and how many qseqids it is linked to
# Sort accessions according to 1. number of qseqids it is hitting; 2. mean bitscore and save it in an appropriate type of variable

# Could you please write me a most elegant, swift and smooth python script to do this? 

###

import pandas as pd

# Read the Blast results file into a pandas DataFrame
blast_results = pd.read_csv('blast_results.txt', sep='\t', header=None,
                            names=['qseqid', 'sseqid', 'bitscore', 'evalue', 'taxonomy'])

# Group data by qseqid and sseqid, keeping the lowest e-value
grouped_data = blast_results.sort_values('evalue').groupby(['qseqid', 'sseqid']).first().reset_index()

# Remove accession numbers from the taxonomy column
grouped_data['taxonomy'] = grouped_data['taxonomy'].str.split('; ').str[-1]

# Create a nested dictionary from the grouped data
result_dict = {}
for _, row in grouped_data.iterrows():
    sseqid = row['sseqid']
    qseqid = row['qseqid']
    bitscore = row['bitscore']
    taxonomy = row['taxonomy']
    
    if sseqid not in result_dict:
        result_dict[sseqid] = {}
    
    result_dict[sseqid][qseqid] = {'bitscore': bitscore, 'taxonomy': taxonomy}

# Calculate mean bitscore and count of qseqids for each sseqid
for sseqid in result_dict:
    bitscores = [result_dict[sseqid][qseqid]['bitscore'] for qseqid in result_dict[sseqid]]
    mean_bitscore = sum(bitscores) / len(bitscores)
    qseqid_count = len(result_dict[sseqid])
    
    result_dict[sseqid]['mean_bitscore'] = mean_bitscore
    result_dict[sseqid]['qseqid_count'] = qseqid_count

# Sort accessions based on qseqid count and mean bitscore
sorted_accessions = sorted(result_dict.keys(), key=lambda x: (result_dict[x]['qseqid_count'], result_dict[x]['mean_bitscore']), reverse=True)

# Print the sorted accessions
for sseqid in sorted_accessions:
    print(f"Sseqid: {sseqid}")
    print(f"Mean Bitscore: {result_dict[sseqid]['mean_bitscore']}")
    print(f"Number of qseqids: {result_dict[sseqid]['qseqid_count']}")
    print("")

# If you need to use the result_dict for further analysis, you can directly access the nested data.
# For example: result_dict['sseqid']['qseqid']['bitscore'] or result_dict['sseqid']['mean_bitscore']
