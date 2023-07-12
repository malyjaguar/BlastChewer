#!/usr/bin/env python3

import argparse
from pathlib import Path
import csv

def parse_arguments():
    usage = "./blast_chewer.py"
    description = ' \n \n \n"I will chew on your blast results to prepare a list of accessions for building phylogenetic tree."' + "\n\nThis script works with one txt input file that contains a table of blast hits for a given group of orthologous genes.\n "
    parser = argparse.ArgumentParser(usage, description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input", required = True, help = "Path to input file with blast results; txt file with space delimited table expected")
    parser.add_argument("-e", "--evalue", help="E-value treshold for blast hits; default = 1e-1", default = "1e-1")
    parser.add_argument("-n", "--nr_hits", help="Number of blast hits taken for a single ortholog; default = None", default = None)
    parser.add_argument("-o", "--output_path", help="Path to output file")
    return parser.parse_args()

def read_file(input_path):
    table = []
    with open(input_path, "r", encoding="utf-8") as infile:
        # after opening the file, we want to read it as a csv table, thus we introduce a new "input file" variable for that
        csv_file = csv.reader(infile, delimiter= "\t")
        for row in csv_file:
            table.append(row)
        return table

# we only need some columns from the file, namely 1, 2, 3, 12, 13 (qseqid, sseqid, stitle, evalue, bitscore)
# plus we want to a) turn num values into float and b) extract only one hieararchical level from taxonomy (see parameter level=4)
def parse_data(table, level=4):
    result = []
    for row in table:
        qseqid = row[0]
        sseqid = row[1]
        taxonomy = row[2]
        taxonomy = taxonomy[taxonomy.index(" ")+1:].split("__")
        try:
            taxonomy = taxonomy[level-1]
        except:
            taxonomy = taxonomy[0]
        if taxonomy != "Diplomonadida":
            print(taxonomy, end=" ") # TODO: delete this line
        evalue = float(row[-2])
        bitscore = float(row[-1])
        result.append([qseqid, sseqid, taxonomy, evalue, bitscore])
    return result

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
    
    data = read_file(input_path)

    data = parse_data(data)

    # print(data)

