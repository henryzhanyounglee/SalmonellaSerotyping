from Bio import SeqIO
import MyLib as ml
import os
from ReadBlastPMapingGene_02 import ReadBlastPMapingGene


# ss = "makeblastdb -input_type fasta -dbtype prot -in SalPiliGeneIDCount.faa  -out pili_genes"
# os.system( ss)

def BLASTPiliGene (file):              
    seq_obj = SeqIO.parse(file, 'fasta')
    
    ORFs = []
    headers = []
    geneNum = 0
    for rec in seq_obj:
        orfs = ml.FindORFs(rec.seq)
        for orf in orfs:
            if not 'N' in orf:
                ORFs.append( ml.translate(orf))
                headers.append( f"A{geneNum}")
                geneNum += 1
        orfs = ml.FindORFs( rec.seq.reverse_complement())
        for orf in orfs:
            if not 'N' in orf:
                ORFs.append( ml.translate(orf))
                headers.append( f"A{geneNum}")
                geneNum += 1
    
    ml.writeFast("All1.faa", ORFs, headers)
    
    ss = f"blastp -query {file}.faa -db pili_genes -outfmt 6 -evalue 1e-6 -threshold 300 -out AAA1.tub"
    os.system( ss)
    piligene145, match145 = ReadBlastPMapingGene( "AAA1.tub")
    return(piligene145, match145, geneNum)

FILES = []
for path, dirs, file in os.walk(r'I:\LEESAN\Salmonella_Genome\TEMP'):
    for files in file:
        if files[-4:] == '.fna':
            file = path + '\\' + files
            if os.stat(file).st_size <= 5576900:
                FILES.append(file)
                
for file in FILES:
    piligene145, match145, geneNum= BLASTPiliGene(file)