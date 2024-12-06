# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 10:59:09 2022

@author: bojack
"""
from Bio import SeqIO
import MyLib as ml
from ftplib import FTP #載入ftp模組
import time
import os
import pandas as pd
import gzip

#os.chdir( r'G:\CLASS\2021下\專研\LeeHenry\PCA_Cluster\FTP_NCBI')
flog = open( "LOGFILE.txt", "w")

def IsATCG( seq):
    flag = 0    
    for c in seq:
        if c not in 'ATCG':
            flag = 1
            break
    return( flag)

def FNA2FAA( file):
    try:
#        print( file)
        mypath = r'I:\CLASS\2021下\專研\LeeHenry\PCA_Cluster\NCBI_serovar'
        ORFs = []
        headers = []
        cc = 0    
        fin = gzip.open(file, "rt")
        for rec in SeqIO.parse( fin, "genbank"):
            if cc == 0: 
                biosample = rec.dbxrefs[1].split(':')[1]
                print(file + " " + biosample)
    
            orfs = ml.FindORFs(rec.seq)
            for orf in orfs:
                if IsATCG( orf) == 0:
                    ORFs.append( ml.translate(orf))
                    headers.append( f"A{cc}")
                    cc += 1
                    
            orfs = ml.FindORFs( rec.seq.reverse_complement())
            for orf in orfs:
                if IsATCG( orf) == 0:
                    ORFs.append( ml.translate(orf))
                    headers.append( f"A{cc}")
                    cc += 1
        fin.close()
        ml.writeFast( os.path.join( mypath, biosample+".faa"), ORFs, headers)
        print( 'OK')
    except:
        fin.close()        
        # time.sleep(1)
        # file1 = file + 'E'
        # os.rename(file, file1)
        print( f"{file}\n")
        flog.write( f"{file}\n")        

#################################################
#################################################
df = pd.read_csv('Salmonella10805.csv', keep_default_na='', encoding='utf-8')
Salmonella10805_FTP = []
Salmonella10805 = {}    
for nl in df.values.tolist():    
    serovar = nl[1][nl[1].index('serovar'):]
    fc = serovar.find( ' str.')
    if fc > 0:
        serovar = serovar[:fc]
    Salmonella10805[nl[3]] = nl[:3] + [serovar]
    Salmonella10805_FTP.append( nl[0])
del df

FAAFTP = []
faapath = r'I:\CLASS\2021下\專研\LeeHenry\PCA_Cluster\NCBI_serovar'           
for root, dirs, files in os.walk(faapath):
    for file in files:
        print(Salmonella10805[file[:-4]][0].split('/')[-1])
        FAAFTP.append( Salmonella10805[file[:-4]][0].split('/')[-1])

gffpath = r'I:\CLASS\2021下\專研\LeeHenry\PCA_Cluster\FTP_NCBI'
GZFTP = []
for root, dirs, files in os.walk( gffpath):
    for file in files:
        if file.endswith( 'gbff.gz' ):
            GZFTP.append( file[:-16])


cc = 0        
lencc = len( Salmonella10805_FTP)
for fileA in Salmonella10805_FTP:
    file = fileA.split(r'/')[-1]
#    print( f"{file} {cc} {lencc}")
    if file not in GZFTP:
        pass
        # print( 'Not in GZ -' + file)
        # ftp=FTP() #設定變數
        # ftp.set_debuglevel(2) #開啟除錯級別2，顯示詳細資訊
        # ftp.connect("ftp.ncbi.nlm.nih.gov") #連線的ftp sever和埠
        # ftp.login("anonymous","bojack@mail.mcu.edu.tw")#連線的使用者名稱，密碼
        # bufsize=1024 #設定的緩衝區大小
        # ftp.cwd(fileA[27:]) #更改遠端目錄
        # filename=fileA.split("/")[-1]+"_genomic.gbff.gz" #需要下載的檔案
        # file_handle=open(filename,"wb").write #以寫模式在本地開啟檔案
        # ftp.retrbinary(f"RETR {filename}",file_handle,bufsize) #接收伺服器上檔案並寫入本地檔案
        # ftp.set_debuglevel(0) #關閉除錯模式
        # ftp.quit #退出ftp    
        # FNA2FAA( os.path.join( gffpath, file+"_genomic.gbff.gz"))
        
    elif file not in FAAFTP: 
        FNA2FAA( os.path.join( gffpath, file+"_genomic.gbff.gz"))
    
    cc += 1

    
flog.close()
