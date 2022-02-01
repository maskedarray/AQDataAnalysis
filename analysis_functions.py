# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 16:38:19 2022

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