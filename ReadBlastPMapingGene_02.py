def ReadBlastPMapingGene( fn):
    fn = "AAA.tub"
    import pandas as pd
    from Bio import SeqIO
    outfmt6 = pd.read_csv(fn, sep ='\t', header=None)
    
    outfmt6.columns = ['1. qseqid query or source (e.g., gene) sequence id',
           '2. sseqid subject or target (e.g., reference genome) sequence id',
           '3. pident percentage of identical matches',
           '4. length alignment length (sequence overlap)',
           '5. mismatch number of mismatches',
           '6. gapopen number of gap openings',
           '7. qstart start of alignment in query',
           '8. qend end of alignment in query',
           '9. sstart start of alignment in subject',
           '10. send end of alignment in subject',
           '11. evalue expect value',
           '12. bitscore bit score']
    
    
    outfmt6 = outfmt6.loc[outfmt6['3. pident percentage of identical matches'] >= 90]
    Genes = outfmt6['2. sseqid subject or target (e.g., reference genome) sequence id']
    
    
    uGenes = set( Genes)
    
    file = "SalPiliGeneIDCount.faa"
    seq_obj = SeqIO.parse(file, 'fasta')
    
    piligene145 = []
    match145 = []
    for seq in seq_obj:
        piligene145.append(seq.name)
        if (seq.name in uGenes):
            match145.append(1)
        else:
            match145.append(0)
       
    return (piligene145, match145)
        