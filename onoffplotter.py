#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 15:27:42 2017

@author: ycan
"""
import os
import numpy as np
import matplotlib.pyplot as plt


main_dir = '/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/data/Experiments/Salamander/2014_01_21/analyzed/'

allfiles = os.listdir(main_dir)
stim_type = 3

files_f = []  # Full field flicker
files_c = []  # Checkerflicker

for i in allfiles:
    if i[-4:] == '.npz':
        if i[0] == str(2):
            files_f.append(i)
        elif i[0] == str(3):
            files_c.append(i)
onoffindices_f = np.array([])
onoffindices_c = np.array([])

filenames_f = []
filenames_c = []
for i in files_f:
    f = np.load(main_dir+i)
    onoffindices_f = np.append(onoffindices_f, f['onoffindex'])
    filenames_f.append(f['filename'])
for i in files_c:
    f = np.load(main_dir+i)
    onoffindices_c = np.append(onoffindices_c, f['onoffindex'])
    filenames_c.append(f['filename'])

# %%
plt.hist(onoffindices_f, bins=np.linspace(-1, 1, num=40), alpha=.6)
plt.hist(onoffindices_c, bins=np.linspace(-1, 1, num=40), alpha=.6)
plt.legend(['Full field', 'Checkerflicker'])
plt.title('Histogram of On Off indices')
plt.show()
plt.scatter(onoffindices_f, onoffindices_c)
plt.plot(np.linspace(-1, 1), np.linspace(-1, 1), '--')
plt.title('On-Off indices obtained from Full field vs Checkerflicker')
plt.ylabel('Checkerflicker')
plt.xlabel('Full field flicker')
plt.axis('square')
plt.show()
