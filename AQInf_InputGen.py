# -*- coding: utf-8 -*-
"""
Created on Fri Feb 11 13:12:41 2022

@author: AbdurRahman
"""
###### env: aqinf
import pandas
import numpy as np
import math
import geopandas as gpd
import json

combined_df = pandas.read_csv('combined_daily_data.csv')
combined_df['time'] = pandas.to_datetime(combined_df['time'])
combined_df = combined_df.set_index('time')
combined_df = combined_df.rename(columns = {'PurpleAir-0': 'PAir-GardenTown', 'PurpleAir-2': 'PAir-DefenceChowk',
                              'PurpleAir-4': 'PAir-IqbalTown', 'PurpleAir-6': 'PAir-AkbarChowk',
                              'PurpleAir-8': 'PAir-Township', 'PurpleAir-10': 'PAir-DHAPhase2',
                              'PurpleAir-12': 'PAir-Anarkali', 'PurpleAir-14': 'PAir-Harbanspura'})


labeled_nodes_id = [221,184,292,224,189,192,261,281,173,280]
labeled_nodes_aqi = [227,274,248,91,284,285,258,368,207,268]    
labeled_nodes_id, labeled_nodes_aqi = zip(*sorted(zip(labeled_nodes_id, labeled_nodes_aqi)))


nodes_df = gpd.read_file('nodes_hsp2.geojson')


with open('unlabeledList', 'w') as f:
    for item in nodes_df['id']:
        if not item in labeled_nodes_id:
            f.write("%s\n" % int(item))
            
with open('labeledList', 'w') as f:
    for item in nodes_df['id']:
        if item in labeled_nodes_id:
            f.write("%s\n" % int(item))

with open('labeledAQITable', 'w') as f:
    for item in nodes_df['id']:
        if item in labeled_nodes_id:
            f.write("%s\n" % int(labeled_nodes_aqi[labeled_nodes_id.index(int(item))]))
    
x_list = sorted(nodes_df.geometry.x.unique())
y_list = sorted(nodes_df.geometry.y.unique())

nodes_df['row'] = x_list.index(nodes_df.geometry.x)

nodes_df['row'] = nodes_df.apply(lambda row : x_list.index(row.geometry.x), axis = 1)
nodes_df['col'] = nodes_df.apply(lambda row : y_list.index(row.geometry.y), axis = 1)


nodes_df.set_index('id', inplace = True)

labeled_feature_df = pandas.DataFrame(columns = ['rowCol', 'traffic_spot', 'industry', 'commercial', 'nala'],index = labeled_nodes_id)



for ind in nodes_df.index:
    if ind in labeled_nodes_id:
        print("({}, {})".format(nodes_df['row'][ind],nodes_df['col'][ind]))
        labeled_feature_df['rowCol'][ind] = "({}, {})".format(nodes_df['row'][ind],nodes_df['col'][ind])
        labeled_feature_df['industry'][ind] = nodes_df['industry_interp'][ind]
        labeled_feature_df['traffic_spot'][ind] = nodes_df['hotspot_interp'][ind]
        labeled_feature_df['commercial'][ind] = nodes_df['commercial_interp'][ind]
        labeled_feature_df['nala'][ind] = nodes_df['nala_interp'][ind]

labeled_feature_df.to_csv("labeledFeatureTimestampPanel.csv")

#%%

unlabeled_nodes_id = []
for ind in nodes_df.index:
    if not ind in labeled_nodes_id:
        unlabeled_nodes_id.append(ind)

unlabeled_feature_df = pandas.DataFrame(columns = ['rowCol', 'traffic_spot',
                                                 'industry', 'commercial', 'nala']
                                      ,index = unlabeled_nodes_id)

for ind in nodes_df.index:
    if not ind in labeled_nodes_id:
        print("({}, {})".format(nodes_df['row'][ind],nodes_df['col'][ind]))
        unlabeled_feature_df['rowCol'][ind] = "({}, {})".format(nodes_df['row'][ind],nodes_df['col'][ind])
        unlabeled_feature_df['industry'][ind] = nodes_df['industry_interp'][ind]
        unlabeled_feature_df['traffic_spot'][ind] = nodes_df['hotspot_interp'][ind]
        unlabeled_feature_df['commercial'][ind] = nodes_df['commercial_interp'][ind]
        unlabeled_feature_df['nala'][ind] = nodes_df['nala_interp'][ind]

unlabeled_feature_df.to_csv("unlabeledFeatureTimestampPanel.csv")

with open('featureList', 'w') as f:
    for item in labeled_feature_df.columns:
        f.write("%s\n" % item)


#%%


pandas.read_csv('')




