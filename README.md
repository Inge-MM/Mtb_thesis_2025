This repository contains the script used for my research project "Structural Mapping of 2-Component System Variants in
_Mycobacterium tuberculosis_". 

- The .py files make up the alignment and PhoPR extraction pipeline. To run this, main.py can be used with options from the command line. Files needed: the 'sequences' directory, containing subfolders of ENA study accessions with within them downloading scripts, and the reference sequence located in 'reference'.

  To download the raw sequencing data within the 'sequences' folders, the 'download_ENA_files.py' script can be used which makes a new download file per study accesion where the number of files to be downloaded can be specified. With bash the downloading scripts can be run per accession subdir.
- The PhoPR loci resulting from the pipeline were moved to the 'all_phopr/phopr_region' subdirectory, which is uploaded on google drive. These files are necesarry to run other scripts within the 'all_phopr' directory, namely MSA and the subsequent analysis of the MSA results.
- The 'chimerax' folder contains the .defattr files made and figures of the structures.
- The pipenn folder contains PIPENN, PIPENN-EMB, PIPENN 3 results for both PhoP and PhoR, and the jupyter notebook used to create figures and .csv used to make .defattr files (making .defattr files was done in 'msa_analysis.ipynb').
  
Important!
- two folders were too large to upload here, this includes the 'phopr_region' subdirectory in 'all_phopr', together with the 'all_consensus' files. These have been uploaded to google drive.

They can be found here: https://drive.google.com/drive/folders/13VHywBWXuIakVAMcK39uCyvMmD_COsTg?usp=drive_link.
  
