#!/usr/bin/env python
# -*- coding: utf-8 -*-
#"""
#Created on Mon Mar  4 13:20:50 2024 A.D. 民國壹佰壹拾參年 甲辰年 正月 廿四

#@author: Henry Zhan Young Lee 李湛然
#"""

from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import warnings

warnings.filterwarnings("ignore")
MATCH145 = pd.read_csv( "match145SalV24Dec2023.csv", index_col="A").drop(columns = "Sero")
MATCH145 = MATCH145.rename({"A11" : "A0", "A12" : "A0",
                            "A13" : "A0", "A14" : "A0", "A15" : "A0",
                            "A16" : "A0", "A17" : "A0", "A18" : "A0",
                            "A19" : "A0", "A20" : "A0", "A21" : "A0",
                            "A22" : "A0", "A23" : "A0", "A24" : "A0",
                            "A25" : "A0", "A26" : "A0", "A27" : "A0",                            
                            "A28" : "A0", "A29" : "A0", "A30" : "A0"}).sort_index()
data = MATCH145.rename({"A0" : "Others", "A1" : "Typhi", "A2" : "Typhimurium",
                            "A3" : "Enteritidis", "A4" : "Kentucky", "A5" : "Heidelberg",
                            "A6" : "Newport", "A7" : "Infantis", "A8" : "Derby",
                            "A9" : "Weltevreden", "A10" : "Agona"})
sns.set(font="monospace")


NPNew9 = pd.read_csv( "NPNew9_df.csv")
Piligene = NPNew9.set_index("XX").index
Piligene = pd.Series(Piligene).tolist()

data1 = data[[c for c in data.columns if c in Piligene]]

datatmap = sns.heatmap(data1)

