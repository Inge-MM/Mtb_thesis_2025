# script to change headers, compile all fasta files and perform MSA
import os

# changing header so it begins with the sequence accession instead of the study accession, and remove an empty space

for file in os.listdir('./phopr_region'):
    if file.endswith('.fasta') and file.startswith('aln_'):
        f = open('./phopr_region/'+file, 'r')
        header = f.readlines()
        if header:
            accession = file.split('.')[0].split('_')[1]
            header[0] = f'>{accession}|phoPR\n'
            f = open('./phopr_region/'+file, 'w')
            f.writelines(header)
            f.close()
            
# compiling into 1 file
os.system('''awk 'FNR==1{print ""}1' ./phopr_region/aln_*.fasta > combined_phopr.fasta''')

# keeping length
os.system(f'mafft --6merpair --keeplength --add combined_phopr.fasta ./phopr_region/reference_phoPR.fasta > msa.fasta')

# not keeping length
#os.system(f'mafft --6merpair --add combined_phopr.fasta ./phopr_region/reference_phoPR.fasta > msa_do_not_keep_length.fasta')