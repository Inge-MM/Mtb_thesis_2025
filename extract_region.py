#!/usr/bin/python3

import os
import argparse
import textwrap

# setting arguments that can be passed from command line
parser = argparse.ArgumentParser(prog = "region extractor")

parser.add_argument('sequence_dir', 
                    help = 'directory of sequences where phoP/R is to be extracted')
parser.add_argument('-o', '--output',
                    help = 'output within sequence folder',
                    default = './sequences/ENA_PRJEB2138/phopr_region')
parser.add_argument('-a', '--additional_bp', 
                    help = 'number of bp to be used as a buffer on either side of the genetic region, default = 500',
                    default = 500, type = int)
parser.add_argument('-g', '--gene',
                    help = 'if a gene other than phoPR is to be extracted, enter the name of the gene')
parser.add_argument('-b', '--begin',
                    help = 'beginning bp of gene',
                    type = int)
parser.add_argument('-e', '--end',
                    help = 'end bp of gene',
                    type = int)

args = parser.parse_args()

# require location of region if it differs from phoPR
if args.gene and (args.begin is None or args.end is None):
    parser.error('--gene requires --begin and --end to return gene other than phoPR')

sequence_dir = args.sequence_dir
output_dir = args.output
buffer = args.additional_bp
os.system('mkdir '+output_dir)

# if gene is given use that to extract region, otherwise use phoPR
if args.gene:
    gene_name = args.gene
    gene_b = args.begin - buffer
    gene_e = args.end + buffer
else:
    gene_name = 'phoPR'
    gene_b = 851608 - buffer
    gene_e = 853853 + buffer

file_add = '_'+gene_name+'.fasta'    # this is added to the file names 

# for each file in the sequence folder, create a new file in the output
# folder where the header is copied and the wanted sequence is copied
for file in os.listdir(sequence_dir):
    file_name = file.split('.')[0]+file_add
    seq = ''
    f = open(sequence_dir+'/'+file, 'r')
    first_line = f.readline().strip('\n') + ' | '+gene_name+'\n'
    for line in f:
        seq += line.strip('\n')
    f.close()
    seq = seq[gene_b:gene_e]
    seq = textwrap.fill(seq, width=60)
    new_file = first_line+seq

    g = open(output_dir+'/'+file_name, 'w')
    g.write(new_file)
    g.close()