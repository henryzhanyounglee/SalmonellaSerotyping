def readFast( fn):
    fp = open(fn, "r") #"w", "a"  a:append
    line = fp.readline()
    header = line 
    seq = ''
    while line:
        line = fp.readline()
        if ( len( line) > 0 ):
            if (line[-1] == '\n'):
                line = line[:-1]
            seq = seq + line
        
    fp.close()
    return( header, seq)

########################################################
def FindExtraORFs( seq, PlotOn = 0):
    import matplotlib.pyplot as plt
    
    orfs = []  #開放閱讀框 (Open reading frame)  
    orf_Beg = []
    orf_End = []
    orf_Len = []
    
    for i in range(0, len(seq)-5):
        if (seq[i:i+3] == "ATG"): 
            seq2 = seq[i:]
            for j in range(0, len(seq2)-5, 3):
                if (seq2[j:j+3] == "TAA" or seq2[j:j+3] == "TAG" or seq2[j:j+3] == "TGA" ):   
                    orfs.append(seq[i:i+j+3] )
                    orf_Beg.append( i)
                    orf_End.append( i+j+3)
                    orf_Len.append( j+3)
                    break
    ExtraORFs = []
    if (len( orf_Len) > 0):                
        max_orf_Len = max( orf_Len)                
        orf_Len_index  =orf_Len.index( max_orf_Len)
    #    print( orf_Len_index, max_orf_Len )
        
        if (PlotOn == 1):
            plt.clf()
            plt.plot([1, len(seq)], [0,0], 'r-', linewidth=10)
            plt.plot([orf_Beg[orf_Len_index], orf_End[orf_Len_index]], [0,0], 'b-', linewidth=20)
            plt.text( orf_End[orf_Len_index],  0,  'MAX', fontsize = 30)
            plt.show()
        
        cc = 0
        dd = 1
        for orf in orfs:
            if (orf_Len[cc] > 300):
                if (orf_End[orf_Len_index] == orf_End[cc]): 
                    if (PlotOn == 1):
                        plt.plot([orf_Beg[cc], orf_End[cc]], [dd,dd], 'g-', linewidth=10)
                else:
                    if (PlotOn == 1):
                        plt.plot([orf_Beg[cc], orf_End[cc]], [dd,dd], 'r-', linewidth=10)
                        plt.text( orf_End[cc],  dd,  'Extra ORF', fontsize = 30)
                    ExtraORFs.append( orfs[cc])
                dd += 1        
        #    print( orf)
        #    print( cc)
            cc += 1 #cc = cc + 1
            
    return( ExtraORFs)



def FindORFs( seq):
    
    orfs = []  #開放閱讀框 (Open reading frame)  

    lastStopPoz = 0
    cc = 0
    for i in range(0, len(seq)-5):
        if (seq[i:i+3] == "ATG"): 
            seq2 = seq[i:]
            for j in range(0, len(seq2)-5, 3):
                if (seq2[j:j+3] == "TAA" or seq2[j:j+3] == "TAG" or seq2[j:j+3] == "TGA" ):
                    if (j > 180 and lastStopPoz != i+j+3):
                        orfs.append(seq[i:i+j+3] )
#                        print( seq[i:i+j+3])
                        cc += 1
                        lastStopPoz = i+j+3
#                        print( cc, i, i+j+3)
                    break

#    len_seq = len(seq)
#    print( f"Ori={len_seq} Gene Number = {cc}")
    return( orfs)

def translate(seq):
      
    table = {
        'ATA':'I', 'ATC':'I', 'ATT':'I', 'ATG':'M',
        'ACA':'T', 'ACC':'T', 'ACG':'T', 'ACT':'T',
        'AAC':'N', 'AAT':'N', 'AAA':'K', 'AAG':'K',
        'AGC':'S', 'AGT':'S', 'AGA':'R', 'AGG':'R',                
        'CTA':'L', 'CTC':'L', 'CTG':'L', 'CTT':'L',
        'CCA':'P', 'CCC':'P', 'CCG':'P', 'CCT':'P',
        'CAC':'H', 'CAT':'H', 'CAA':'Q', 'CAG':'Q',
        'CGA':'R', 'CGC':'R', 'CGG':'R', 'CGT':'R',
        'GTA':'V', 'GTC':'V', 'GTG':'V', 'GTT':'V',
        'GCA':'A', 'GCC':'A', 'GCG':'A', 'GCT':'A',
        'GAC':'D', 'GAT':'D', 'GAA':'E', 'GAG':'E',
        'GGA':'G', 'GGC':'G', 'GGG':'G', 'GGT':'G',
        'TCA':'S', 'TCC':'S', 'TCG':'S', 'TCT':'S',
        'TTC':'F', 'TTT':'F', 'TTA':'L', 'TTG':'L',
        'TAC':'Y', 'TAT':'Y', 'TAA':'', 'TAG':'',
        'TGC':'C', 'TGT':'C', 'TGA':'', 'TGG':'W',
    }
    protein =""
    if len(seq)%3 == 0:
        for i in range(0, len(seq), 3):
            codon = seq[i:i + 3]
            protein+= table[codon]
    return( protein)

def writeFast(fn, seqs, headers):
    fo = open(fn, 'w')
    cc = 0
    for seq in seqs:
        fo.writelines( ">" + headers[cc] + "\n" )
        fo.writelines( seq + "\n" )
        cc += 1
    fo.close()