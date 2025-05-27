import os

# this script was used on bazis (now ada) to move finished sequences into
# a seperate dir for downloading

export_folder = 'phopr_export11'
sequences_batch = 'sequences'
what_to_export = 'phopr_region/*.fasta'

path = f'./{sequences_batch}/'
for folder in os.listdir(path):
    if os.path.isdir(path+folder):
        #consensus_dir = '/mnt/e/export2/'+folder+'/consensus'
        os.system(f'mkdir ./{export_folder}/{folder}')
        os.system(f'mkdir ./{export_folder}/{folder}/phopr_region')
        os.system(f'mkdir ./{export_folder}/{folder}/consensus')
        os.system(f'cp ./{sequences_batch}/{folder}/{what_to_export} ./{export_folder}/{folder}/phopr_region -r')
        os.system(f'cp ./{sequences_batch}/{folder}/consensus/*.fasta ./{export_folder}/{folder}/consensus -r')

