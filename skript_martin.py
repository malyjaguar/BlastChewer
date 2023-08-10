import os
import sys
import glob
import pandas as pd
from  collections import defaultdict
import ipdb

def blast_parser(blast):
        # open blast output and convert it to pandas dataframe
        # For Martin: here taxonomy was at the end, but in the data it shows as column 3, so we shifted the titles accordingly
        data = pd.read_csv(blast, sep = "\t", names = ['qseqid', 'sseqid', 'taxonomy', 'pident', 'length','matches', 'gaps', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']) 

        df = pd.DataFrame(data)
        print(df.head())

        # groupby specific columns and get the hit with the better e-value

        idx = df.groupby(['qseqid', 'sseqid'])['evalue'].transform(min) == df['evalue'] # martine, tady jsi mel 'max' a ono bylo potreba 'min' :-)
        df2 = df[idx]
        df2.to_csv('%s_single_aln.txt' % (sys.argv[1]), sep='\t')


blast_parser(sys.argv[1])

infile = open('%s_single_aln.txt' % (sys.argv[1]))
lines = infile.readlines()
infile.close()

# print(lines[:3])


d1 = defaultdict(list)
for line in lines[1:]:
    #print(line)
    #tax = line.split()[-1].split(' ')[1].split('__')
    tax = line.split('\t')[3] # Here we changed the index from [-1] to the correct taxonomy position 
    d1[line.split('\t')[2]].append({'query': line.split('\t')[1],'bitscore': line.split('\t')[-2], 'taxonomy': tax})
    ipdb.set_trace()
    # tady uplne nerozumime tomu, proc pouzivas defaultdict, a ne obycejny dict; je to duvod, proc jsou pak v d1 schovany [{}]...?

# import ipdb; ipdb.set_trace()


mean_bitscore_d = {}
num_hits_d = defaultdict(dict)

for acc in d1:
    total = 0
    for rec in d1[acc]:
        #print(rec)
        total = total + float(rec['bitscore'])
    mean_bitscore_d[acc] = float(total)/len(d1[acc])
    num_hits_d[len(d1[acc])][acc] =  (float(total)/len(d1[acc]))
#print(mean_bitscore_d)
print(num_hits_d)
num_hits_d = dict(reversed(sorted(num_hits_d.items())))
#aprint(num_hits_d)

for numb in num_hits_d:
    num_hits_d[numb] = dict(reversed(sorted(num_hits_d[numb].items(), key=lambda x:x[1])))

#print(num_hits_d)

acc_order = []

for numb in num_hits_d:
    for acc in num_hits_d[numb]:
        acc_order.append(acc)

final_acc_order = set(acc_order)

#aprint(final_acc_order)


final_ordered_tax_d = defaultdict(list)

for acc in final_acc_order:
    taxonomy = d1[acc][0]['taxonomy']
    #print(taxonomy)
    try:
        taxonomy = ' '.join(taxonomy.split(' ')[1:])
    except IndexError:
        taxonomy = ''
   # print(taxonomy)
    taxonomy = taxonomy.split('__')
    if len(taxonomy) >= 4:
        final_ordered_tax_d[taxonomy[3]].append(acc)
    elif len(taxonomy) > 0:
        final_ordered_tax_d[taxonomy[-1]].append(acc)
    else:
        pass
#print(final_ordered_tax_d)
    




'''
sorted_accs = []
for k in sorted(d1, key=lambda k: len(d1[k]), reverse=True):
    sorted_accs.append(k)
    rint(len(d1[k]))

print(d1)
'''









