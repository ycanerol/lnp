#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 16:55:59 2017

@author: ycan

Figure plotter
"""

import numpy as np
import matplotlib.pyplot as plt


plotthis = [['2017_02_14', '901', 'On cell'],
            ['2017_01_17', '201', 'Off cell']]

for i in plotthis:

    main_dir = '/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/data/Experiments/Mouse/'
    
    currentfile_c = main_dir + i[0] +\
                     '/analyzed/2_SP_C' + i[1] + '.npz'
    currentfile_f = main_dir + i[0] +\
                     '/analyzed/3_SP_C' + i[1] + '.npz'
    
    
    c = np.load(str(currentfile_c))
    f = np.load(str(currentfile_f))
