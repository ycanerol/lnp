#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  6 15:27:42 2017

@author: ycan
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

main_dir = '/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/data/Experiments/Mouse/'

all_experiments = os.listdir(main_dir)[1:]

all_o = np.array([])
all_f = np.array([])
all_c = np.array([])
dataset_sizes = np.array([])

for experiment in all_experiments:
#%%
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
    onoffindices_o = np.array([])
    onoffindices_f = np.array([])
    onoffindices_c = np.array([])

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
    spikenr_c = spikenrc_c
    onoffindices_f = onoffindicesc_f
    onoffindices_o = onoffindicesc_o
    onoffindices_c = onoffindicesc_c

    outliers_cf = np.where(np.abs(onoffindices_c - onoffindices_f) > .6)[0]
    outliers_of = np.where(np.abs(onoffindices_o - onoffindices_f) > .6)[0]
    outliers_co = np.where(np.abs(onoffindices_c - onoffindices_o) > .6)[0]

    r_cf = np.corrcoef(onoffindices_c, onoffindices_f)[1, 0]
    r_of = np.corrcoef(onoffindices_o, onoffindices_f)[1, 0]
    r_co = np.corrcoef(onoffindices_c, onoffindices_o)[1, 0]

    axis_limits = [-1.1, 1.1, -1.1, 1.1]
    ticks = [-1, -.5, 0, .5, 1]

    matplotlib.rcParams['axes.spines.right'] = False
    matplotlib.rcParams['axes.spines.top'] = False

    # %%
    plt.figure(figsize=(10, 10), dpi=200)
    plt.suptitle(exp_name)

    plt.subplot(6, 2, 1)
    plt.hist(onoffindices_f, bins=np.linspace(-1, 1, num=40),
             alpha=.5, color='C0')
    plt.xticks(ticks)
    plt.ylabel('FFF')
    plt.subplot(6, 2, 3)
    plt.ylabel('Checker')
    plt.hist(onoffindices_c, bins=np.linspace(-1, 1, num=40),
             alpha=.5, color='C1')
    plt.xticks(ticks)
    plt.subplot(6, 2, 5)
    plt.ylabel('On off steps')
    plt.hist(onoffindices_o, bins=np.linspace(-1, 1, num=40),
             alpha=.5, color='C2')
    plt.xticks(ticks)
    plt.xlabel('On-off index')
    plt.subplots_adjust(hspace=0)

    plt.subplot(2, 2, 2)
    plt.plot(onoffindices_f, onoffindices_c, '.')
    plt.plot(onoffindices_f[outliers_cf], onoffindices_c[outliers_cf],
             'r.', markersize=3)
    plt.plot(np.linspace(-1, 1), np.linspace(-1, 1), '--', alpha=.4)
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.text(.7, -1.05, 'R = {:4.2}'.format(r_cf))
    plt.axis(axis_limits)
    plt.axis('square')
    for i in outliers_cf:
        plt.text(onoffindices_f[i], onoffindices_c[i],
                 filenamesc_c[i], fontsize=8)
    plt.title('On-Off indices obtained from Full field vs Checkerflicker')
    plt.ylabel('Checkerflicker')
    plt.xlabel('Full field flicker')

    plt.subplot(2, 2, 3)
    plt.plot(onoffindices_f, onoffindices_o, '.')
    plt.plot(onoffindices_f[outliers_of], onoffindices_o[outliers_of],
             'r.', markersize=3)
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.text(.7, -1.05, 'R = {:4.2}'.format(r_of))
    plt.plot(np.linspace(-1, 1), np.linspace(-1, 1), '--', alpha=.4)
    plt.axis(axis_limits)
    plt.axis('square')
    for i in outliers_of:
        plt.text(onoffindices_f[i], onoffindices_o[i],
                 filenamesc_f[i], fontsize=8)
    plt.title('FFF vs On off steps')
    plt.xlabel('Full field flicker')
    plt.ylabel('On off steps')

    plt.subplot(2, 2, 4)
    plt.plot(onoffindices_c, onoffindices_o, '.')
    plt.plot(onoffindices_c[outliers_co], onoffindices_o[outliers_co],
             'r.', markersize=3)
    plt.xticks(ticks)
    plt.yticks(ticks)
    plt.text(.7, -1.05, 'R = {:4.2}'.format(r_co))
    plt.plot(np.linspace(-1, 1), np.linspace(-1, 1), '--', alpha=.4)
    plt.axis(axis_limits)
    plt.axis('square')
    for i in outliers_co:
        plt.text(onoffindices_c[i], onoffindices_o[i],
                 filenamesc_f[i], fontsize=8)
    plt.title('Checkerflicker vs On off steps')
    plt.xlabel('Checkerflicker')
    plt.ylabel('On off steps')

    plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    plt.savefig('/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/figures/{}'.format(exp_name), dpi=200)

    all_o = np.append(all_o, onoffindices_o)
    all_f = np.append(all_f, onoffindices_f)
    all_c = np.append(all_c, onoffindices_c)
    dataset_sizes = np.append(dataset_sizes, onoffindices_o.size).astype(int)

np.savez('/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/data/Experiments/Mouse/2017_02_14/allindices.npz',
         all_o=all_o,
         all_f=all_f,
         all_c=all_c,
         dataset_sizes=dataset_sizes)

# %%
exp_name = 'all_experiments'

hist_axis_limits = [-1, 1, 0, 30]
r_fontsize=14

w_pf = np.sum(dataset_sizes[:2])  # Index at which data with preframes start

# Divide experiments into two, without and with preframes
o_npf, o_pf = all_o[:w_pf], all_o[w_pf:]
f_npf, f_pf = all_f[:w_pf], all_f[w_pf:]
c_npf, c_pf = all_c[:w_pf], all_c[w_pf:]

# Correlation coefficients for all pairs
r_cf = np.corrcoef(all_c, all_f)[1, 0]
r_of = np.corrcoef(all_o, all_f)[1, 0]
r_co = np.corrcoef(all_c, all_o)[1, 0]

# Correlation coefficients separate for w/ and w/o preframes
r_of_pf = np.corrcoef(o_pf, f_pf)[1, 0]
r_of_npf = np.corrcoef(o_npf, f_npf)[1, 0]
r_co_pf = np.corrcoef(o_pf, c_pf)[1, 0]
r_co_npf = np.corrcoef(o_npf, c_npf)[1, 0]

plt.figure(figsize=(10, 10), dpi=200)
#plt.suptitle(exp_name)

plt.subplot(6, 2, 1)
plt.title('Distribution of on-off indices')
plt.hist(all_f, bins=np.linspace(-1, 1, num=40),
         alpha=.5, color='C0')
plt.xticks(ticks)
plt.axis(hist_axis_limits)
plt.ylabel('FFF')
plt.subplot(6, 2, 3)
plt.ylabel('Checker')
plt.hist(all_c, bins=np.linspace(-1, 1, num=40),
         alpha=.5, color='C1')
plt.xticks(ticks)
plt.axis(hist_axis_limits)
plt.subplot(6, 2, 5)
plt.ylabel('On-off steps')
plt.hist(all_o, bins=np.linspace(-1, 1, num=40),
         alpha=.5, color='C2')
plt.xticks(ticks)
plt.axis(hist_axis_limits)
plt.xlabel('On-off index')
plt.subplots_adjust(hspace=.4)

plt.subplot(2, 2, 2)
plt.plot(np.linspace(-1, 1), np.linspace(-1, 1), '--', alpha=.4, color='black')
plt.axvline(0, linestyle='dashed', alpha=.2, color='gray')
plt.axhline(0, linestyle='dashed', alpha=.2, color='gray')
plt.plot(all_f, all_c, '.', alpha=.5)
plt.text(1, -1.05, 'r = {:4.2}'.format(r_cf), fontsize=r_fontsize,
         horizontalalignment='right')
plt.axis(axis_limits)
plt.axis('square')
plt.xticks(ticks)
plt.yticks(ticks)
plt.title('On-off indices obtained from\nFull field vs Checkerflicker')
plt.ylabel('Checkerflicker')
plt.xlabel('Full-field flicker')

plt.subplot(2, 2, 3)
#plt.plot(all_f, all_o, '.', alpha=.5)
plt.plot(np.linspace(-1, 1), np.linspace(-1, 1), '--', alpha=.4, color='black')
plt.axvline(0, linestyle='dashed', alpha=.2, color='gray')
plt.axhline(0, linestyle='dashed', alpha=.2, color='gray')
plt.plot(f_npf, o_npf, '.', alpha=.5)
plt.plot(f_pf, o_pf, '.', alpha=.5)
plt.text(1, -0.81, r'$r_{{total}}$ = {:4.2}'.format(r_of), 
         fontsize=r_fontsize, horizontalalignment='right')
plt.text(1, -0.93, r'$r_{{no\;preframes}}$ = {:4.2}'.format(r_of_npf), 
         fontsize=r_fontsize, color='C0', horizontalalignment='right')
plt.text(1, -1.05, r'$r_{{with\;preframes}}$ = {:4.2}'.format(r_of_pf),
         fontsize=r_fontsize, color='C1', horizontalalignment='right')
plt.axis(axis_limits)
plt.axis('square')
plt.xticks(ticks)
plt.yticks(ticks)
plt.title('FFF vs On-off steps')
plt.xlabel('Full-field flicker')
plt.ylabel('On-off steps')

plt.subplot(2, 2, 4)
#plt.plot(all_c, all_o, '.', alpha=.5)
plt.plot(np.linspace(-1, 1), np.linspace(-1, 1), '--', alpha=.4, color='black')
plt.axvline(0, linestyle='dashed', alpha=.2, color='gray')
plt.axhline(0, linestyle='dashed', alpha=.2, color='gray')
plt.plot(c_npf, o_npf, '.', alpha=.5)
plt.plot(c_pf, o_pf, '.', alpha=.5)
plt.text(1, -0.81, r'$r_{{total}}$ = {:4.2}'.format(r_co),
         fontsize=r_fontsize, horizontalalignment='right')
plt.text(1, -0.93, r'$r_{{no\;preframes}}$ = {:4.2}'.format(r_co_npf),
         fontsize=r_fontsize, color='C0', horizontalalignment='right')
plt.text(1, -1.05, r'$r_{{with\;preframes}}$ = {:4.2}'.format(r_co_pf),
         fontsize=r_fontsize, color='C1', horizontalalignment='right')
plt.axis(axis_limits)
plt.axis('square')
plt.xticks(ticks)
plt.yticks(ticks)
plt.title('Checkerflicker vs On-off steps')
plt.xlabel('Checkerflicker')
plt.ylabel('On-off steps')
#plt.tight_layout()
plt.subplots_adjust(top=0.9)
plt.savefig('/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/figures/{}'.format(exp_name), dpi=200, bbox_inches='tight',
                     pad_inches=0.0)
plt.show()
