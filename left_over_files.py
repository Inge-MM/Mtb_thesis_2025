#!/usr/bin/python3
import os

accession_numbers = []
n_to_download = 250
for file in os.listdir('./all_phopr/'):
    if file.startswith('aln_'):
        accession = file.split('.')[0].split('_')[1]
        accession_numbers.append(accession)


for folder in os.listdir('./moving_files'):
    if folder.startswith('ENA_'):
        for file in os.listdir(f'./moving_files/{folder}'):
            if file.startswith('sorted-'):
                f = open(f'./sequences/{folder}/{file}', 'r')
                lines = []
                for i, line in enumerate(f):
                    lines.append(line.replace(' -nc', ' -c'))
                if folder == 'ENA_PRJEB3223':
                    lines = lines[:n_to_download-46]
                elif len(lines) >= n_to_download:
                    lines = lines[:n_to_download]
                write = ''
                for line in lines:
                    write += line + '\n'
                
                w = open(f'./moving_files/{folder}/top_{n_to_download}_download_{folder}.sh', 'w')
                w.write(write)
                f.close()

                for number in accession_numbers:
                    os.system(f'sed -i "/{number}/d" ./moving_files/{folder}/top_{n_to_download}_download_{folder}.sh')
                #os.system(f'sed -i "/^$/d" ./moving_files/{folder}/top_{n_to_download}_download_{folder}.sh')
                    
                w.close()