# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 16:36:15 2022

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

from analysis_functions import *


#%%

combined_df = pandas.read_csv('combined_daily_data.csv')
combined_df['time'] = pandas.to_datetime(combined_df['time'])
combined_df = combined_df.set_index('time')

combinedAQI_df = pandas.read_csv('combinedAQI.csv')
combinedAQI_df['time'] = pandas.to_datetime(combinedAQI_df['time'])
combinedAQI_df = combinedAQI_df.set_index('time')

combinedAQIBand_df = pandas.read_csv('combinedAQIBand.csv')
combinedAQIBand_df['time'] = pandas.to_datetime(combinedAQIBand_df['time'])
combinedAQIBand_df = combinedAQIBand_df.set_index('time')

#%%

mae_compute(combinedAQI_df)





































