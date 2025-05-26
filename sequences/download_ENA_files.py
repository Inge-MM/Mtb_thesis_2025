# this script is to sort all ENA download files in their respective folders
# and make a new file containing the first n (20) sequences from the sorted file

import os

n = 400 # number of sequences to be kept from the sorted files

download = False
for folder in os.listdir():
    if not folder.endswith('.py'): #excluding this script
        for file in os.listdir(folder):
            file_dir = folder+'/'
            if file.startswith('ena-file'): # only unsorted files
                os.system(f'sort -n {file_dir+file} -o {file_dir}sorted-{file}')
                os.system(f'head -n {n} {file_dir}sorted-{file} > {file_dir}s{str(n)}-{file}')
                r = open(f'{file_dir}s{str(n)}-{file}', 'r')
                lines = r.read()

                r.close()
                lines = lines.replace(' -nc', ' -c ') # only downloads missing files
                w = open(f'{file_dir}s{str(n)}-{file}', 'w')
                w.write(lines)
                w.close()
                print(file_dir)
                # download
                if download:
                    os.system(file_dir+file)