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
    with open(input_path, "r", encoding="utf-8") as infile:
        # after opening the file, we want to read it as a csv table, thus we introduce a new "input file" variable for that
        csv_file = csv.reader(infile, delimiter= "\t")
        i = 1
        for row in csv_file:
            i += 1
            if i > 3:
                break 
            print(row)


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
    
    working_table = read_file(input_path)

