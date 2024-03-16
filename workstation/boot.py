#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random
import pandas as pd
import plotly.graph_objects as go

x = [71,68,66,67,70,71,70,73,72,65,66]
y = [69,64,65,63,65,62,65,64,66,59,62]
res=[]

for i in range(200):
    s1=[]
    s2=[]
    for i in range(11):
        a = random.randrange(11)
        s1.append(x[a])
        s2.append(y[a])
    s1 = pd.Series(s1)
    s2 = pd.Series(s2)
    res.append(s1.corr(s2))




fig = go.Figure(data=[
    go.Histogram(x=res, nbinsx=20),
])
fig.show()

