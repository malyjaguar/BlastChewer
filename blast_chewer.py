#!/usr/bin/env python3

###___BLAST-CHEWER___###
# a first-ever Python script by marie.pazoutova@gmail.com from the Martin Kolisko lab https://github.com/kolecko007
# with GREAT help of Petr Sedlacek https://github.com/trohat
# and Serafim Nenarokov https://github.com/Seraff

import argparse
from pathlib import Path
import pandas as pd


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
                   
    def clean_taxonomy(self):
        self.data['taxonomy'] = self.data['taxonomy'].split(' ', 1)[1] 

"""
def refine_taxonomy(blast_hits):  
    for hit in blast_hits:
        taxonomy = hit.data['taxonomy']
        taxonomy_3rd_level = taxonomy.split('__')[2] 
"""        

if __name__ == "__main__":
    args = parse_arguments()
    validate_input_path(args.input)

    raw_lists = parse_blast_data(args.input)
    blast_hits = [BlastHit(list) for list in raw_lists]
    
 

    # import ipdb; ipdb.set_trace()
    
