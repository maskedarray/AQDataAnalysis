# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 14:29:06 2022

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


combined_df = pandas.read_csv('combined_daily_data.csv')
combined_df['time'] = pandas.to_datetime(combined_df['time'])

combinedAQI_df = combined_df.copy()


#%% calculate US EPA AQI

for column in combined_df.columns[1:16]:
    for i in range(len(combined_df[column])):
        if not np.isnan(combined_df[column][i]):
            if combined_df[column][i] < 500:
                combinedAQI_df[column][i] = aqi.to_iaqi(aqi.POLLUTANT_PM25, combined_df[column][i], algo=aqi.ALGO_EPA)
            else:
                combinedAQI_df[column][i] = 600
        else:
            combinedAQI_df[column][i] = math.nan

combinedAQI_df = combinedAQI_df.set_index('time')

#%% plot combined AQI

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

combinedAQI_df = combinedAQI_df.rename(columns = {'PurpleAir-0': 'Pair-GardenTown', 'PurpleAir-2': 'Pair-DefenceChowk',
                              'PurpleAir-4': 'Pair-IqbalTown', 'PurpleAir-6': 'Pair-AkbarChowk',
                              'PurpleAir-8': 'Pair-Township', 'PurpleAir-10': 'Pair-DHAPhase2',
                              'PurpleAir-12': 'Pair-Anarkali', 'PurpleAir-14': 'Pair-Harbanspura'})
combined_df2019 = combinedAQI_df[combinedAQI_df.index.year == 2019]
combined_df2020 = combinedAQI_df[combinedAQI_df.index.year == 2020]
combined_df2021 = combinedAQI_df[combinedAQI_df.index.year == 2021]
combined_df2021.append(combinedAQI_df[combinedAQI_df.index.year == 2022])
corr2019 = combined_df2019.corr()
corr2020 = combined_df2020.corr()
corr2021 = combined_df2021.corr()
corr = combinedAQI_df.corr()
#plt.matshow(corr)


#%%
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

#%% convert to aqi bands

def to_aqiband(aqi_value):
    if aqi_value <= 100:
        return 1
    elif aqi_value <= 200:
        return 2
    elif aqi_value <= 300:
        return 3
    elif aqi_value <= 400:
        return 4
    elif aqi_value <= 500:
        return 5
    else:
        return 6

combinedAQIBand_df = combinedAQI_df.copy()

for column in combinedAQI_df.columns:
    for i in range(len(combinedAQI_df[column])):
        if not np.isnan(combinedAQI_df[column][i]):
            combinedAQIBand_df[column][i] = to_aqiband(combinedAQI_df[column][i])
        else:
            combinedAQIBand_df[column][i] = math.nan

mae = mae_compute(combinedAQIBand_df)

for column in combinedAQIBand_df.columns[1:15]:
    print(column)
    print(sum(combinedAQIBand_df['US-Embassy'] == combinedAQIBand_df[column]))


#%%

combinedAQIBand_df.to_csv('combinedAQIBand.csv')
combinedAQI_df.to_csv('combinedAQI.csv')



#%%

df = combinedAQIBand_df[['US-Embassy', 'EPA Gulberg', 'Met Station',
                                 'Dental College']]

for column in df.columns:
    print(df[column][df[column] == 5].count())


df2 = combinedAQIBand_df.max(axis = 1)

df2.value_counts(dropna = False)

#%%
colors1 = ['#19E601', '#93FF26', '#F5F000', '#F5B801', '#FF075A', '#7D042C']
colors2 = ['#19E601', '#F5F000', '#F5B801', '#FF075A', '#BE25CC','#7D042C']
fig = go.Figure()
fig.add_trace(go.Bar( x = ['Good', "Moderate", "Unhealthy (Sensitive)", "Unhealthy", "Very Unhealthy", "Hazardous"],
                      y = [89    , 653           , 186                  , 97    , 58         , 6],
                     showlegend = False, marker_color=colors2))
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
fig.update_xaxes(title = "Time", showline=True, linewidth=2, linecolor='black', mirror=True)
fig.update_yaxes(title = 'Number of Days', showline=True, linewidth=2, linecolor='black', mirror=True)


plot(fig)
 
del df2, column, df

#%%






