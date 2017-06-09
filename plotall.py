#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 12:16:38 2017

@author: ycan
"""
import os
import numpy as np
import matplotlib.pyplot as plt

main_dir = '/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/data/Experiments/Salamander/2014_01_27/analyzed/'

exp_name = main_dir.split('/')[-4]+' '+main_dir.split('/')[-3]

allfiles = os.listdir(main_dir)

files_f = []  # Full field flicker
files_c = []  # Checkerflicker

for i in allfiles:
    if i[-4:] == '.npz':
        if i[0] == str(2):
            files_f.append(i.split('C')[-1].split('.')[0])
        elif i[0] == str(3):
            files_c.append(i.split('C')[-1].split('.')[0])

files = [i for i in files_c if i in files_f]

files = ['101']

for i in files:
    fname_f = main_dir+'2_SP_C'+i+'.npz'
    fname_c = main_dir+'3_SP_C'+i+'.npz'

    f = np.load(fname_f)
    c = np.load(fname_c)

    savepath = '/'.join(main_dir.split('/')[:-1])+'SP_C'+i

#%% fullfield

    rows = 1
    columns = 3
    fig = plt.figure(figsize=(20, 5))
    plt.suptitle('Full field flicker for {}'.format(
                    str(f['spike_path']).split('Experiments')[1]))

    plt.subplot(rows, columns, 1)
    plt.plot(f['sta'])
    plt.plot(f['v'][:, 0])
    plt.title('Filters')
    plt.axvline(f['peak'], linewidth=1, color='r', linestyle='dashed')
    plt.legend(['STA', 'Eigenvalue 0', 'Peak'], fontsize='x-small')
    plt.xticks(np.linspace(0, 20, 20/2+1))
    plt.xlabel('Time')
    plt.ylabel('Linear output')

    ax = plt.subplot(rows, columns, 2)
    plt.plot(f['bins_sta'], f['spikecount_sta'], '-')
    plt.plot(f['bins_stc'], f['spikecount_stc'], '-')
    plt.text(.5, .99, 'On-Off Bias: {:2.2f}'.format(float(f['onoffindex'])),
             horizontalalignment='center',
             verticalalignment='top',
             transform=ax.transAxes)
    plt.title('Non-linearities')
    plt.legend(['STA', 'Eigenvalue 0'], fontsize='x-small')
    plt.xlabel('Linear output')
    plt.ylabel('Firing rate')

    plt.subplot(rows, columns, 3)

    plt.plot(f['w'], 'o')
    plt.title('Eigenvalues of covariance matrix')
    plt.xticks(np.linspace(0, 20, 20/2+1))
    plt.xlabel('Eigenvalue index')
    plt.ylabel('Variance')

    plt.show()

    #%% checkerflicker
    if False:  # change if you need STA to be plotted
        plt.figure(figsize=(15, 15), dpi=200)
        plt.title('STA for cell {}'.format(c['filename']))
        for i in range(20):
            plt.subplot(4, 5, i+1)
            plt.imshow(c['sta_unscaled'][:, :, i], cmap='Greys',
                       vmin=np.min(c['sta_unscaled']),
                       vmax=np.max(c['sta_unscaled']))
        plt.show()

    plt.figure(figsize=(15, 10), dpi=200)
    plt.suptitle('Checkerflicker for {}'.format(
            str(c['spike_path']).split('Experiments')[1]))

    plt.subplot(2, 2, 1)
    plt.plot(c['sta_weighted'])
    plt.plot(c['v'][:, 0])
    plt.plot(c['temporal'])
    plt.axvline(c['peak'], linewidth=1, color='r', linestyle='dashed')
    plt.title('Filters')
    plt.ylabel('Linear output')
    plt.xlabel('Time')
    plt.xticks(np.linspace(0, 20, 20/2+1))
    plt.legend(['Weighted stimulus', 'Eigenvalue 0', 'Temporal component',
                'Peak'])

    ax = plt.subplot(2, 2, 2)
    for i in range(len(c['bins'])):
        plt.plot(c['bins'][i], c['spike_counts_in_bins'][i], '-')
    plt.legend(['Weigted stimulus', 'Eigenvector 0'])
    plt.text(.5, .99, 'On-Off Bias: {:2.2f}'.format(float(c['onoffindex'])),
             horizontalalignment='center',
             verticalalignment='top',
             transform=ax.transAxes)
    plt.title('Non-linearities')
    plt.xlabel('Linear output')
    plt.ylabel('Firing rate')

    plt.subplot(2, 4, 5)
    plt.imshow(c['sta_unscaled'][:, :, c['max_i'][2]].reshape((60, 80,)),
               cmap='Greys',
               vmin=np.min(c['sta_unscaled']),
               vmax=np.max(c['sta_unscaled']))
    plt.title('Receptive field')
    plt.subplot(2, 4, 6)
    f_size = 5
    plt.imshow(c['sta_unscaled'][c['max_i'][0]-f_size:c['max_i'][0]+f_size+1,
                                 c['max_i'][1]-f_size:c['max_i'][1]+f_size+1,
                                 int(c['max_i'][2])],
               cmap='Greys',
               vmin=np.min(c['sta_unscaled']),
               vmax=np.max(c['sta_unscaled']))
    plt.title('Brightest pixel: {}'.format(c['max_i']))

    plt.subplot(2, 2, 4)
    plt.plot(c['w'], 'o')
    plt.title('Eigenvalues of covariance matrix')
    plt.xticks(np.linspace(0, 20, 20/2+1))
    plt.xlabel('Eigenvalue index')
    plt.ylabel('Variance')

    plt.show()

    #plt.savefig(save_path, dpi=200, bbox_inches='tight')
    #plt.close()