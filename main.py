#!/usr/bin/python3

# runs fastqc to fasta pipeline and extract region 
# for all files in sequence folder

import os
import argparse

# setting arguments that can be passed from command line
parser = argparse.ArgumentParser(prog = 'looping scripts over all folders')

#arguments for fastq2fasta
parser.add_argument('sequences_dir', 
                    help = 'directory containing ENA subfolders')
parser.add_argument('reference',
                    help = 'reference sequence directory')
parser.add_argument('-t', '--threads', 
                    help = 'number of threads to be used, default = 1',
                    default = 1, choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                    type = int)

args = parser.parse_args()

sequences_dir = args.sequences_dir
n_threads = str(args.threads)
reference_seq = args.reference

folders_done = 0 #added to limit
for folder in os.listdir(sequences_dir):
    folders_done +=1
    # I DELTED FILES SO EXCLUDE THOSE IF THE SPECIFIC FOLDER IS MISSING!!!!!!!!!
    #if folders_done <= 10 and 
    if os.path.isdir(sequences_dir+'/'+folder): # seeing whether the file/folder is a directory
        folder_dir = sequences_dir+'/'+folder
        aligned_dir = folder_dir+'/consensus'
        phopr_dir = folder_dir+'/phopr_region'
        # making consensus sequence
        os.system(f'python3 ./fastq2fasta_pipeline.py {folder_dir} {reference_seq} -t {n_threads}')
        # extracting region of intereest
        os.system(f'python3 ./extract_region.py {aligned_dir} -o {phopr_dir}')