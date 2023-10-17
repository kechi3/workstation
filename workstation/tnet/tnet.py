#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 20:54:19 2023

@author: kenta
"""

import schemdraw
import schemdraw.elements as elm
import pandas as pd
from tkinter import filedialog
import os


def read_csv():
    typ = [('CSVファイル','*.csv')] 
    dir = os.getcwd()
    fle = filedialog.askopenfilename(filetypes = typ, initialdir = dir) 
    result = pd.read_csv(fle)
    return result

def w_net(nlist):
    with schemdraw.Drawing() as d:
        for i in range(len(nlist)):
            if nlist.loc[i,'address'] == "v":
                d += elm.Resistor().up()
            elif nlist.loc[i,'address'] == "h":
                d += elm.Resistor().right()

schemdraw.theme('monokai')

data = read_csv()
w_net(data)


        
