# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 14:56:01 2022

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

#%%


us_df = pandas.read_csv('us-cleaned.csv')
us_df['time'] = pandas.to_datetime(us_df['time'])

pair_df = pandas.read_csv('PAir-cleaned.csv')
pair_df['time'] = pandas.to_datetime(pair_df['time'])

renke_df = pandas.read_csv('renke-cleaned.csv')
renke_df['time'] = pandas.to_datetime(renke_df['time'])

epd_met_df = pandas.read_csv('metstation2.csv')
epd_met_df.drop(columns = ['Unnamed: 0'], inplace = True)
epd_met_df.rename(columns = {'date': 'time', 'value': 'conc'}, inplace = True)
epd_met_df['location'] = 'EPD-MetStation'
epd_met_df = epd_met_df.assign(lat = 31.5425058929335, long = 74.32475501445185)
epd_met_df['time'] = pandas.to_datetime(epd_met_df['time'])
epd_met_df.sort_values(by = "time", inplace = True)

#%%

#hourly plots purple air and us embassy and renke
pair_sep_df = pair_df.pivot(index="time", columns="location", values="conc")
pair_sep_df = pair_sep_df.reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x = us_df['time'], y = us_df['conc'], mode = 'lines'))
for columns in pair_sep_df.columns[1:9]:
    fig.add_trace(go.Scatter(x = pair_sep_df['time'], y = pair_sep_df[columns], mode = 'lines'))
    
fig.add_trace(go.Scatter(x = renke_df['time'], y = renke_df['conc'], mode = 'lines'))
plot(fig)

#del fig, columns, pair_sep_df

#%%

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

#%%



us_df_d = hourly_avg(us_df)
renke_df_d = hourly_avg(renke_df)

pair_df_d = pandas.DataFrame()
for i in range(0,16,2):
    print(i)
    pair_df_d = pair_df_d.append(hourly_avg(pair_df.where(pair_df['location'] == 'PurpleAir-{}'.format(i)).dropna(subset = ['conc']).reset_index(drop = True)))



#%%
#daily plots us embassy, epd met, renke, purple air

pair_sep_df = pair_df_d.pivot(index="time", columns="location", values="conc")
pair_sep_df = pair_sep_df.reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x = us_df_d['time'], y = us_df_d['conc'], mode = 'lines'))
fig.add_trace(go.Scatter(x = epd_met_df['time'], y = epd_met_df['conc'], mode = 'lines'))
for columns in pair_sep_df.columns[1:9]:
    fig.add_trace(go.Scatter(x = pair_sep_df['time'], y = pair_sep_df[columns], mode = 'lines'))
    
fig.add_trace(go.Scatter(x = renke_df_d['time'], y = renke_df_d['conc'], mode = 'lines'))
plot(fig)

#del fig, columns, pair_sep_df

#%%


epd_met_df.to_csv('epd-met-cleaned.csv', index=False)













