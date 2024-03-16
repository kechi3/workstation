#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 20:33:49 2023

@author: kenta
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np

data = pd.read_csv("Sheet1.csv")

bar_x = sum(data["myhome"])/len(data["myhome"])
bar_y = sum(data["jimin"])/len(data["jimin"])

Sx = data["myhome"]-bar_x 
Sy = data["jimin"]-bar_y 

sum_Sx = sum(np.square(Sx))
sum_Sy = sum(np.square(Sy))

r = sum(Sx * Sy)/(np.sqrt(sum_Sx)*np.sqrt(sum_Sy))

print(sum_Sx)
print(sum_Sy)
print(r)


fig = go.Figure(data=[
    go.Scatter(x=data["myhome"], y=data["jimin"], name="sin",mode='markers'),
])
#fig.show()

