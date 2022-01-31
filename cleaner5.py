# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 10:51:43 2022

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


#%%


us_df = pandas.read_csv('us-cleaned.csv')
us_df['time'] = pandas.to_datetime(us_df['time'])

pair_df = pandas.read_csv('PAir-cleaned.csv')
pair_df['time'] = pandas.to_datetime(pair_df['time'])

renke_df = pandas.read_csv('renke-cleaned.csv')
renke_df['time'] = pandas.to_datetime(renke_df['time'])

epd_met_df = pandas.read_csv('epd-met-cleaned.csv')
epd_met_df['time'] = pandas.to_datetime(epd_met_df['time'])


#%%
#define functions to convert to daily from hourly

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
#use function hourly_avg to convert to daily average
us_df_d = hourly_avg(us_df)
renke_df_d = hourly_avg(renke_df)

pair_df_d = pandas.DataFrame()
for i in range(0,16,2):
    print(i)
    pair_df_d = pair_df_d.append(hourly_avg(pair_df.where(pair_df['location'] == 'PurpleAir-{}'.format(i)).dropna(subset = ['conc']).reset_index(drop = True)))

del i


#%%
# daily plots us embassy, epd met, renke, purple air

pair_sep_df = pair_df_d.pivot(index="time", columns="location", values="conc")
pair_sep_df = pair_sep_df.reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x = us_df_d['time'], y = us_df_d['conc'], mode = 'lines'))
fig.add_trace(go.Scatter(x = epd_met_df['time'], y = epd_met_df['conc'], mode = 'lines'))
for columns in pair_sep_df.columns[1:9]:
    fig.add_trace(go.Scatter(x = pair_sep_df['time'], y = pair_sep_df[columns], mode = 'lines'))
    
fig.add_trace(go.Scatter(x = renke_df_d['time'], y = renke_df_d['conc'], mode = 'lines'))
plot(fig)

del fig, columns, pair_sep_df

#%%
# daily plots of all epd and others

epd_met_df2 = pandas.read_csv('list2.csv')
epd_met_df2['time'] = pandas.to_datetime(epd_met_df2['Date'])

epd_met_df2.sort_values('time', inplace=True)

pair_sep_df = pair_df_d.pivot(index="time", columns="location", values="conc")
pair_sep_df = pair_sep_df.reset_index()
pair_sep_df.rename(columns = {'PurpleAir-0': 'Pair-GardenTown', 'PurpleAir-2': 'Pair-DefenceChowk',
                              'PurpleAir-4': 'Pair-IqbalTown', 'PurpleAir-6': 'Pair-AkbarChowk',
                              'PurpleAir-8': 'Pair-Township', 'PurpleAir-10': 'Pair-DHAPhase2',
                              'PurpleAir-12': 'Pair-Anarkali', 'PurpleAir-14': 'Pair-Harbanspura',}, inplace = True)


fig = go.Figure()
fig.add_trace(go.Scatter(x = us_df_d['time'], y = us_df_d['conc'], mode = 'lines', name = 'US-Embassy'))
for columns in pair_sep_df.columns[1:9]:
    fig.add_trace(go.Scatter(x = pair_sep_df['time'], y = pair_sep_df[columns], mode = 'lines', name = columns))
for columns in epd_met_df2.columns[1:30]:
    if epd_met_df2[columns].count() > 10:
        fig.add_trace(go.Scatter(x = epd_met_df2['time'], y = epd_met_df2[columns], mode = 'lines', name = columns))

plot(fig)

del fig, columns, epd_met_df2, pair_sep_df


#%%
# generate combined dataframe for processing


epd_met_df2 = pandas.read_csv('list2.csv')
epd_met_df2['time'] = pandas.to_datetime(epd_met_df2['Date'])

epd_met_df2.sort_values('time', inplace=True)

datelist = pandas.date_range(start="2019-01-01",end="2022-01-20").to_pydatetime().tolist()
combined_df = pandas.DataFrame(datelist, columns=['time'])
del datelist

combined_df = pandas.merge(left=combined_df, right=us_df_d.drop(columns = ['location', 'lat', 'long']), how='left', left_on='time', right_on='time')
combined_df.rename(columns = {'conc': 'US-Embassy'}, inplace = True)
combined_df = pandas.merge(left=combined_df, right=renke_df_d.drop(columns = ['location', 'lat', 'long']), how='left', left_on='time', right_on='time')
combined_df.rename(columns = {'conc': 'Renke-LUMS'}, inplace = True)

pair_sep_df = pair_df_d.pivot(index="time", columns="location", values="conc")
pair_sep_df = pair_sep_df.reset_index()
for column in pair_sep_df.columns[1:9]:
    combined_df = pandas.merge(left=combined_df, right=pair_sep_df[['time',column]].drop_duplicates(subset=['time']), how='left', on = 'time')

for column in epd_met_df2.columns[1:30]:
    if epd_met_df2[column].count() > 10:
        combined_df = pandas.merge(left=combined_df, right=epd_met_df2[['time',column]].drop_duplicates(subset=['time']), how='left', on = 'time')

del column

combined_df = combined_df.set_index('time')


#%%

#plot combined df

combined_df_plot = combined_df.rename(columns = {'PurpleAir-0': 'Pair-GardenTown', 'PurpleAir-2': 'Pair-DefenceChowk',
                              'PurpleAir-4': 'Pair-IqbalTown', 'PurpleAir-6': 'Pair-AkbarChowk',
                              'PurpleAir-8': 'Pair-Township', 'PurpleAir-10': 'Pair-DHAPhase2',
                              'PurpleAir-12': 'Pair-Anarkali', 'PurpleAir-14': 'Pair-Harbanspura'})

combined_df_plot = combined_df_plot.stack()
combined_df_plot = combined_df_plot.reset_index()
combined_df_plot = combined_df_plot.rename(columns = {'level_1': 'location', 0: 'conc'})

fig = px.line(combined_df_plot, x="time", y = 'conc', color = 'location',
             color_discrete_sequence=px.colors.qualitative.Alphabet)


plot(fig)


#%%
# compute pearson correlation
combined_df = combined_df.rename(columns = {'PurpleAir-0': 'Pair-GardenTown', 'PurpleAir-2': 'Pair-DefenceChowk',
                              'PurpleAir-4': 'Pair-IqbalTown', 'PurpleAir-6': 'Pair-AkbarChowk',
                              'PurpleAir-8': 'Pair-Township', 'PurpleAir-10': 'Pair-DHAPhase2',
                              'PurpleAir-12': 'Pair-Anarkali', 'PurpleAir-14': 'Pair-Harbanspura'})
combined_df2019 = combined_df[combined_df.index.year == 2019]
combined_df2020 = combined_df[combined_df.index.year == 2020]
combined_df2021 = combined_df[combined_df.index.year == 2021]
combined_df2021.append(combined_df[combined_df.index.year == 2022])
corr2019 = combined_df2019.corr()
corr2020 = combined_df2020.corr()
corr2021 = combined_df2021.corr()
corr = combined_df.corr()
#plt.matshow(corr)


#%%
# compute mean error
mae = pandas.DataFrame(columns = combined_df.columns,
                              index= combined_df.columns)
for column1 in combined_df.columns:
    for column2 in combined_df.columns:
        mae[column1][column2] = abs((combined_df[column1] - combined_df[column2])).mean()

del column1, column2

#%%
# compute mean absolute percentage error
mape = pandas.DataFrame(columns = combined_df.columns,
                              index= combined_df.columns)
for column1 in combined_df.columns:
    for column2 in combined_df.columns:
        mape[column1][column2] = (abs((combined_df[column1] - combined_df[column2])/combined_df[column1])*100).mean()

del column1, column2












