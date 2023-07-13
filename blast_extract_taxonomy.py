#!/usr/bin/env python3

import argparse
from pathlib import Path
import csv

def parse_arguments():
    usage = "./blast_extract_taxonomy.py"
    description = "Extracts fourth level of taxonomy from blast results table, if there is any; otherwise takes whatever is at the beginning"
    parser = argparse.ArgumentParser(usage, description=description)
    parser.add_argument("-i", "--input", required = True, help = "Path to input file with blast results; txt file with space delimited table expected")
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

def parse_data_to_set(table, level=4):  # "programátoři počítají od nuly, ale biologové od jedničky..." takže pokud chci úroveň 4, píšu 4 a níže to ošetřím 
    result = set()
    for row in table:
        taxonomy = row[2]   # here I choose column three from our blast results table (= stitle), saving it in a new string variable 
        after_space = taxonomy.find(" ")+1  # finding the position of " " in the string while avoiding the "of by one error" - returning number 
        taxonomy = taxonomy[after_space:]   # this actually cuts the NCBI accession number from the taxonomy that follows in the 'stitle' column
        taxonomy = taxonomy.split("__")
        try:
            taxonomy = taxonomy[level-1]
        except:
            taxonomy = taxonomy[0]  # sometimes, not a full taxonomical hierarchy is given for some weird accession, this helps us to deal with it
        result.add(taxonomy)
    return result

if __name__ == "__main__":
    args = parse_arguments()

    # now we will validate the path to input file:
    input_path = Path(args.input)
    if input_path.is_file():
        print(f"Input file taken from {input_path}")
    else:
        raise Exception (f"Input file {input_path} not valid.")
    
    data = read_file(input_path)
    data = parse_data_to_set(data)
    for taxonomic_group in data:
        print(taxonomic_group)


