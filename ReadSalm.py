from Bio import SeqIO
import MyLib as ml
import os
from ReadBlastPMapingGene_02 import ReadBlastPMapingGene



file = r"I:\CLASS\2021下\專研\LeeHenry\Salmononella\SEQ\ATFA01_1.faa"
seq_obj = SeqIO.parse(file, 'fasta')

sequences = []
for seq in seq_obj:
    sequences.append(seq)

seqs = []
headers = []
dd = 0
match145s = []
for record in sequences:
    sequence = record.seq    
    orfs = ml.FindORFs(sequence)
    cc = 0
    for orf in orfs:
        seqs.append( ml.translate(orf)[:-1])
        headers.append( f"A_{cc}") 
        cc += 1
    
    ml.writeFast(f"S{dd}aaa.faa", seqs, headers)
    ss = f"blastp -query S{dd}aaa.faa -db pili_genes -outfmt 6 -evalue 1e-6 -threshold 300 -out AAA.tub"
    print( dd)
    dd += 1

    os.system( ss)
    piligene145, match145 = ReadBlastPMapingGene( "AAA.tub")
    match145s.append( match145)

#import numpy as np
#match145s_np = np.array(match145s) 

with open( "piligene145.txt", "w") as fout:
    fout.write( 'GeneName')
    for piligene in piligene145: 
        fout.write( '\t' + piligene)
    fout.write('\n')
    cc = 0
    for match145 in match145s:
        fout.write( f'count{cc}')
        cc += 1
        for match1 in match145:
            fout.write( f'\t{match1}')
        fout.write('\n')
            
            
        

