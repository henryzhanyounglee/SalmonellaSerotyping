#!/usr/bin/env python
# -*- coding: utf-8 -*-
#"""
#Created on Mon Jun 24 16:41:20 2024 A.D. 民國壹佰壹拾參年 甲辰年 五月 十九日

#@author: Henry Zhan Young Lee 李湛然
#"""

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

# A00_10MATCH145 = MATCH145.rename(index= lambda x : map(lambda y : map(lambda z: z(y=="A00" if (int(y.strip("A")) <= 11) else y=="A00", y ), MATCH145.index), x))

# A00_10MATCH145 = MATCH145.rename(index=lambda x: f'A{x}' if isinstance(x, int) and 11 <= x <= 30 else 'A0' if x == 0 else x)


A0_10MATCH145 = MATCH145.replace(0, np.nan)
SumMATCH145 = A0_10MATCH145.groupby(['A']).sum(numeric_only = True)
SumMATCH145zeros = A0_10MATCH145.isnull().groupby(['A']).sum()
