# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 15:29:59 2022

@author: AbdurRahman
"""

import pandas
import matplotlib.pyplot as plt
import numpy as np
from analysis_functions import *
from plotly.offline import plot
import math
import geopandas





sensormap_dict = {
    'Met Station' : [31.542565189837347, 74.32466701123708],
    'EPD Gulberg' : [31.511579422313474, 74.33832152415287],
    'Dental College' : [31.580127144483225, 74.46372822774073],
    'US-Embassy' : [31.559984433931433, 74.33607681104723],
    'SDSA LUMS' : [31.46954844925869, 74.40724558003234],
    'PAir-GardenTown' : [31.501559, 74.306762],
    'PAir-DefenceChowk' : [31.4859, 74.3735],
    'PAir-IqbalTown' : [31.510158, 74.284233],
    'PAir-AkbarChowk' : [31.468374, 74.301385],
    'PAir-Township' : [31.444512, 74.309754],
    'PAir-DHAPhase2' : [31.480284, 74.404699],
    'PAir-Anarkali' : [31.565131, 74.310783],
    'PAir-Harbanspura' : [31.570236, 74.412914]
    }

sensormap_df = pandas.DataFrame(columns = ['location', 'lat', 'long'])
sensormap_df['location'] = list(sensormap_dict.keys())

for i in range(len(list(sensormap_dict.keys()))):
    sensormap_df.iloc[i]['lat'] = sensormap_dict[list(sensormap_dict.keys())[i]][0]
    sensormap_df.iloc[i]['long'] = sensormap_dict[list(sensormap_dict.keys())[i]][1]
    
sensormap_df['type'] = 'Low-Cost'

gdf = geopandas.GeoDataFrame(
    sensormap_df[['location', 'type']], geometry=geopandas.points_from_xy(sensormap_df.long, sensormap_df.lat))

del i

#%%
gdf.to_file("SensorMap.geojson",driver="GeoJSON")

#%% not used
credits = 'Static Congestion Map for Lahore using Google Directions API'

fig, ax = plt.subplots(figsize=(14,10))
    
p = gdf.plot(ax=ax, column = gdf['type'])

 

p.axes.get_xaxis().set_visible(False)

p.axes.get_yaxis().set_visible(False)

ax.get_legend().set_bbox_to_anchor((1.5,1))

ctx.add_basemap(ax=ax, source=ctx.providers.OpenStreetMap.Mapnik, attribution=credits)

 

 

plt.savefig('Static Congestions.png',dpi=500)

 

gpd_static = gpd_static.to_crs(epsg=32643) #if reprojecting to QGIS