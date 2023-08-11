
# a version of blast_chewer.py that was completely suggested by the chatGPT according to a following query:

# We have input file of blast results looking basically like tab separated table. Now we want to do the following: 
# Read the data row by row and store them in the most handy format to be approached for whatever we need later
# Group data according to qseqid and sseqid; if there are cases of more than one pair of identical qseqid - sseqid pairs, keep the one with lowest e-value
# Polish the column with taxonomy from the NCBI, so that it only stores readable taxonomical hierarchy, without the accession number that is repeated at the beginning of this section
# Transform the original table into dictionary of dictionaries that looks like this: {sseqid: {qseqid: value, bitscore: value, taxonomy: value of the 3rd level of the hierarchy}
# For each accession compute its mean bitscore and how many qseqids it is linked to
# Sort accessions according to 1. number of qseqids it is hitting; 2. mean bitscore and save it in an appropriate type of variable

# Could you please write me a most elegant, swift and smooth python script to do this? 

# Would you consider using classes and functions or methods to improve the script or not?

###


import pandas as pd

class BlastAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.grouped_data = None
        self.result_dict = {}

    def read_blast_results(self):
        self.data = pd.read_csv(self.file_path, sep='\t', header=None,
                                names=['qseqid', 'sseqid', 'bitscore', 'evalue', 'taxonomy'])

    def group_and_filter(self):
        self.grouped_data = self.data.sort_values('evalue').groupby(['qseqid', 'sseqid']).first().reset_index()
        self.grouped_data['taxonomy'] = self.grouped_data['taxonomy'].str.split('; ').str[-1]

    def create_result_dict(self):
        for _, row in self.grouped_data.iterrows():
            sseqid = row['sseqid']
            qseqid = row['qseqid']
            bitscore = row['bitscore']
            taxonomy = row['taxonomy']

            if sseqid not in self.result_dict:
                self.result_dict[sseqid] = {}

            self.result_dict[sseqid][qseqid] = {'bitscore': bitscore, 'taxonomy': taxonomy}

    def calculate_metrics(self):
        for sseqid in self.result_dict:
            bitscores = [self.result_dict[sseqid][qseqid]['bitscore'] for qseqid in self.result_dict[sseqid]]
            mean_bitscore = sum(bitscores) / len(bitscores)
            qseqid_count = len(self.result_dict[sseqid])

            self.result_dict[sseqid]['mean_bitscore'] = mean_bitscore
            self.result_dict[sseqid]['qseqid_count'] = qseqid_count

    def sort_accessions(self):
        sorted_accessions = sorted(self.result_dict.keys(),
                                   key=lambda x: (self.result_dict[x]['qseqid_count'], self.result_dict[x]['mean_bitscore']),
                                   reverse=True)
        return sorted_accessions

def main():
    blast_analyzer = BlastAnalyzer('blast_results.txt')
    blast_analyzer.read_blast_results()
    blast_analyzer.group_and_filter()
    blast_analyzer.create_result_dict()
    blast_analyzer.calculate_metrics()
    sorted_accessions = blast_analyzer.sort_accessions()

    for sseqid in sorted_accessions:
        print(f"Sseqid: {sseqid}")
        print(f"Mean Bitscore: {blast_analyzer.result_dict[sseqid]['mean_bitscore']}")
        print(f"Number of qseqids: {blast_analyzer.result_dict[sseqid]['qseqid_count']}")
        print("")

if __name__ == "__main__":
    main()

