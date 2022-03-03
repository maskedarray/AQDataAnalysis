# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 23:45:11 2022

@author: AbdurRahman
"""


import pandas

rankTable = pandas.read_csv('rankTable.csv')
rankTable.set_index('Unnamed: 0', inplace = True)
print(rankTable.sort_values(by = ['t1'],axis = 1))
rankTable2= rankTable.sort_values(by = ['t1'],axis = 1)






