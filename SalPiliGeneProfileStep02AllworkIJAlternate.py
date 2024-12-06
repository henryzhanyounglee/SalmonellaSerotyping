#!/usr/bin/env python
# -*- coding: utf-8 -*-
#"""
#Created on Mon Mar  4 14:14:20 2024 A.D. 民國壹佰壹拾參年 甲辰年 正月 廿四

#@author: Henry Zhan Young Lee 李湛然
# """

import pandas as pd
import numpy as np
import warnings
import sys

warnings.filterwarnings("ignore")

def testWithA01( NP, tester):
    A05s = list(NP.columns[1:])
    num_c = len(NP.index)
    ans = 'NA'
    for A05 in A05s:
        cc = 0
        for a, b in zip( NP[A05], tester[1:]):
            if a == b or a == -1:
                cc += 1
        if cc == num_c:
            ans = A05
            break
    return ans

def testNP( NP, MATCH145):
    MATCH145A = MATCH145.T
    MATCH145A = MATCH145A[NP.columns]

    columnsNum = len( NP.columns)
    A0_A5 = {}
    for i in range(columnsNum):
        A0_A5[f"A{i}"] = [0 for i in range(columnsNum)]
    A05s = list(NP.columns[1:]) + ['NA']
    B_out = []
    for _, row in MATCH145A.iterrows():
        ans = testWithA01(NP, row)
        n = A05s.index( ans)
        if row[0] not in A0_A5:
            row[0] = 'A0'
        B_out.append(ans)
        A0_A5[ row[0]][n] += 1
    MATCH145New = MATCH145.copy().T
    MATCH145New['B_out'] = B_out

    A0_A5_df = pd.DataFrame.from_dict( A0_A5).T
    A0_A5_df.columns = A05s
    # correct = 0
    # for i in range( 1, len(A0_A5_df)):
    #     correct += A0_A5_df.iloc[i,i]
    # print(A0_A5_df)
    return A0_A5_df, MATCH145New

def testNP1( NP, MATCH145):
    MATCH145A =  MATCH145.loc[NP.index]

    # MATCH145A0 = MATCH145 - MATCH145.loc[NPNew9_df.index]

    columnsNum = len( NP.columns)-1
    A0_A5 = {}
    for i in range(columnsNum):
        A0_A5[f"A{i}"] = [0 for i in range(columnsNum+1)]
    A05s = list(NP.columns[1:]) + ['NA']
    B_out = []
    for _, row in MATCH145A.iterrows():
        ans = testWithA01( NP, row)
        n = A05s.index( ans)
        if row[0] not in A0_A5:
            row[0] = 'A0'
        B_out.append(ans)
        A0_A5[ row[0]][n] += 1
    MATCH145New = MATCH145.copy()
    MATCH145New['B_out'] = B_out

    A0_A5_df = pd.DataFrame.from_dict( A0_A5).T
    A0_A5_df.columns = A05s
    # correct = 0
    # for i in range( 1, len(A0_A5_df)):
    #     correct += A0_A5_df.iloc[i,i]
    # print(A0_A5_df)
    return( A0_A5_df, MATCH145New)

def CorrectRate(A0_A9_df):
    A1_10 = [f'A{i}' for i in range(1,11)]
    ss = 0
    ss_all = 0
    for a1 in A1_10:
        ss += A0_A9_df.loc[a1 , a1]
        ss_all += sum( A0_A9_df.loc[a1])
    return ss , ss_all, ss/ss_all

def test( NP, MATCH145_A10):
    RES = []
    for AA, row in MATCH145_A10.iterrows():
#        print( row)
        res = 'A0'
        for np0 in list(NP.columns):
            cc = 0
            for i, pili in enumerate(NP.index):
                if NP.loc[pili,np0] == 1 and row[i] == 1:
                    cc += 1
                if NP.loc[pili,np0] == 0 and row[i] == 0:
                    cc += 1
                if NP.loc[pili,np0] == -1:
                    cc += 1
            if cc == 10:
                res = np0
                break
        RES.append( res)
    return RES

def RES2JDFPili( RES, MATCH145_A10):
    AA_RES = pd.DataFrame( [MATCH145_A10.index, RES]).T
    AA_RES.columns = ['r1','r2']
    J = []
    for np0 in list(NPNew9_df.columns)+['A0']:
        T1 = sum( (AA_RES.r1 == np0) & (AA_RES.r2 == np0))
        T4 = sum( (AA_RES.r1 != np0) & (AA_RES.r2 != np0))
        T3 = sum( (AA_RES.r1 != np0) & (AA_RES.r2 == np0))
        T2 = sum( (AA_RES.r1 == np0) & (AA_RES.r2 != np0))
#        print( T1,T2,T3,T4)
        J.append([np0, T1, T2, T3, T4])
        ####$$#####
    
    JDFPili = pd.DataFrame(J)
    JDFPili = JDFPili.rename(columns={0: "XX"})
    JDFPili = JDFPili.set_index("XX")
    if sum( JDFPili.iloc[:10,0])+sum( JDFPili.iloc[:10,1]) > 0:
        Sen=sum( JDFPili.iloc[:10,0])/(sum( JDFPili.iloc[:10,0])+sum(JDFPili.iloc[:10,1]))
    else:
        Sen=0
    if JDFPili.iloc[10,0]+JDFPili.iloc[10,1] > 0:
        Spe=JDFPili.iloc[10,0]/(JDFPili.iloc[10,0]+JDFPili.iloc[10,1])
    else:
        Spe=0
    return JDFPili, Sen, Spe


MATCH145 = pd.read_csv( "MATCH145sHENRYCutB.txt",sep = "\t", index_col="A")
MATCH145 = MATCH145.rename({"A11" : "A0", "A12" : "A0",
                            "A13" : "A0", "A14" : "A0", "A15" : "A0",
                            "A16" : "A0", "A17" : "A0", "A18" : "A0",
                            "A19" : "A0", "A20" : "A0", "A21" : "A0",
                            "A22" : "A0", "A23" : "A0", "A24" : "A0",
                            "A25" : "A0", "A26" : "A0", "A27" : "A0",                            
                            "A28" : "A0", "A29" : "A0", "A30" : "A0"})

MATCH145 = MATCH145.rename({"A0" : "A0", "A1" : "Typhi", "A2" : "Typhimurium",
                            "A3" : "Enteritidis", "A4" : "Kentucky", "A5" : "Heidelberg",
                            "A6" : "Newport", "A7" : "Infantis", "A8" : "Derby",
                            "A9" : "Weltevreden", "A10" : "Agona"})

NPNew9_df = pd.read_csv("AllworkPiliNPNew9_df.csv", sep = ",", index_col='XX')

MATCH145_A10 = MATCH145[ NPNew9_df.index]

####################################################################
def SenSpeFun( NPNew9_df2, MATCH145_A10):
    RES = test( NPNew9_df2, MATCH145_A10) 
    JDFPili, Sen, Spe = RES2JDFPili( RES, MATCH145_A10)
    if 1 == 1:
        Sen1 = []
        Spe1 = []
        for i in range(10):
            aa = JDFPili.iloc[i]
            Sen1.append(aa[1]/(aa[1]+aa[2]))
            Spe1.append( aa[4]/(aa[3]+aa[4])) 
        Spe = np.mean(Spe1)
        Sen = np.mean(Sen1) 
    cor = sum( JDFPili.iloc[:-1,0])/( sum(JDFPili.iloc[:-1,0])+sum(JDFPili.iloc[:-1,1]))
    return Sen+Spe, Sen, Spe, JDFPili, cor

_, Sen, Spe, JDFPili, cor =SenSpeFun( NPNew9_df, MATCH145_A10) 
JDFPili.to_csv("MJDFPiliIJLoop.csv")

NDF = []
IDX = [-1,1,0]
SenSpe = np.zeros( 3)
Sen3 = np.zeros( 3)
Spe3 = np.zeros( 3)

NPNew9_df1 = NPNew9_df.copy()

np.set_printoptions(threshold=sys.maxsize)


for i in range(10):     ###i,j,i
    for j in range(10): ###j,i,j
        NPNew9_df2 = NPNew9_df1.copy()
        NPNew9_df2.iloc[i,j] = -1
        SenSpe[0] , Sen3[0], Spe3[0],_,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)
        NPNew9_df2.iloc[i,j] = 1
        SenSpe[1] , Sen3[1], Spe3[1],_,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)
        NPNew9_df2.iloc[i,j] = 0
        SenSpe[2] , Sen3[2], Spe3[2],_,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)  
        idxA = SenSpe.argmax()
        NPNew9_df1.iloc[i,j] = IDX[idxA]
        # print(f"{i}{j} ; {SenSpe[idxA]} ; {Sen3[idxA]} ; {Spe3[idxA]}\n", SenSpe )
        NDF.append([0,i,j,SenSpe[idxA], Sen3[idxA],Spe3[idxA]])

for j in range(10):     ###i,j,i
    for i in range(10): ###j,i,j
        NPNew9_df2 = NPNew9_df1.copy()
        NPNew9_df2.iloc[i,j] = -1
        SenSpe[0] , Sen3[0], Spe3[0], _,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)
        NPNew9_df2.iloc[i,j] = 1
        SenSpe[1] , Sen3[1], Spe3[1], _,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)
        NPNew9_df2.iloc[i,j] = 0
        SenSpe[2] , Sen3[2], Spe3[2], _,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)  
        idxA = SenSpe.argmax()
        NPNew9_df1.iloc[i,j] = IDX[idxA]
        # print(f"{i}{j} ; {SenSpe[idxA]} ; {Sen3[idxA]} ; {Spe3[idxA]}\n", SenSpe )
        NDF.append([1,i,j,SenSpe[idxA], Sen3[idxA],Spe3[idxA]])

for i in range(10):     ###i,j,i
    for j in range(10): ###j,i,j
        NPNew9_df2 = NPNew9_df1.copy()
        NPNew9_df2.iloc[i,j] = -1
        SenSpe[0] , Sen3[0], Spe3[0], _,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)
        NPNew9_df2.iloc[i,j] = 1
        SenSpe[1] , Sen3[1], Spe3[1], _,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)
        NPNew9_df2.iloc[i,j] = 0
        SenSpe[2] , Sen3[2], Spe3[2], _,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)  
        idxA = SenSpe.argmax()
        NPNew9_df1.iloc[i,j] = IDX[idxA]
        # print(f"{i}{j} ; {SenSpe[idxA]} ; {Sen3[idxA]} ; {Spe3[idxA]}\n", SenSpe )
        NDF.append([2,i,j,SenSpe[idxA], Sen3[idxA],Spe3[idxA]])

for j in range(10):     ###i,j,i
    for i in range(10): ###j,i,j
        NPNew9_df2 = NPNew9_df1.copy()
        NPNew9_df2.iloc[i,j] = -1
        SenSpe[0] , Sen3[0], Spe3[0], _,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)
        NPNew9_df2.iloc[i,j] = 1
        SenSpe[1] , Sen3[1], Spe3[1], _,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)
        NPNew9_df2.iloc[i,j] = 0
        SenSpe[2] , Sen3[2], Spe3[2], _,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)  
        idxA = SenSpe.argmax()
        NPNew9_df1.iloc[i,j] = IDX[idxA]
        # print(f"{i}{j} ; {SenSpe[idxA]} ; {Sen3[idxA]} ; {Spe3[idxA]}\n", SenSpe )
        NDF.append([3,i,j,SenSpe[idxA], Sen3[idxA],Spe3[idxA]])

for i in range(10):     ###i,j,i
    for j in range(10): ###j,i,j
        NPNew9_df2 = NPNew9_df1.copy()
        NPNew9_df2.iloc[i,j] = -1
        SenSpe[0] , Sen3[0], Spe3[0], _,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)
        NPNew9_df2.iloc[i,j] = 1
        SenSpe[1] , Sen3[1], Spe3[1], _,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)
        NPNew9_df2.iloc[i,j] = 0
        SenSpe[2] , Sen3[2], Spe3[2], _,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)  
        idxA = SenSpe.argmax()
        NPNew9_df1.iloc[i,j] = IDX[idxA]
        # print(f"{i}{j} ; {SenSpe[idxA]} ; {Sen3[idxA]} ; {Spe3[idxA]}\n", SenSpe )
        NDF.append([2,i,j,SenSpe[idxA], Sen3[idxA],Spe3[idxA]])

for j in range(10):     ###i,j,i
    for i in range(10): ###j,i,j
        NPNew9_df2 = NPNew9_df1.copy()
        NPNew9_df2.iloc[i,j] = -1
        SenSpe[0] , Sen3[0], Spe3[0], _,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)
        NPNew9_df2.iloc[i,j] = 1
        SenSpe[1] , Sen3[1], Spe3[1], _,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)
        NPNew9_df2.iloc[i,j] = 0
        SenSpe[2] , Sen3[2], Spe3[2], _,_ = SenSpeFun( NPNew9_df2, MATCH145_A10)  
        idxA = SenSpe.argmax()
        NPNew9_df1.iloc[i,j] = IDX[idxA]
        # print(f"{i}{j} ; {SenSpe[idxA]} ; {Sen3[idxA]} ; {Spe3[idxA]}\n", SenSpe )
        NDF.append([3,i,j,SenSpe[idxA], Sen3[idxA],Spe3[idxA]])
        
_, Sen, Spe, JDFPili, cor =SenSpeFun( NPNew9_df1, MATCH145_A10) 
JDFPili.to_csv("MFinJDFPiliIJLoop.csv")
print(cor)
# print(Sen, Spe, cor, JDFPili)
########

NPNew9_df1.to_csv("MeanGeneProfilePiliGeneIJAlternate.csv")

NDF = pd.DataFrame(NDF)
NDF.to_csv("MeanSenSpeRatePiliGeneIJAlternate.csv")


# NDF = pd.DataFrame(NDF)

# NPNew9_df1.to_csv("AllworkGeneProfilePiliGeneIJAlternate.csv")
# NDF.to_csv("AllworkSenSpeRatePiliGeneIJAlternate.csv")

