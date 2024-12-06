from Bio import SeqIO
import MyLib as ml
import os
from ReadBlastPMapingGene_02 import ReadBlastPMapingGene


#ss = "makeblastdb -input_type fasta -dbtype prot -in SalPiliGeneIDCount.faa  -out pili_genes"
#os.system( ss)

file = r"I:\CLASS\2021下\專研\LeeHenry\Salmononella\SEQ\ATFA01_1.faa"
seq_obj = SeqIO.parse(file, 'fasta')

ORFs = []
headers = []
cc = 0
for rec in seq_obj:
    orfs = ml.FindORFs(rec.seq)
    for orf in orfs:
        if not 'N' in orf:
            ORFs.append( ml.translate(orf))
            headers.append( f"A{cc}")
            cc += 1
    orfs = ml.FindORFs( rec.seq.reverse_complement())
    for orf in orfs:
        if not 'N' in orf:
            ORFs.append( ml.translate(orf))
            headers.append( f"A{cc}")
            cc += 1

ml.writeFast("All.faa", ORFs, headers)

ss = "blastp -query ALL.faa -db pili_genes -outfmt 6 -evalue 1e-6 -threshold 300 -out AAA.tub"
os.system( ss)
piligene145, match145 = ReadBlastPMapingGene( "AAA.tub")
