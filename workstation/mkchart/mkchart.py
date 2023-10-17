#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 10 20:33:49 2023

@author: kenta
"""

from bokeh.plotting import show,figure
from bokeh.models import Range1d, SingleIntervalTicker
 
# prepare some data
x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]
 
# create a new plot with a title and axis labels
p = figure(x_axis_label='x', y_axis_label='y', title='Linear vs. Quadratic',x_range=[0,15])
 
# add a line renderer with legend and line thickness to the plot
x_line=p.line(x, y, line_width=2, legend_label='うんち')
p.circle(x, y, color='blue', line_width=5)
p.line(y, y, line_width=2, legend_label='linear')
p.cross(y, y, color='red', line_width=15)

#p.y_range.renderers = [x_line] 
p.xaxis.ticker = SingleIntervalTicker(interval=1)
p.y_range= Range1d(0, 15)


# show the results
show(p)
