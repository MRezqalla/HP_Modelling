#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 11:57:26 2023

@author: kbiscoch
"""

import pandas as pd

hp_abbrev = ["D1_1","D1_2","D1_3","D1_4", # [0-4]
             "D2_1","D2_2","D2_3","D2_4","D2_5", # [4-9]
             "HL", # [9]
             "D3_1","D3_2", # [10-12]
             "D4_1","D4_2","D4_3", # [12-15]
             "D5_1","D5_2","D5_3"] # [15-18]

COP_heating = x[0]
COP_cooling = x[1]
temps_heating = x[2]
temps_cooling = np.array(x[3],ndmin=2)
temps_cooling = temps_cooling.T

COP_heating = np.column_stack(COP_heating)
COP_cooling = np.column_stack(COP_cooling)

column_names = hp_abbrev[0:4]
column_names.insert(0,'temp')
cool_df = pd.DataFrame(np.column_stack((temps_cooling,COP_cooling)),columns=column_names)
heat_df = pd.DataFrame(np.column_stack((temps_heating,COP_heating)),columns=column_names)

cool_df.to_csv('D1cool_COP_temp.csv')
heat_df.to_csv('D1heat_COP_temp.csv')
