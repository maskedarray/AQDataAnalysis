# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 11:58:48 2022

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

#%%

renke_df = pandas.read_csv('Renke2021-12-01 15_07 TO 2021-12-31 00_00.csv')
renke_df = renke_df.drop(columns = ['Node name', 'PM10(ug/m3)'])
renke_df.rename(columns = {'PM2.5(ug/m3)': 'conc', 'Recording Time': 'time'}, inplace = True)

renke_df['time'] = pandas.to_datetime(renke_df['time'])
renke_df['time'] = renke_df['time'].dt.strftime("%Y-%m-%d %H")
renke_df['time'] = pandas.to_datetime(renke_df['time'])
renke_df = renke_df.groupby('time').mean().reset_index()

renke_df = renke_df.assign(lat = 31.469140063664643, long = 74.40849523976961)
renke_df['location'] = 'Lums'
renke_df = renke_df.reindex(columns=['time','conc','location','lat','long'])



renke_df2 = pandas.read_csv('Historical record2022-01-14 08_50 TO 2022-01-19 09_50.csv')
renke_df2 = renke_df2.drop(columns = ['Node name', 'PM10(ug/m3)'])
renke_df2.rename(columns = {'PM2.5(ug/m3)': 'conc', 'Recording Time': 'time'}, inplace = True)

renke_df2['time'] = pandas.to_datetime(renke_df2['time'])
renke_df2['time'] = renke_df2['time'].dt.strftime("%Y-%m-%d %H")
renke_df2['time'] = pandas.to_datetime(renke_df2['time'])
renke_df2 = renke_df2.groupby('time').mean().reset_index()

renke_df2 = renke_df2.assign(lat = 31.469140063664643, long = 74.40849523976961)
renke_df2['location'] = 'Lums'
renke_df2 = renke_df2.reindex(columns=['time','conc','location','lat','long'])

renke_df = renke_df.append(renke_df2)


renke_df.to_csv('renke-cleaned.csv', index=False)
#%%


fig = go.Figure()
fig.add_trace(go.Scatter(x = pair_df['time'], y = pair_df['conc'], mode = 'markers'))
fig.add_trace(go.Scatter(x = us_df['time'], y = us_df['conc'], mode = 'markers'))
# fig.add_trace(go.Scatter(x = pair_df['time'], y = pair_df['conc'], mode = 'markers'))
plot(fig)


#%%

pair_sep_df = pair_df.pivot(index="time", columns="location", values="conc")
pair_sep_df = pair_sep_df.reset_index()

fig = go.Figure()
fig.add_trace(go.Scatter(x = us_df['time'], y = us_df['conc'], mode = 'lines'))
for columns in pair_sep_df.columns[1:9]:
    fig.add_trace(go.Scatter(x = pair_sep_df['time'], y = pair_sep_df[columns], mode = 'lines'))
    
fig.add_trace(go.Scatter(x = renke_df['time'], y = renke_df['conc'], mode = 'lines'))
plot(fig)


#%%

#ONLY FOR AQI CALCULATIONS. NOT RAW COMPARISON WITH US DATA
pair_sep_df = pair_df.pivot(index="time", columns="location", values="conc")
pair_sep_df = pair_sep_df.reset_index()


#print(df['A'].rolling(24,center = True, min_periods=1).mean())

pair_1hour_avg = pandas.DataFrame()
pair_1hour_avg['time'] = pair_sep_df['time']

for columns in pair_sep_df.columns[1:9]:
    pair_1hour_avg[columns] = pair_sep_df[columns].rolling(24,center = True, min_periods=1).mean()


#%%

import hmac
import hashlib
import requests

DavisKey = 'pximklrj27gxockgwopjeqhs2d3bzhdv'
DavisSec = 'jztwkfbllckkczljsuit7fevl38ksjlc'
start_time = 1638298800
end_time = 1638385200
st_id = 126241

t = int(time.time())

message1 = 'api-key{}t{}'.format(DavisKey, t)
message2 = 'api-key{}end-timestamp{}start-timestamp{}station-id{}t{}'.format(DavisKey,end_time,start_time,st_id, t)
message3 = 'api-key{}station-id{}t{}'.format(DavisKey,st_id,t)
signature = hmac.new(bytes(DavisSec , 'latin-1'), msg = bytes(message3 , 'latin-1'),
                     digestmod = hashlib.sha256).hexdigest().upper()

url = "https://api.weatherlink.com/v2/stations?api-key={}&t={}&api-signature={}".format(DavisKey,t,signature)
url2 = "https://api.weatherlink.com/v2/historic/{}?api-key={}&t={}&start-timestamp={}&end-timestamp={}&api-signature={}".format(st_id,DavisKey,t,start_time,end_time,signature)
url3 = "https://api.weatherlink.com/v2/current/96230?api-key=987654321&t=1558729481&api-signature=c818f075283713f1a133c30e27984032e19ca6dd37c33160d1c8f1edbaa509e4"
session = requests.session()
r = session.get(url2)
if r.status_code == 200:
    print(r.text)
else:
    print("error")










