#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 16:55:59 2017

@author: ycan

Figure plotter
"""

import numpy as np
import matplotlib.pyplot as plt


#           Exp date      Cluster Label Flipped
plotthis = [['2017_02_14', '901', 'On cell', False],
            ['2017_01_31', '8401', 'Off cell', True],
            ['2017_01_17', '201',  'On off 1', True]]

for i in plotthis:

    main_dir = '/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/data/Experiments/Mouse/'

    currentfile_c = main_dir + i[0] +\
                    '/analyzed/2_SP_C' + i[1] + '.npz'
    currentfile_f = main_dir + i[0] +\
                    '/analyzed/3_SP_C' + i[1] + '.npz'

    c = np.load(str(currentfile_c))
    f = np.load(str(currentfile_f))

    savepath = '/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/figures' + i[2]

    flipper = 1
    if i[3]:
        flipper = -1

    # %% plot all
    plt.figure(figsize=(12, 12), dpi=200)
    plt.suptitle(str(' '.join(str(c['spike_path'])
                 .split('rasters')[0].split('Experiments')[1]
                 .split('/'))+str(i[1])))
    plt.subplot(3, 3, 1)
    plt.plot(f['sta']*flipper)
    plt.plot(f['v'][:, 0]*flipper)
    plt.title('Filters')
    plt.legend(['STA', 'Eigenvalue 0'], fontsize='small')
    plt.xticks(np.linspace(0, 20, 3), np.linspace(0, 600, 3).astype(int))
    plt.ylabel('Full field flicker\n$\\regular_{Linear\,\,\,output}$',
               fontsize=16)
    plt.xlabel('Time [ms]')

    ax = plt.subplot(3, 3, 2)
    plt.plot(f['bins_sta'], f['spikecount_sta'][::flipper], '-')
    plt.plot(f['bins_stc'], f['spikecount_stc'][::flipper], '-')
    plt.text(.5, .99, 'On-Off Bias: {:2.2f}\nTotal spikes: {}'
             .format(float(f['onoffindex']), f['total_spikes']),
             horizontalalignment='center',
             verticalalignment='top',
             transform=ax.transAxes)
    plt.title('Non-linearities')
    plt.ylabel('Firing rate')
    plt.xlabel('Linear output')

    plt.subplot(3, 3, 3)
    plt.plot(f['w'], 'o')
    plt.title('Eigenvalues of covariance matrix')
    plt.xticks(np.linspace(0, 20, 3))
    plt.xlabel('Eigenvalue index')
    plt.ylabel('Variance')

    plt.subplot(3, 3, 4)
    plt.plot(c['sta_weighted']*flipper)
    plt.plot(c['v'][:, 0]*flipper)
    plt.plot(c['temporal'])
    plt.title('Filters')
    plt.ylabel('Checkerflicker\n$\\regular_{Linear\,\,\,output}$', fontsize=16)
    plt.xlabel('Time [ms]')
    plt.xticks(np.linspace(0, 20, 3), np.linspace(0, 600, 3).astype(int))
    plt.legend(['Weighted stimulus', 'Eigenvalue 0', 'Brightest pixel'],
               fontsize='small')

    ax = plt.subplot(3, 3, 5)
    for j in range(len(c['bins'])):
        plt.plot(c['bins'][j], c['spike_counts_in_bins'][j][::flipper], '-')
    plt.text(.5, .99, 'On-Off Bias: {:2.2f}\nTotal spikes: {}'
             .format(float(c['onoffindex']), c['total_spikes']),
             horizontalalignment='center',
             verticalalignment='top',
             transform=ax.transAxes)
    plt.title('Non-linearities')
    plt.xlabel('Linear output')
    plt.ylabel('Firing rate')

    plt.subplot(3, 3, 6)
    plt.plot(c['w'], 'o')
    plt.title('Eigenvalues of covariance matrix')
    plt.xticks(np.linspace(0, 20, 3))
    plt.xlabel('Eigenvalue index')
    plt.ylabel('Variance')

    plt.subplot(3, 3, 7)
    plt.imshow(c['sta_unscaled'][:, :, c['max_i'][2]].reshape((60, 80,)),
               cmap='Greys',
               vmin=np.min(c['sta_unscaled']),
               vmax=np.max(c['sta_unscaled']))
    plt.title('Receptive field')

    plt.subplot(3, 3, 8)
    f_size = 5
    plt.imshow(c['sta_unscaled'][c['max_i'][0]-f_size:c['max_i'][0]+f_size+1,
                                 c['max_i'][1]-f_size:c['max_i'][1]+f_size+1,
                                 int(c['max_i'][2])],
               cmap='Greys',
               vmin=np.min(c['sta_unscaled']),
               vmax=np.max(c['sta_unscaled']))
    plt.title('Brightest pixel: {}'.format(c['max_i']))
    plt.tight_layout(pad=5, h_pad=1, w_pad=1.8)
    plt.show()
#    plt.savefig(savepath, dpi=200, bbox_inches='tight')
    plt.close()
