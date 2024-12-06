#!/usr/bin/env python
# -*- coding: utf-8 -*-
#"""
#Created on Wed Jan 24 13:36:08 2024 A.D. 民國壹佰壹拾參年 癸卯年 臘月 十亖

#@author: Henry Zhan Young Lee 李湛然
#"""

import pandas as pd
import numpy as np

def getCrossT( MATCH145, AA):
    Piligene = MATCH145.columns
    CrossT = np.zeros((len( Piligene), 4), dtype = int)
    dfA = MATCH145[MATCH145.index == AA]
    lenA = len( dfA)
    dfB = MATCH145[MATCH145.index != AA]
    lenB = len( dfB)
    crossT = [0,0,0,0]  
    for i, pg in enumerate(Piligene):
        crossT[0] = sum( dfA[pg] == 1)  
        crossT[1] = lenA - crossT[0]
        crossT[2] = sum( dfB[pg] == 1)
        crossT[3] = lenB - crossT[2]
        CrossT[i] = crossT
    return CrossT

def Sen_Spe(CrossT):
    SenSpe = np.zeros((len(CrossT),4), dtype = float)
    for i , cr in enumerate(CrossT):
        SenSpe[i, 0] = cr[0]/(cr[0] + cr[1])###Specificity
        SenSpe[i, 1] = cr[3]/(cr[2] + cr[3])###Sentivity
        SenSpe[i, 2] = cr[0]/10559###Specificity
        SenSpe[i, 3] = cr[3]/10559###Sentivity
    return SenSpe

def findIndMATCH145( MATCH145AB, j):
    Piligene = MATCH145AB.columns
    CrossT = getCrossT(MATCH145AB, f'A{j}')
    SenSpe = Sen_Spe(CrossT)
    SenSpe_sum = sum( [SenSpe[:,0]*1 + SenSpe[:,1]*1])
    sum_indA = SenSpe_sum.argsort()[::-1]
    sel_indA = sum_indA[0]
    CR = CrossT[sum_indA[0]]
    TopSenSpe = SenSpe[sel_indA]
    TopPili = Piligene[sel_indA]
    # print(CR, f'A{j}', SenSpe[sum_indA[:1]], len( MATCH145AB))
    return CR, TopPili, TopSenSpe, f'A{j}'
    
MATCH145 = pd.read_csv( "match145SalV24Dec2023.csv", index_col="A").drop(columns = "Sero")
MATCH145 = MATCH145.rename({"A11" : "A0", "A12" : "A0",
                            "A13" : "A0", "A14" : "A0", "A15" : "A0",
                            "A16" : "A0", "A17" : "A0", "A18" : "A0",
                            "A19" : "A0", "A20" : "A0", "A21" : "A0",
                            "A22" : "A0", "A23" : "A0", "A24" : "A0",
                            "A25" : "A0", "A26" : "A0", "A27" : "A0",                            
                            "A28" : "A0", "A29" : "A0", "A30" : "A0"}).sort_index()

Piligene = MATCH145.columns

MATCH145A = MATCH145.copy()
TopSen = []
TopSpe = []
A1_10 = [i for i in range(1,11)]
FinalPili = [] 
FinalAllWork = []
for i in range(1,11):
    SelSenSpe = []
    SelPili = [] 
    CR_ALL = []
    for j in A1_10:
        CR, TopPili, TopSenSpe, Ai = findIndMATCH145( MATCH145A, j)
        SelPili.append( TopPili)
        SelSenSpe.append( (TopSenSpe[0] + TopSenSpe[1])/2)
        TopSen.append(TopSenSpe[1])
        TopSpe.append(TopSenSpe[0])
        CR_ALL.append(CR)
    ind = SelSenSpe.index( max(SelSenSpe))###Addition of sum
    print( '\n\n\n', CR_ALL[ind], SelSenSpe[ ind], SelPili[ind], A1_10[ind])
    FinalAllWork.append([f"A{A1_10[ind]}", SelPili[ind], CR_ALL[ind], SelSenSpe[ ind]])
    FinalPili.append( [SelPili[ind], A1_10[ind]])
    A1_10.pop(ind)
    MATCH145A = MATCH145A[MATCH145A[SelPili[ind]] == 0]

SenSpe = pd.DataFrame( TopSen , TopSpe)
SenSpe.to_csv("SalCDDidMEanTopSenSpeOnebyOne.csv")

FPili = dict(FinalPili)        
FPili = pd.DataFrame.from_dict(FPili, orient='index')
FPili.to_csv("MeanFCDDid.csv")
FinalAllWork = pd.DataFrame(FinalAllWork, columns = ["Abundance", "CDDid", "CorrectFiles", "AverageSenSpe"]) 
FinalAllWork.to_csv("FinalMeanCDDid.csv")

