# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 10:59:09 2022

@author: bojack
"""
from ftplib import FTP #載入ftp模組
import time

FTP_Files = []
with open( 'Salmonella001.txt', 'r') as fin:
    for line in fin:
        FTP_Files.append( line.strip())
cc = 0        
for files in FTP_Files:
    if cc >= 0: #535:
        ftp=FTP() #設定變數
        ftp.set_debuglevel(2) #開啟除錯級別2，顯示詳細資訊
        ftp.connect("ftp.ncbi.nlm.nih.gov") #連線的ftp sever和埠
        ftp.login("anonymous","10396054@me.mcu.edu.tw")#連線的使用者名稱，密碼
        bufsize=1024 #設定的緩衝區大小
        ftp.cwd(files[27:]) #更改遠端目錄
        filename=files.split("/")[-1]+"_genomic.gbff.gz" #需要下載的檔案
        file_handle=open(filename,"wb").write #以寫模式在本地開啟檔案
        ftp.retrbinary(f"RETR {filename}",file_handle,bufsize) #接收伺服器上檔案並寫入本地檔案
        ftp.set_debuglevel(0) #關閉除錯模式
        ftp.quit #退出ftp
    cc += 1
    time.sleep(5)

