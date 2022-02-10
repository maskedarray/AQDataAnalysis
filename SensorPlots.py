# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 11:30:43 2022

@author: AbdurRahman
"""


import pandas
import matplotlib.pyplot as plt
import numpy as np
from analysis_functions import *
from plotly.offline import plot
import plotly.graph_objects as go
import math
import geopandas


combined_df = pandas.read_csv('combined_daily_data.csv')
combined_df['time'] = pandas.to_datetime(combined_df['time'])
combined_df = combined_df.set_index('time')

combinedAQI_df = pandas.read_csv('combinedAQI.csv')
combinedAQI_df['time'] = pandas.to_datetime(combinedAQI_df['time'])
combinedAQI_df = combinedAQI_df.set_index('time')

combinedAQIBand_df = pandas.read_csv('combinedAQIBand.csv')
combinedAQIBand_df['time'] = pandas.to_datetime(combinedAQIBand_df['time'])
combinedAQIBand_df = combinedAQIBand_df.set_index('time')

combined_df = combined_df.rename(columns = {'PurpleAir-0': 'PAir-GardenTown', 'PurpleAir-2': 'PAir-DefenceChowk',
                              'PurpleAir-4': 'PAir-IqbalTown', 'PurpleAir-6': 'PAir-AkbarChowk',
                              'PurpleAir-8': 'PAir-Township', 'PurpleAir-10': 'PAir-DHAPhase2',
                              'PurpleAir-12': 'PAir-Anarkali', 'PurpleAir-14': 'PAir-Harbanspura'})

#%%

df = combined_df
df.reset_index(inplace = True)
df.drop(columns = ['Green Town', 'Wagha Town'], inplace = True)

#%% Reference big plot

fig = go.Figure()
fig.add_trace(go.Scatter(x = df['time'], y = df['US-Embassy'], mode = 'lines',
                         name = 'US-Embassy', connectgaps = False))
fig.add_trace(go.Scatter(x = df['time'], y = df['Met Station'], mode = 'lines',
                         name = 'Met Station', connectgaps = False, line = dict(dash = '1px')))
fig.add_trace(go.Scatter(x = df['time'], y = df['Dental College'], mode = 'lines',
                         name = 'Dental College', connectgaps = False, line = dict(dash = '2px')))
fig.add_trace(go.Scatter(x = df['time'], y = df['EPA Gulberg'], mode = 'lines',
                         name = 'EPA Gulberg', connectgaps = False, line = dict(dash = '6px,2px', color = 'rgb(255, 165, 0)')))

fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
fig.update_xaxes(title = "Time", showline=True, linewidth=2, linecolor='black', mirror=True)
fig.update_yaxes(title = 'PM2.5 Conc (ug/m3)', showline=True, linewidth=2, linecolor='black', mirror=True)


plot(fig, filename = "Reference Main Sensors.html")


#%% Reference small plots 1

reference_names = ['US-Embassy', 'Met Station', 'EPA Gulberg', 'Dental College']

for i in range(len(reference_names)):
    
    for j in range(len(reference_names)):
        fig = go.Figure()
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
        fig.update_xaxes(title = "Time", showline=True, linewidth=2, linecolor='black', mirror=True)
        fig.update_yaxes(title = 'PM2.5 Conc (ug/m3)', showline=True, linewidth=2, linecolor='black', mirror=True)
        
        
        fig.add_trace(go.Scatter(x = df['time'], y = df[reference_names[i]], mode = 'lines',
                                 name =reference_names[i], connectgaps = False))
        fig.add_trace(go.Scatter(x = df['time'], y = df[reference_names[j]], mode = 'lines',
                                 name = reference_names[j], connectgaps = False, line = dict(dash = '1px')))
        plot(fig, filename = 'temp-plot{}.html'.format((i+1)*(j+1)))

#%% Reference small plots 2
fig = go.Figure()
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
fig.update_xaxes(title = "Time", showline=True, linewidth=2, linecolor='black', mirror=True)
fig.update_yaxes(title = 'PM2.5 Conc (ug/m3)', showline=True, linewidth=2, linecolor='black', mirror=True)


fig.add_trace(go.Scatter(x = df['time'], y = df['US-Embassy'], mode = 'lines',
                         name = 'US-Embassy', connectgaps = False))
fig.add_trace(go.Scatter(x = df['time'], y = df['Dental College'], mode = 'lines',
                         name = 'Dental College', connectgaps = False, line = dict(dash = '2px')))
plot(fig, filename = "Low Cost 2.html")

#%% Reference small plots 3
fig = go.Figure()
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
fig.update_xaxes(title = "Time", showline=True, linewidth=2, linecolor='black', mirror=True)
fig.update_yaxes(title = 'PM2.5 Conc (ug/m3)', showline=True, linewidth=2, linecolor='black', mirror=True)


fig.add_trace(go.Scatter(x = df['time'], y = df['US-Embassy'], mode = 'lines',
                         name = 'US-Embassy', connectgaps = False))
fig.add_trace(go.Scatter(x = df['time'], y = df['EPA Gulberg'], mode = 'lines',
                         name = 'EPA Gulberg', connectgaps = False, line = dict(dash = '6px,2px', color = 'rgb(255, 165, 0)')))
plot(fig, filename = "Low Cost 3.html")

#%% Low-Cost main plot

fig = go.Figure()
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
fig.update_xaxes(title = "Time", showline=True, linewidth=2, linecolor='black', mirror=True,
                 range = ['2021-08-01', '2022-01-20'])
fig.update_yaxes(title = 'PM2.5 Conc (ug/m3)', showline=True, linewidth=2, linecolor='black', mirror=True)


for columns in df.columns[3:11]:
    
    if columns  == 'PAir-AkbarChowk':
        fig.add_trace(go.Scatter(x = df['time'], y = df[columns], 
                                mode = 'lines', name = columns, line = dict(dash = '6px,2px'))) 
    elif columns == 'PAir-Harbanspura':
        fig.add_trace(go.Scatter(x = df['time'], y = df[columns], 
                                mode = 'lines', name = columns, line = dict(dash = '10px,4px')))
    else:
        fig.add_trace(go.Scatter(x = df['time'], y = df[columns], 
                             mode = 'lines', name = columns))

plot(fig, filename = "Low Cost Main Sensors.html")

#%% Low Cost vs Reference Plot

#compute error bands
y_upper = []
y_lower = []

low_cost_df = df.drop(columns = ['US-Embassy', 'EPA Gulberg', 'Met Station',
                                 'Dental College', 'time'])
df['y_upper'] = low_cost_df.max(axis = 1)
df['y_lower'] = low_cost_df.min(axis = 1)
df['y_avg'] = df[['y_upper', 'y_lower']].mean(axis = 1)

fig = go.Figure()
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
fig.update_xaxes(title = "Time", showline=True, linewidth=2, linecolor='black', mirror=True,
                 range = ['2021-08-01', '2022-01-20'])
fig.update_yaxes(title = 'PM2.5 Conc (ug/m3)', showline=True, linewidth=2, linecolor='black', mirror=True)

fig.add_trace(go.Scatter(x = df['time'], y = df['US-Embassy'], mode = 'lines+markers',
                         name = 'US-Embassy', connectgaps = False,
                         line = dict(color = 'rgba(0, 0, 255, 1)')))
fig.add_trace(go.Scatter(x = df['time'], y = df['EPA Gulberg'], mode = 'lines+markers',
                         name = 'EPA Gulberg', connectgaps = False,
                         line = dict(color = 'rgba(255, 0, 0, 1)')))

# fig.add_trace(go.Scatter(x = df['time'], y = df['y_avg'], mode = 'lines',
#                          name = 'US-Embassy', connectgaps = False, line=dict(color = 'rgba(255, 165, 0, 1)')))

fig.add_trace(go.Scatter(
    x= pandas.concat([df['time'] , df['time'][::-1]]), 
    y=  pandas.concat([df['y_upper'] , df['y_lower'][::-1]]), 
    fill='toself', fillcolor='rgba(255, 165, 0, 0.2)',
    line=dict(color = 'rgba(104, 175, 168, 0.4)'), hoverinfo="skip", 
    name = 'Low-Cost Sensors',showlegend=True))
          

plot(fig, filename = "Low Cost v Reference Main.html")

#%%

#compute error bands
y_upper = []
y_lower = []

low_cost_df = df.drop(columns = ['US-Embassy', 'EPA Gulberg', 'Met Station',
                                 'Dental College', 'time'])
df['y_upper'] = low_cost_df.max(axis = 1)
df['y_lower'] = low_cost_df.min(axis = 1)
df['y_avg'] = df[['y_upper', 'y_lower']].mean(axis = 1)

fig = go.Figure()
fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)')
fig.update_xaxes(title = "Time", showline=True, linewidth=2, linecolor='black', mirror=True,
                 range = ['2021-08-01', '2022-01-20'])
fig.update_yaxes(title = 'PM2.5 Conc (ug/m3)', showline=True, linewidth=2, linecolor='black', mirror=True)


layout = {
    # to highlight the timestamp we use shapes and create a rectangular
    'shapes': [
        # 1st highlight during Feb 4 - Feb 6
        {
            'type': 'rect',
            # x-reference is assigned to the x-values
            'xref': 'x',
            # y-reference is assigned to the plot paper [0,1]
            'yref': 'paper',
            'x0': '2021-11-29',
            'y0': 0,
            'x1': '2022-01-06',
            'y1': 1,
            'fillcolor': '#FEC94C',
            'opacity': 0.2,
            'line': {
                'width': 0,
            }
        },
        {
            'type': 'rect',
            'xref': 'x',
            'yref': 'paper',
            'x0': '2021-12-23',
            'y0': 0,
            'x1': '2022-01-06',
            'y1': 1,
            'fillcolor': '#FF429E',
            'opacity': 0.2,
            'line': {
                'width': 0,
            }
        }
        ]
    }
fig.update_layout(layout)

fig.add_trace(go.Scatter(x = df['time'], y = df['US-Embassy'], mode = 'lines+markers',
                         name = 'US-Embassy', connectgaps = False,
                         line = dict(color = '#004DFF')))
fig.add_trace(go.Scatter(x = df['time'], y = df['EPA Gulberg'], mode = 'lines+markers',
                         name = 'EPA Gulberg', connectgaps = False,
                         line = dict(color = '#ED0013')))

# fig.add_trace(go.Scatter(x = df['time'], y = df['y_avg'], mode = 'lines',
#                          name = 'US-Embassy', connectgaps = False, line=dict(color = 'rgba(255, 165, 0, 1)')))

# fig.add_trace(go.Scatter(
#     x= pandas.concat([df['time'] , df['time'][::-1]]), 
#     y=  pandas.concat([df['y_upper'] , df['y_lower'][::-1]]), 
#     fill='toself', fillcolor='rgba(235, 59, 120, 0.2)',
#     line=dict(color = 'rgba(104, 175, 168, 0.4)'), hoverinfo="skip",line_shape='spline',
#     name = 'Low-Cost Sensors',showlegend=True))

fig.add_trace(go.Bar( x = df['time'], y = df['y_upper'], base = df['y_lower'],
                     marker = dict(color = 'rgba(182, 178, 215, 0.8)'), showlegend = False))
          


plot(fig, filename = "Low Cost v Reference Main 2.html")




#%%








