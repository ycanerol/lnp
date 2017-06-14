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

exp_name = main_dir.split('/')[-4]+'_'+main_dir.split('/')[-3]

allfiles = os.listdir(main_dir)

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

spikenr_f = np.array([])
spikenr_c = np.array([])

filenames_f = []
filenames_c = []

exclude_spike_limit = 200
excluded_f = 0
excluded_c = 0

for i in files_f:
    f = np.load(main_dir+i)
    spikenr_f = np.append(spikenr_f, f['total_spikes'])
    if spikenr_f[-1] < exclude_spike_limit:
        spikenr_f = spikenr_f[:-1]
        excluded_f += 1
        continue
    onoffindices_f = np.append(onoffindices_f, f['onoffindex'])
    filenames_f.append(str(f['filename']))

for i in files_c:
    f = np.load(main_dir+i)
    spikenr_c = np.append(spikenr_c, f['total_spikes'])
    if spikenr_c[-1] < exclude_spike_limit:
        spikenr_c = spikenr_c[:-1]
        excluded_c += 1
        continue
    onoffindices_c = np.append(onoffindices_c, f['onoffindex'])
    filenames_c.append(str(f['filename']))
# %% Only get cells that are in both sets
filenamesc_f = []
spikenrc_f = np.array([])
onoffindicesc_f = np.array([])
filenamesc_c = []
spikenrc_c = np.array([])
onoffindicesc_c = np.array([])

for i in range(len(filenames_f)):
    if filenames_f[i] in filenames_c:
        filenamesc_f.append(filenames_f[i])
        spikenrc_f = np.append(spikenrc_f, spikenr_f[i])
        onoffindicesc_f = np.append(onoffindicesc_f, onoffindices_f[i])
for i in range(len(filenames_c)):
    if filenames_c[i] in filenames_f:
        filenamesc_c.append(filenames_c[i])
        spikenrc_c = np.append(spikenrc_c, spikenr_c[i])
        onoffindicesc_c = np.append(onoffindicesc_c, onoffindices_c[i])

spikenr_f = spikenrc_f
onoffindices_f = onoffindicesc_f
spikenr_c = spikenrc_c
onoffindices_c = onoffindicesc_c

# %%
plt.figure(figsize=(8, 16), dpi=200)

plt.subplot(2, 1, 2)
plt.hist(onoffindices_f, bins=np.linspace(-1, 1, num=40), alpha=.6)
plt.hist(onoffindices_c, bins=np.linspace(-1, 1, num=40), alpha=.6)
plt.legend(['Full field', 'Checkerflicker'])
plt.title('Histogram of On Off indices \n{}'.format(exp_name))
plt.xlabel('On-off index')
plt.ylabel('Frequency')

plt.subplot(2, 1, 1)
plt.scatter(onoffindices_f, onoffindices_c)
plt.plot(onoffindices_f[outliers], onoffindices_c[outliers], 'r.')
plt.plot(np.linspace(-1, 1), np.linspace(-1, 1), '--')
for i in outliers:
    plt.text(onoffindices_f[i], onoffindices_c[i], filenamesc_c[i])
plt.title('On-Off indices obtained from Full field vs Checkerflicker\n{}'
          .format(exp_name))
plt.ylabel('Checkerflicker')
plt.xlabel('Full field flicker')
plt.axis('square')

plt.tight_layout()
plt.savefig('/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/figures/{}'.format(exp_name)
            , dpi=200)
plt.show()

for i in outliers:
    print('{:5s} change {:>5.2f} to {:>5.2f}'
          .format(filenamesc_c[i], onoffindices_f[i], onoffindices_c[i]))
