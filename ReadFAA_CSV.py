# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 13:56:59 2022

@author: bojack1
"""

from Bio import SeqIO
import os
import csv
from ReadBlastPMapingGene_02 import ReadBlastPMapingGene
import pandas as pd
from Bio.Cluster import distancematrix


# ss = "makeblastdb -input_type fasta -dbtype prot -in pili_genes.faa  -out pili_genes"
# os.system( ss)

    
def BLASTPiliGene02 (file, piligene145):     
    ss = f"blastp -query {file} -db pili_genes -outfmt 6 -evalue 1e-6 -threshold 300 -out AAA1.tub"
    os.system( ss)
    match145 = ReadBlastPMapingGene( "AAA1.tub", piligene145)
    return( match145)

def get_piligene145():
    file = "pili_genes.faa"
    seq_obj = SeqIO.parse(file, 'fasta')    
    piligene145 = []
    for seq in seq_obj:
        piligene145.append(seq.name)
    return( piligene145)

FILES = []
mypath = r'E:\LEESAN\Salmonella_Genome\TEMP1\NCBI_serovar'
for path, dirs, file in os.walk( mypath):
    for files in file:
        if files.endswith('.faa'):  ############[-4:] == '.faa':
            FILES.append( files)

piligene145 = get_piligene145()           
MATCH145s = []


MATCHED = []
MATCHED_145 = []
df = pd.read_csv('MATCH145s.txt', keep_default_na='', encoding='utf-8', delimiter="\t")
for nl in df.values.tolist():   
    MATCHED.append( nl[0].split('_')[1])
    MATCHED_145.append( nl[1:])

len_FILES = len(FILES)    
for cc, file in enumerate( FILES):
    print( file)
    print( f"{cc} in {len_FILES}" )
    if file[:-4] in MATCHED:
        fc = MATCHED.index( file[:-4])
        match145 = MATCHED_145[fc]
        MATCH145s.append( match145)
    else:    
        match145 = BLASTPiliGene02(os.path.join( mypath,file), piligene145)
        MATCH145s.append( match145)

df = pd.read_csv('Salmonella10805.csv', keep_default_na='', encoding='utf-8')
Salmonella10805 = {}    
for nl in df.values.tolist():    
    serovar = nl[1][nl[1].index('serovar'):]
    fc = serovar.find( ' str.')
    if fc > 0:
        serovar = serovar[:fc]
    Salmonella10805[nl[3]] = nl[:3] + [serovar]


with open('MATCH145sHENRYCut.txt', 'w', encoding='UTF8', newline='') as fout:
    writecsv = csv.writer(fout, quoting = csv.QUOTE_NONE, delimiter="\t")
    writecsv.writerow(['GeneName']+piligene145)
    for file, match145 in zip(FILES, MATCH145s):
        faa = Salmonella10805[ file[:-4]][3] + '_' + file[:-4]
        faa = faa.replace( '"', '')
        writecsv.writerow([faa] + match145)




matrix = distancematrix(MATCH145s)
with open('MATCH145sDistanceMatrixHENRYCut.csv', 'w', encoding='UTF8', newline='') as fout:
    writecsv = csv.writer(fout) 
    writecsv.writerow(matrix )