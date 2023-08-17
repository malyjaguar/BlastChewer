#!/usr/bin/env python3

###___BLAST-CHEWER___###
# a first-ever Python script by marie.pazoutova@gmail.com from the Martin Kolisko lab https://github.com/kolecko007
# with GREAT help of Petr Sedlacek https://github.com/trohat
# and Serafim Nenarokov https://github.com/Seraff

import argparse
from pathlib import Path
import pandas as pd
from pprint import pprint

def parse_arguments():
    usage = "./blast_chewer.py"
    description = ' \n \n \n"I will chew on your blast results to prepare a list of accessions for building phylogenetic tree."' + "\n\nThis script works with one txt input file that contains a table of blast hits for a given group of orthologous genes.\n "
    parser = argparse.ArgumentParser(usage, description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input", required=True, help="Path to input file with blast results; txt file with tab delimited table expected")
    parser.add_argument("-e", "--evalue", help="E-value treshold for blast hits; default = 1e-1", default="1e-1")
    # TODO: decide whether you want to apply the following argument ---> add what is needed in the code
    # parser.add_argument("-n", "--nr_hits", help="Number of blast hits taken for a single ortholog; default = None", default=None) 
    parser.add_argument("-o", "--output_path", help="Path to output file")
    return parser.parse_args()


def validate_input_path(path_to_file):
    if Path(path_to_file).is_file():
        print(f"Input file taken from {path_to_file}")
    else:
        # TODO: change exception to more specific 
        raise Exception (f"Input file {path_to_file} not valid.")


def parse_blast_data(path_to_file):
    names = ['qseqid', 'sseqid', 'taxonomy', 'pident', 'length', 'matches', 'gaps', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']
    data = pd.read_csv(path_to_file, sep = "\t", names = names) 
    # Here we could remove accession numbers from the taxonomy column like this:
    # data['taxonomy'] = data['taxonomy'].str.split(' ', n=1).str[1] 
    # But Serafim suggests to do this within the class BlastHit, as it is ___it's___ responsability (-> cleaner code)
    grouped_data = data.sort_values('evalue').groupby(['qseqid', 'sseqid']).first().reset_index() # beware, this line shuffled the overall order of data
    # alternatively, if one doesn't wish to shuffle the lines, use the following code:
    """
    idx = data.groupby(['qseqid', 'sseqid'])['evalue'].transform(min) == data['evalue']
    grouped_data = data[idx]
    """
    raw_lists = grouped_data.values.tolist()
    return raw_lists


class BlastHit():
    blast_fields = ('qseqid', 'sseqid', 'taxonomy', 'pident', 'length', 'matches', 'gaps', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore')
    float_fields = ('pident', 'evalue')
    int_fields = ('length', 'matches', 'gaps', 'qstart', 'qend', 'sstart', 'send', 'bitscore')

    def __init__(self, raw_list):
        self.data = dict([[e, raw_list[i]] for i, e in enumerate(BlastHit.blast_fields)])

        for key, value in self.data.items():
            if key in BlastHit.float_fields:
                self.data[key] = float(value)
            elif key in BlastHit.int_fields:
                self.data[key] = int(value)

        self.clean_taxonomy()        
        # print(blast_hits[:10].data['taxonomy'])

    def __repr__(self):
        return f"BlastHit(qseqid={self.data['qseqid'][:30]}... sseqid={self.data['sseqid']})"

    def accession(self):
        return self.data['sseqid']
    
    def taxonomy(self):
        return self.data['taxonomy']
                   
    def clean_taxonomy(self):
        self.data['taxonomy'] = self.data['taxonomy'].split(' ', 1)[1] 

"""
def refine_taxonomy(blast_hits):  
    for hit in blast_hits:
        taxonomy = hit.data['taxonomy']
        taxonomy_3rd_level = taxonomy.split('__')[2] 
"""        

"""
def parse_data_to_dict(blast_hits):
    dict_of_accessions = {}
    for hit in blast_hits:
        accession = hit.data['sseqid']
       # now I somehow need to create this:   dict_of_accessions[accession].append(hit.data['qseqid'], hit.data['bitscore'], hit.data['taxonomy'])
    return dict_of_accessions
"""         

def pull_accessions_taxonwise(inputfile, sorted_list, max_tax_per_group=3):
    acc_selection = []
    n = 0

    with open(inputfile) as f:
        for line in f:
            line = line.strip()

            for tax_dict in sorted_list:
                if n < max_tax_per_group:
                    if line.lower() in tax_dict["taxonomy"].lower():
                        acc_selection.append(tax_dict)
                        n += 1

    return acc_selection


if __name__ == "__main__":
    args = parse_arguments()
    validate_input_path(args.input)

    raw_lists = parse_blast_data(args.input)
    blast_hits = [BlastHit(list) for list in raw_lists]

    hits_by_acc = {}

    for hit in blast_hits:
        acc = hit.data['sseqid']

        if acc not in hits_by_acc:
            hits_by_acc[acc] = []
        
        hits_by_acc[acc].append(hit)

    # result is { 'acc_number_1': [<hit_1>, <hit_2>], 'acc_number_2': [<hit_3>, ...], ... }

    hit_list = list(hits_by_acc.values())

    def condition(element):
        length = len(element)
        mean_bitscore = sum([e.data['bitscore'] for e in element])/length
        return (length, mean_bitscore)
    
    hit_list.sort(key=condition, reverse=True)

    taxonomy = [{"accession": e[0].accession(), "taxonomy": e[0].taxonomy()} for e in hit_list]
    filtered = pull_accessions_taxonwise("taxon_list_test.txt", taxonomy)
    pprint(filtered)

    with open('test_output.txt', "w") as out_f:
        for tax_dict in filtered:
            out_f.write(f"{tax_dict['accession']}\n") 
    
     # result is [[<hit_1>, <hit_2>], [<hit_3>, ...], ...
     # 
     # Sort it by some parameters

    # dict_of_accessions = parse_data_to_dict(blast_hits)
    # here we created a list of objects of class BlastHit
    # each having an atribute 'data' where one row of blast hits is stored as dictionary
 

    
    # import ipdb; ipdb.set_trace()
