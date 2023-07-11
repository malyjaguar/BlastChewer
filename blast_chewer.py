#!/usr/bin/env python3

import argparse

def parse_arguments():
    usage = "./blast_chewer.py"
    description = ' \n \n \n"I will chew on your blast results to prepare a list of accessions for building phylogenetic tree."' + "\n\nThis script works with one txt input file that contains a table of blast hits for a given group of orthologous genes.\n "
    parser = argparse.ArgumentParser(usage, description=description, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-i", "--input", required = True, help = "Path to input file with blast results; txt file with space delimited table expected")
    parser.add_argument("-e", "--evalue", help="E-value treshold for blast hits; default = 1e-1", default = "1e-1")
    parser.add_argument("-n", "--nr_hits", help="Number of blast hits taken for a single ortholog; default = None", default = None)
    parser.add_argument("-o", "--output_path", help="Path to output file")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

# now it would be nice to validate the path to input file; we'll skip this step for now