#!/usr/bin/python3

# this script runs the entire sequence alignment pipeline and returns a consensus sequence
import os
import argparse

# setting arguments that can be passed from command line
parser = argparse.ArgumentParser(prog = 'fastq to fasta pipeline')

parser.add_argument('sequence_dir', 
                    help = 'directory of sequences to be aligned')
parser.add_argument('reference',
                    help = 'reference sequence directory (should end with .fasta)')
parser.add_argument('-t', '--threads', 
                    help = 'number of threads to be used, default = 1',
                    default = 1, choices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                    type = int)

args = parser.parse_args()

sequence_dir = args.sequence_dir
n_threads = str(args.threads)
reference_seq = args.reference

reference_dir = '/'.join(reference_seq.split('/')[:-1])
aligned_dir = sequence_dir+'/aligned'
consensus_dir = sequence_dir+'/consensus'

# programs and options
cutadapt_options_pe = '-j '+n_threads+' -q 24 -m 30 --cut 10 -U 5'
cutadapt_options = '-j '+n_threads+' -q 24 -m 30 --cut 10'
bwa = 'bwa mem'
bwa_options = '-t '+n_threads+' -v 0'
samtools_options = '-@ '+n_threads 

# making folders to store faligned and consensus sequences
new_dirs = ['aligned', 'consensus']
for i in new_dirs:
    if i not in os.listdir(sequence_dir):
        os.system('mkdir '+sequence_dir+'/'+i)

# indexing reference genome if this was not previously done
if len(os.listdir('./reference')) == 1:
    os.system(f'{bwa} index {reference_seq}')

###############################################
###            CREATING FUNCTIONS           ###
###############################################

# organize sequence pairs in a dictionary
def seq_files(directory):
    sequencing_pairs = []
    for file in sorted(os.listdir(directory)):
        if file.endswith('fastq.gz'):
            sequencing_pairs.append(file)
    
    pairs = {}
    unpaired = []
    for i in sequencing_pairs:
        if i.endswith('_1.fastq.gz') or i.endswith('_2.fastq.gz'):
            id1, num1 = i.split('_')
            num1, _, _ = i.split('.')
            if id1 not in pairs.keys():
                for j in sequencing_pairs:
                    if j.startswith(id1):
                        num2, _, _ = j.split('.') 
                        pairs[id1] = [num1, num2]
        else:
            id1, _, _ = i.split('.')
            if id1 not in unpaired:
                unpaired.append(id1)

        pairs['unpaired'] = unpaired

    return pairs

# trimming reads
def trim_seq(pairs):    
    for keys in pairs.keys():
        if keys == 'unpaired':
                for val in pairs['unpaired']:
                    if val+'_cut.fastq' not in os.listdir(sequence_dir):
                        in1 = sequence_dir+'/'+val+'.fastq.gz'
                        out1 = sequence_dir+'/'+val+'_cut.fastq'
                        os.system(f'cutadapt {in1} -o {out1} {cutadapt_options}')
            
        elif pairs[keys][0]+'_cut.fastq' not in os.listdir(sequence_dir): 
            in1 = sequence_dir+'/'+pairs[keys][0]+'.fastq.gz'
            out1 = sequence_dir+'/'+pairs[keys][0]+'_cut.fastq'
            in2 = sequence_dir+'/'+pairs[keys][1]+'.fastq.gz'
            out2 = sequence_dir+'/'+pairs[keys][1]+'_cut.fastq' 
            os.system(f'cutadapt {in1} {in2} -o {out1} -p {out2} {cutadapt_options_pe}')

# aligning to reference genome, sorting SAM and outputting a BAM file
def align_pairs(ref, pairs_cut):    
    for keys in pairs_cut.keys():
        if keys == 'unpaired':
                for val in pairs['unpaired']:
                    if 'aln_'+val+'.bam' not in os.listdir(aligned_dir):
                        in1 = sequence_dir+'/'+val+'.fastq'
                        out = aligned_dir+'/aln_'+val.split('_')[0]+'.bam'
                        os.system(f'{bwa} {ref} {in1} {bwa_options} | samtools sort {samtools_options} -o {out}') 

        elif 'aln_'+keys+'.bam' not in os.listdir(aligned_dir):   
            in1 = sequence_dir+'/'+pairs[keys][0]+'.fastq'
            in2 = sequence_dir+'/'+pairs[keys][1]+'.fastq'
            out = aligned_dir+'/aln_'+keys+'.bam'
            os.system(f'{bwa} {ref} {in1} {in2} {bwa_options} | samtools sort {samtools_options} -o {out}') 

# consensus sequence
def consensus():
    for file in os.listdir(aligned_dir):
        file = file.split('.')[0]
        if file+'.fasta' not in os.listdir(consensus_dir):
            os.system(f'samtools consensus {samtools_options} {aligned_dir}/{file}.bam -o {sequence_dir}/consensus/{file}.fasta')

# changing headers
def header():
    for file in os.listdir(consensus_dir):
        f = open(consensus_dir+'/'+file, 'r')
        header = f.readlines()
        accession_n = sequence_dir.split('/')[-1]
        header[0] = f'>{accession_n} | {file.split(".")[0].split("_")[1]}\n'
        
        f = open(consensus_dir+'/'+file, 'w')
        f.writelines(header)
        f.close()


###############################################
###            RUNNING FUNCTIONS            ###
###############################################

pairs = seq_files(sequence_dir)
trim_seq(pairs)

# making a dictionary containing read pairs
pairs_cut = pairs
for key in pairs.keys():
    new_val = pairs_cut[key] 
    new_val = [i + '_cut' for i in new_val]
    pairs_cut[key] = new_val

align_pairs(reference_seq, pairs_cut)
consensus()
header()