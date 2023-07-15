#!/usr/bin/env python3

###___BLAST-CHEWER___###
# a first-ever Python script by marie.pazoutova@gmail.com from the Martin Kolisko lab
# with GREAT help of Petr Sedlacek https://github.com/trohat
# and Serafim Nenarokov https://github.com/Seraff

import argparse
from pathlib import Path
import csv

def parse_arguments():
    usage = "./blast_chewer.py"
    description = ' \n \n \n"I will chew on your blast results to prepare a list of accessions for building phylogenetic tree."' + "\n\nThis script works with one txt input file that contains a table of blast hits for a given group of orthologous genes.\n "
    parser = argparse.ArgumentParser(usage, description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input", required=True, help="Path to input file with blast results; txt file with space delimited table expected")
    parser.add_argument("-e", "--evalue", help="E-value treshold for blast hits; default = 1e-1", default="1e-1")
    # TODO: decide whether you want to apply the following argument ---> add what is needed in the code
    # parser.add_argument("-n", "--nr_hits", help="Number of blast hits taken for a single ortholog; default = None", default=None) 
    parser.add_argument("-o", "--output_path", help="Path to output file")
    parser.add_argument("-t", "--test", action="store_true", help="Just for test data")
    return parser.parse_args()

def read_file(input_path, test=False):
    table = []
    with open(input_path, "r", encoding="utf-8") as infile:
        # after opening the file, we want to read it as a csv table, thus we introduce a new "input file" variable for that
        csv_file = csv.reader(infile, delimiter="\t")
        for row in csv_file:
            table.append(row)
    return table

# we only need some columns from the file, namely 1, 2, 3, 12, 13 (qseqid, sseqid, stitle, evalue, bitscore)
# plus we want to a) turn num values into float and b) extract only one hieararchical level from taxonomy (see parameter level=4)
def parse_data(table, level=3, test=False):
    working_table = []
    for row in table:
        query_ID = row[0]
        accession_nr = row[1]
        taxonomy = row[2]
        taxonomy = taxonomy[taxonomy.find(" ")+1:].split("__")
        try:
            taxonomy = taxonomy[level-1]
        except:
            taxonomy = taxonomy[0]
        evalue = float(row[-2])
        bitscore = float(row[-1])
        working_table.append((query_ID, accession_nr, taxonomy, evalue, bitscore)) # adding items into list in a form of tuple
    return working_table

def filter_out_low_evalues(data, evalue_treshold, test=False):
    # TODO: try rewriting with list comprehension
    filtered = []
    evalue_treshold = float(evalue_treshold)
    if test:
        evalue_treshold = .8   
    for row in data:
        if row[3] > evalue_treshold:
            filtered.append(row)
    print(f"Erased {len(data)-len(filtered)} records with too low e-value")        
    return filtered    

##### DAL 
def rank_accession(data, evalue):

    result = set()

    # create table 1
    query_table = {}
    for row in data:
        query_ID = row[0]
        row = row[1:]
        if query_ID in query_table:
            record_number = len(query_table[query_ID]) + 1
            query_table[query_ID].append(row + (record_number, ))
        else:
            query_table[query_ID] = [row + (1, )]

    print(query_table)  




    # create table 2
    for query_ID_record in query_table.keys():
        for hit in query_table[query_ID_record]:
            pass

    return result

def print_to_file(file, data):
    pass

if __name__ == "__main__":
    args = parse_arguments()

    # now we will validate the path to input file:
    input_path = Path(args.input)
    # print(type(input_file))   #here we can verify that we created an instance of the class '*Path', where we store the path to our input
    # print(input_file.parts)
    if input_path.is_file():
        print(f"Input file taken from {input_path}")
    else:
        # TODO: change exception to more specific 
        raise Exception (f"Input file {input_path} not valid.")
    
    test=False
    if args.test:
        test=True

    data = read_file(input_path, test=test)

    data = parse_data(data, test=test)

    # TODO: ERASE THIS NOTE here I will probably call the evalue filtering
    data = filter_out_low_evalues(data, args.evalue, test)
    

    # result = rank_accession(data, evalue)

    # print_to_file(args.output_path, result)
      


