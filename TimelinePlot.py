    # -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 12:09:15 2022

@author: AbdurRahman
"""

import pandas
import matplotlib.pyplot as plt
import numpy as np
from analysis_functions import *
from plotly.offline import plot
import math

us_df = pandas.read_csv('us-cleaned.csv')
us_df['time'] = pandas.to_datetime(us_df['time'])

pair_df = pandas.read_csv('PAir-cleaned.csv')
pair_df['time'] = pandas.to_datetime(pair_df['time'])

renke_df = pandas.read_csv('renke-cleaned.csv')
renke_df['time'] = pandas.to_datetime(renke_df['time'])

epd_met_df2 = pandas.read_csv('list2.csv')
epd_met_df2['time'] = pandas.to_datetime(epd_met_df2['Date'])

epd_met_df2.sort_values('time', inplace=True)
epd_met_df2.drop(columns = ['Date'], inplace=True)


us_df_d = hourly_avg(us_df)
renke_df_d = hourly_avg(renke_df)

pair_df_d = pandas.DataFrame()
for i in range(0,16,2):
    print(i)
    pair_df_d = pair_df_d.append(hourly_avg(pair_df.where(pair_df['location'] == 'PurpleAir-{}'.format(i)).dropna(subset = ['conc']).reset_index(drop = True)))

del i

#%%

def to_dategroups(df, column, location):
    out_df = pandas.DataFrame(columns = ['start','end', 'location'])
    datelist = pandas.date_range(start="2019-01-01",end="2022-01-25").to_pydatetime().tolist()
    
    start = 0
    end = 0
    start_date = 0
    end_date = 0
    for i in range(len(datelist)):
        value = df.loc[df['time'] == datelist[i]][column]
        if value.empty == False:
            if math.isnan(value) == False:
                if start == 0:
                    start = 1
                    start_date = datelist[i]
            else:
                if start == 1:
                    start = 0
                    end = 1
                    end_date = datelist[i] - datetime.timedelta(days=1)
        elif value.empty == True:
            if start == 1:
                start = 0
                end = 1
                end_date = datelist[i] - datetime.timedelta(days=1)
        if end == 1:
            end = 0
            out_df.loc[out_df.shape[0]] = [start_date, end_date, location]
    if start == 1:
        end_date = datelist[i]
        out_df.loc[out_df.shape[0]] = [start_date, end_date, location]
    return out_df
            
            

#%% reference plot
timeline_df = pandas.DataFrame()
timeline_df = timeline_df.append(to_dategroups(us_df_d, 'conc', 'US-Embassy'))
for column in epd_met_df2.columns[0:29]:
    if epd_met_df2[column].count() > 20:
        timeline_df = timeline_df.append(to_dategroups(epd_met_df2.drop_duplicates(subset=['time']), column, column))

fig = px.timeline(timeline_df, x_start='start', x_end="end", y="location", color = 'location', template="simple_white")
fig.update_yaxes(title = '')
fig.update_layout(showlegend=False)
plot(fig, filename = "Reference Main.html")


#%% low cost plot

timeline_df = pandas.DataFrame()

pair_sep_df = pair_df_d.pivot(index="time", columns="location", values="conc")
pair_sep_df = pair_sep_df.reset_index()

pair_sep_df = pair_sep_df.rename(columns = {'PurpleAir-0': 'PAir-GardenTown', 'PurpleAir-2': 'PAir-DefenceChowk',
                              'PurpleAir-4': 'PAir-IqbalTown', 'PurpleAir-6': 'PAir-AkbarChowk',
                              'PurpleAir-8': 'PAir-Township', 'PurpleAir-10': 'PAir-DHAPhase2',
                              'PurpleAir-12': 'PAir-Anarkali', 'PurpleAir-14': 'PAir-Harbanspura'})

for column in pair_sep_df.columns[1:9]:
    timeline_df = timeline_df.append(to_dategroups(pair_sep_df.drop_duplicates(subset=['time']), column, column))
timeline_df = timeline_df.append(to_dategroups(renke_df_d, 'conc', 'SDSA LUMS'))

fig = px.timeline(timeline_df, x_start='start', x_end="end", y="location", color = 'location', template="simple_white")
fig.update_yaxes(title = '')
fig.update_layout(showlegend=False)
plot(fig, filename = "Low Cost Main.html")


#%% timeline plotly express

# fig = px.timeline(timeline_df, x_start='start', x_end="end", y="location", color = 'location')
# #fig.update_yaxes(autorange="reversed")
# plot(fig)

#%%

# Declaring a figure "gnt"
fig, gnt = plt.subplots()
 
# Setting Y-axis limits
gnt.set_ylim(0, 50)
 
# Setting X-axis limits
gnt.set_xlim(0, 160)
 
# Setting labels for x-axis and y-axis
gnt.set_xlabel('seconds since start')
gnt.set_ylabel('Processor')
 
# Setting ticks on y-axis
gnt.set_yticks([15, 25, 35])
# Labelling tickes of y-axis
gnt.set_yticklabels(['1', '2', '3'])
 
# Setting graph attribute
gnt.grid(True)
 
# Declaring a bar in schedule
gnt.broken_barh([(40, 50)], (30, 9), facecolors =('tab:orange'))
 
# Declaring multiple bars in at same level and same width
gnt.broken_barh([(110, 10), (150, 10)], (10, 9),
                         facecolors ='tab:blue')
 
gnt.broken_barh([(10, 50), (100, 20), (130, 10)], (20, 9),
                                  facecolors =('tab:red'))
 
plt.savefig("gantt1.png")























