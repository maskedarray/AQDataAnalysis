# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 16:38:19 2022

@author: AbdurRahman
"""

import csv
import pandas
import datetime
import numpy as np
import pytz
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objects as go
import numpy as np
import time
import matplotlib.pyplot as plt
import aqi
import math

# compute mean error
def mae_compute(df):
    mae = pandas.DataFrame(columns = df.columns,
                                  index= df.columns)
    for column1 in df.columns:
        for column2 in df.columns:
            mae[column1][column2] = abs((df[column1] - df[column2])).mean()
    
    del column1, column2
    return mae

#%%
# compute mean absolute percentage error
def mape_compute(df):
    mape = pandas.DataFrame(columns = df.columns,
                                  index= df.columns)
    for column1 in df.columns:
        for column2 in df.columns:
            mape[column1][column2] = (abs((df[column1] - df[column2])/df[column1])*100).mean()
    
    del column1, column2
    
#%%
# compute hourly average
def aggregate(df):
    time_dict = {}
    for ind in df.index:
        if not df['time'][ind] in time_dict.keys():
            time_dict[df['time'][ind]] = {'conc_agg': df['conc'][ind], 'count': 1}
        else:
            time_dict[df['time'][ind]] = {'conc_agg': time_dict[df['time'][ind]]['conc_agg'] + df['conc'][ind], 'count': time_dict[df['time'][ind]]['count'] + 1}
    df_ret = pandas.DataFrame.from_dict(time_dict, orient = 'index')
    return df_ret.reset_index()

def hourly_avg(main_df):
    us_df_h = main_df.copy()
    us_df_h['time'] = us_df_h['time'].dt.strftime("%Y-%m-%d")
    us_df_h['time'] = pandas.to_datetime(us_df_h['time'])
    #renke_df2 = renke_df2.groupby('time').mean().reset_index()
    
    us_df_h2 = aggregate(us_df_h)
    us_df_h2 = us_df_h2.where(us_df_h2['count']>=18)
    

    us_df_h2['conc'] = us_df_h2['conc_agg']/us_df_h2['count']
    us_df_h2.dropna(subset = ['conc'], inplace = True)
    us_df_h2.rename(columns = {'index': 'time'}, inplace = True)
    us_df_h2.drop(columns = ['conc_agg', 'count'], inplace = True)    

    
    us_df_h2['location'] = us_df_h['location'].where(us_df_h2['time'].isin(us_df_h['time']))
    us_df_h2['lat'] = us_df_h['lat'].where(us_df_h2['time'].isin(us_df_h['time']))
    us_df_h2['long'] = us_df_h['long'].where(us_df_h2['time'].isin(us_df_h['time']))
    
    return us_df_h2



    