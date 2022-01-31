# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 11:38:06 2022

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


#%%

us_2019_df = pandas.read_csv('Lahore_PM2.5_2019_YTD.csv')
us_2020_df = pandas.read_csv('Lahore_PM2.5_2020_YTD.csv')
us_2021_df = pandas.read_csv('Lahore_PM2.5_2021_YTD.csv')
us_2022_df = pandas.read_csv('Lahore_PM2.5_2022_01_MTD.csv')

us_2019_df.rename(columns = {'Date (LT)': 'time'}, inplace = True)
us_2020_df.rename(columns = {'Date (LT)': 'time'}, inplace = True)
us_2021_df.rename(columns = {'Date (LT)': 'time'}, inplace = True)
us_2022_df.rename(columns = {'Date (LT)': 'time'}, inplace = True)

#31.56056594470933, 74.33581606192398

us_2019_df = us_2019_df[us_2019_df['QC Name'] == 'Valid']
us_2020_df = us_2020_df[us_2020_df['QC Name'] == 'Valid']
us_2021_df = us_2021_df[us_2021_df['QC Name'] == 'Valid']
us_2022_df = us_2022_df[us_2022_df['QC Name'] == 'Valid']


us_2019_df.drop(columns = ['Year', 'Month', 'Day', 'Hour', 'NowCast Conc.',
                           'AQI', 'AQI Category', 'Conc. Unit', 'Duration',
                           'QC Name', 'Parameter'], inplace = True)
us_2020_df.drop(columns = ['Year', 'Month', 'Day', 'Hour', 'NowCast Conc.',
                           'AQI', 'AQI Category', 'Conc. Unit', 'Duration',
                           'QC Name', 'Parameter'], inplace = True)
us_2021_df.drop(columns = ['Year', 'Month', 'Day', 'Hour', 'NowCast Conc.',
                           'AQI', 'AQI Category', 'Conc. Unit', 'Duration',
                           'QC Name', 'Parameter'], inplace = True)
us_2022_df.drop(columns = ['Year', 'Month', 'Day', 'Hour', 'NowCast Conc.',
                           'AQI', 'AQI Category', 'Conc. Unit', 'Duration',
                           'QC Name', 'Parameter'], inplace = True)

us_2019_df['Site'] = 'US-Embassy'
us_2020_df['Site'] = 'US-Embassy'
us_2021_df['Site'] = 'US-Embassy'
us_2022_df['Site'] = 'US-Embassy'

us_2019_df = us_2019_df.assign(lat = 31.56056594470933, long = 74.33581606192398)
us_2020_df = us_2020_df.assign(lat = 31.56056594470933, long = 74.33581606192398)
us_2021_df = us_2021_df.assign(lat = 31.56056594470933, long = 74.33581606192398)
us_2022_df = us_2022_df.assign(lat = 31.56056594470933, long = 74.33581606192398)

us_df = us_2019_df.copy()
us_df = us_df.append(us_2020_df, ignore_index = True)
us_df = us_df.append(us_2021_df, ignore_index = True)
us_df = us_df.append(us_2022_df, ignore_index = True)

del us_2019_df, us_2020_df, us_2021_df, us_2022_df

us_df['time'] = pandas.to_datetime(us_df['time'], format = '%Y-%m-%d %I:%M %p')
us_df.rename(columns = {'Raw Conc.': 'conc', 'Site': 'location'}, inplace = True)

us_df = us_df.reindex(columns=['time','conc','location','lat','long'])

#%%

import os
filelist = []
for subdir, dirs, files in os.walk("./"):
    for file in files:
        filelist.append(file)
        

del dirs, file, files, subdir

#%%

lat_list = [31.501559,31.501559,31.4859,31.4859,31.510158,31.510158,31.468374,31.468374,31.444512,31.444512,
            31.480284,31.480284,31.565131,31.565131,31.570236,31.570236]
long_list = [74.306762,74.306762,74.3735,74.3735,74.284233,74.284233,74.301385,74.301385,74.309754,74.309754,
             74.404699, 74.404699,74.310783,74.310783,74.412914,74.412914]
pair_df = pandas.DataFrame()

for i in range(0,15,2):
    print(i)
    filename1 = filelist[i]
    filename2 = filelist[i+1]
    
    df_prim = pandas.read_csv(filename1)
    df_sec = pandas.read_csv(filename2)
    
    
    df_prim.drop(columns = ['entry_id', 'PM1.0_CF1_ug/m3', 'PM2.5_CF1_ug/m3', 'PM10.0_CF1_ug/m3',
                            'UptimeMinutes', 'RSSI_dbm', 'Temperature_F', 'Humidity_%', 'Unnamed: 10'],
                 inplace = True)
    df_sec.drop(columns = ['entry_id', 'PM1.0_CF1_ug/m3', 'PM2.5_CF1_ug/m3', 'PM10.0_CF1_ug/m3',
                            'UptimeMinutes', 'IAQ', 'ADC', 'Pressure_hpa', 'Unnamed: 10'],
                 inplace = True)
    
    
    df_prim.rename(columns = {'created_at': 'time', 'PM2.5_ATM_ug/m3': 'conc'}, inplace = True)
    df_sec.rename(columns = {'created_at': 'time', 'PM2.5_ATM_ug/m3': 'conc'}, inplace = True)
    
    df_prim['time'] = pandas.to_datetime(df_prim['time'])
    df_prim['time'] = df_prim['time'].dt.tz_convert(pytz.timezone('Asia/Karachi'))
    df_prim['time'] = df_prim['time'].dt.tz_localize(None)
    
    df_sec['time'] = pandas.to_datetime(df_sec['time'])
    df_sec['time'] = df_sec['time'].dt.tz_convert(pytz.timezone('Asia/Karachi'))
    df_sec['time'] = df_sec['time'].dt.tz_localize(None)
    
    df_prim['time'] = df_prim['time'].dt.strftime("%Y-%m-%d %H")
    df_prim['time'] = pandas.to_datetime(df_prim['time'])
    
    df_sec['time'] = df_sec['time'].dt.strftime("%Y-%m-%d %H")
    df_sec['time'] = pandas.to_datetime(df_sec['time'])
    
    df_prim = df_prim.groupby('time').mean().reset_index()
    df_sec = df_sec.groupby('time').mean().reset_index()
    
    df_merge = pandas.merge(left=df_prim, right=df_sec, left_on='time', right_on='time')
    
    df_merge['conc'] = (df_merge['conc_x'] + df_merge['conc_y'])/2
    
    df_merge = df_merge.drop(columns = ['conc_x', 'conc_y'])
    
    df_merge['location'] = "PurpleAir-{}".format(i)
    
    df_merge = df_merge.assign(lat = lat_list[i], long = long_list[i])
    
    pair_df = pair_df.append(df_merge)

del lat_list, long_list, i, filelist, df_prim, df_sec, df_merge, filename1, filename2


#%%
"""
import os
filelist = []
for subdir, dirs, files in os.walk("./"):
    for file in files:
        filelist.append(file)
        

del dirs, file, files, subdir

#%%

lat_list = [31.501559,31.501559,31.4859,31.4859,31.510158,31.510158,31.468374,31.468374,31.444512,31.444512,
            31.480284,31.480284,31.402162,31.402162,31.570236,31.570236]
long_list = [74.306762,74.306762,74.3735,74.3735,74.284233,74.284233,74.301385,74.301385,74.309754,74.309754,
             74.404699, 74.404699,74.274149,74.274149,74.412914,74.412914]
pair_df2 = pandas.DataFrame()

for i in range(0,15,2):
    print(i)
    filename1 = filelist[i]
    filename2 = filelist[i+1]
    
    df_prim = pandas.read_csv(filename1)
    df_sec = pandas.read_csv(filename2)
    
    
    df_prim.drop(columns = ['entry_id', 'PM1.0_CF1_ug/m3', 'PM2.5_CF1_ug/m3', 'PM10.0_CF1_ug/m3',
                            'UptimeMinutes', 'RSSI_dbm', 'Temperature_F', 'Humidity_%', 'Unnamed: 10'],
                 inplace = True)
    df_sec.drop(columns = ['entry_id', 'PM1.0_CF1_ug/m3', 'PM2.5_CF1_ug/m3', 'PM10.0_CF1_ug/m3',
                            'UptimeMinutes', 'IAQ', 'ADC', 'Pressure_hpa', 'Unnamed: 10'],
                 inplace = True)
    
    
    df_prim.rename(columns = {'created_at': 'time', 'PM2.5_ATM_ug/m3': 'conc'}, inplace = True)
    df_sec.rename(columns = {'created_at': 'time', 'PM2.5_ATM_ug/m3': 'conc'}, inplace = True)
    
    df_prim['time'] = pandas.to_datetime(df_prim['time'])
    df_prim['time'] = df_prim['time'].dt.tz_convert(pytz.timezone('Asia/Karachi'))
    df_prim['time'] = df_prim['time'].dt.tz_localize(None)
    
    df_sec['time'] = pandas.to_datetime(df_sec['time'])
    df_sec['time'] = df_sec['time'].dt.tz_convert(pytz.timezone('Asia/Karachi'))
    df_sec['time'] = df_sec['time'].dt.tz_localize(None)
    
    df_prim['time'] = df_prim['time'].dt.strftime("%Y-%m-%d %H")
    df_prim['time'] = pandas.to_datetime(df_prim['time'])
    
    df_sec['time'] = df_sec['time'].dt.strftime("%Y-%m-%d %H")
    df_sec['time'] = pandas.to_datetime(df_sec['time'])
    
    df_prim = df_prim.groupby('time').mean().reset_index()
    df_sec = df_sec.groupby('time').mean().reset_index()
    
    df_merge = pandas.merge(left=df_prim, right=df_sec, left_on='time', right_on='time')
    
    df_merge['conc'] = (df_merge['conc_x'] + df_merge['conc_y'])/2
    
    df_merge = df_merge.drop(columns = ['conc_x', 'conc_y'])
    
    if i == 12:
        j = 16
    else:
        j = i
    df_merge['location'] = "PurpleAir-{}".format(j)
    
    df_merge = df_merge.assign(lat = lat_list[i], long = long_list[i])
    
    pair_df2 = pair_df2.append(df_merge)

del lat_list, long_list, i, filelist, df_prim, df_sec, df_merge, filename1, filename2

pair_df = pair_df.append(pair_df2)
"""
#%%

# fig = go.Figure()
# fig.add_trace(go.Scatter(x = df_merge['time'], y = df_merge['conc_x'], mode = 'markers'))
# fig.add_trace(go.Scatter(x = df_merge['time'], y = df_merge['conc_y'], mode = 'markers'))
# fig.add_trace(go.Scatter(x = df_merge['time'], y = df_merge['conc'], mode = 'markers'))
# plot(fig)


#%%

pair_df.to_csv('PAir-cleaned.csv', index=False)
us_df.to_csv('us-cleaned.csv', index=False)











