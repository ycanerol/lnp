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
LR3 Gollisch/data/Experiments/Mouse/'

all_experiments = os.listdir(main_dir)[1:]

for experiment in all_experiments:

    w_dir = '/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/data/Experiments/Mouse/'+experiment+'/analyzed/'

    exp_name = w_dir.split('/')[-4]+'_'+w_dir.split('/')[-3]

    allfiles = os.listdir(w_dir)

    files_f = []  # Full field flicker
    files_c = []  # Checkerflicker

    for i in allfiles:
        if i[-4:] == '.npz':
            if i[0] == str(3):
                files_f.append(i)
            elif i[0] == str(2):
                files_c.append(i)
    onoffindices_f = np.array([])
    onoffindices_c = np.array([])
    onoffindices_o = np.array([])

    spikenr_f = np.array([])
    spikenr_c = np.array([])

    filenames_f = []
    filenames_c = []

    exclude_spike_limit = 200
    excluded_f = 0
    excluded_c = 0

    for index, i in enumerate(files_f):
        f = np.load(w_dir+i)
        spikenr_f = np.append(spikenr_f, f['total_spikes'])
        if spikenr_f[-1] < exclude_spike_limit:
            spikenr_f = spikenr_f[:-1]
            excluded_f += 1
            continue
        if np.isnan(f['ooi_dimos']):
            continue
        onoffindices_f = np.append(onoffindices_f, f['onoffindex'])
        onoffindices_o = np.append(onoffindices_o, f['ooi_dimos'])
        filenames_f.append(str(f['filename']))

    for i in files_c:
        f = np.load(w_dir+i)
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
    onoffindicesc_o = np.array([])
    filenamesc_c = []
    spikenrc_c = np.array([])
    onoffindicesc_c = np.array([])

    for i in range(len(filenames_f)):
        if filenames_f[i] in filenames_c:
            filenamesc_f.append(filenames_f[i])
            spikenrc_f = np.append(spikenrc_f, spikenr_f[i])
            onoffindicesc_f = np.append(onoffindicesc_f, onoffindices_f[i])
            onoffindicesc_o = np.append(onoffindicesc_o, onoffindices_o[i])
    for i in range(len(filenames_c)):
        if filenames_c[i] in filenames_f:
            filenamesc_c.append(filenames_c[i])
            spikenrc_c = np.append(spikenrc_c, spikenr_c[i])
            onoffindicesc_c = np.append(onoffindicesc_c, onoffindices_c[i])

    spikenr_f = spikenrc_f
    onoffindices_f = onoffindicesc_f
    onoffindices_o = onoffindicesc_o
    spikenr_c = spikenrc_c
    onoffindices_c = onoffindicesc_c

    outliers = np.where(np.abs(onoffindices_c - onoffindices_f) > .6)[0]

    r_cf = np.corrcoef(onoffindices_c, onoffindices_f)[1, 0]
    r_of = np.corrcoef(onoffindices_o, onoffindices_f)[1, 0]
    r_co = np.corrcoef(onoffindices_c, onoffindices_o)[1, 0]

    axis_limits = [-1.1, 1.1, -1.1, 1.1]

    # %%
    plt.figure(figsize=(10, 10), dpi=200)
    plt.suptitle(exp_name)

    plt.subplot(2, 2, 1)
    plt.hist(onoffindices_f, bins=np.linspace(-1, 1, num=40), alpha=.5)
    plt.hist(onoffindices_c, bins=np.linspace(-1, 1, num=40), alpha=.5)
    plt.hist(onoffindices_o, bins=np.linspace(-1, 1, num=40), alpha=.5)
    plt.legend(['Full field', 'Checkerflicker', 'On off steps'])
    plt.title('Histogram of On Off indices')
    plt.xlabel('On-off index')
    plt.ylabel('Frequency')

    plt.subplot(2, 2, 2)
    plt.scatter(onoffindices_f, onoffindices_c)
    plt.plot(onoffindices_f[outliers], onoffindices_c[outliers], 'r.')
    plt.plot(np.linspace(-1, 1), np.linspace(-1, 1), '--', alpha=.4)
    plt.text(.7, -1.05, 'R = {:4.2}'.format(r_cf))
    plt.axis(axis_limits)
    for i in outliers:
        plt.text(onoffindices_f[i], onoffindices_c[i], filenamesc_c[i])
    plt.title('On-Off indices obtained from Full field vs Checkerflicker')
    plt.ylabel('Checkerflicker')
    plt.xlabel('Full field flicker')
   
    plt.subplot(2, 2, 3)
    plt.scatter(onoffindices_f, onoffindices_o)
    plt.text(.7, -1.05, 'R = {:4.2}'.format(r_of))
    plt.plot(np.linspace(-1, 1), np.linspace(-1, 1), '--', alpha = .4)
    plt.axis(axis_limits)
    plt.title('fff vs on off steps')
    plt.xlabel('full field flicker')
    plt.ylabel('on off steps')

    plt.subplot(2, 2, 4)
    plt.scatter(onoffindices_c, onoffindices_o)
    plt.text(.7, -1.05, 'R = {:4.2}'.format(r_co))
    plt.plot(np.linspace(-1, 1), np.linspace(-1, 1), '--', alpha = .4)
    plt.axis(axis_limits)
    plt.title('checkerflicker vs on off steps')
    plt.xlabel('checkerflicker')
    plt.ylabel('on off steps')

    plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    plt.savefig('/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/figures/{}'.format(exp_name), dpi=200)