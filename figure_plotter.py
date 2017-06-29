#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 16:55:59 2017

@author: ycan

Figure plotter
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib


#           Exp date      Cluster   Label       Flipped
plotthis = [['2017_02_14', '901',   'on_cell',  False],
            ['2017_01_31', '8401',  'off_cell', True],
            ['2017_01_17', '201',   'onoff1',   True],
            ['2017_01_17', '4105',  'off_to_on',False],
            ['2017_02_14', '22302', 'on_to_off',True],
            ]


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
LR3 Gollisch/figures/replotted/' + i[2]

    flipper = 1
    if i[3]:
        flipper = -1

    # %% plot all
    matplotlib.rcParams['axes.spines.right'] = False
    matplotlib.rcParams['axes.spines.top'] = False
    matplotlib.rcParams['axes.spines.left'] = True
    matplotlib.rcParams['axes.spines.bottom'] = True

    plt.figure(figsize=(12, 12), dpi=200)
#    plt.suptitle(str(' '.join(str(c['spike_path'])
#                 .split('rasters')[0].split('Experiments')[1]
#                 .split('/'))+str(i[1])))
    plt.subplot(3, 3, 1)
    plt.plot(f['sta']*flipper)
    plt.plot(f['v'][:, 0]*flipper)
    plt.title('Filters')
    plt.legend(['STA', 'STC'], fontsize='small')
    plt.xticks(np.linspace(0, 20, 3), np.linspace(0, 600, 3).astype(int))
    plt.ylabel('Full field flicker\n$\\regular_{Linear\,\,\,output}$',
               fontsize=16)
    plt.xlabel('Time [ms]')

    ax = plt.subplot(3, 3, 2)
    plt.plot(f['bins_sta'], f['spikecount_sta'][::flipper], '-')
    plt.plot(f['bins_stc'], f['spikecount_stc'][::flipper], '-')
    plt.text(.5, .99, 'On-off index: {:2.2f}'
             .format(float(f['onoffindex'])),
             horizontalalignment='center',
             verticalalignment='top',
             transform=ax.transAxes)
    plt.title('Nonlinearities')
    plt.ylabel('Firing rate [Hz]')
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
    plt.legend(['Weighted STA', 'STC', 'Center pixel'],
               fontsize='small')

    ax = plt.subplot(3, 3, 5)
    for j in range(len(c['bins'])):
        plt.plot(c['bins'][j], c['spike_counts_in_bins'][j][::flipper], '-')
    plt.text(.5, .99, 'On-off index: {:2.2f}'
             .format(float(c['onoffindex'])),
             horizontalalignment='center',
             verticalalignment='top',
             transform=ax.transAxes)
    plt.title('Nonlinearities')
    plt.xlabel('Linear output')
    plt.ylabel('Firing rate [Hz]')

    plt.subplot(3, 3, 6)
    plt.plot(c['w'], 'o')
    plt.title('Eigenvalues of covariance matrix')
    plt.xticks(np.linspace(0, 20, 3))
    plt.xlabel('Eigenvalue index')
    plt.ylabel('Variance')

    matplotlib.rcParams['axes.spines.right'] = False
    matplotlib.rcParams['axes.spines.top'] = False
    matplotlib.rcParams['axes.spines.left'] = False
    matplotlib.rcParams['axes.spines.bottom'] = False

    plt.subplot(3, 3, 7)
    plt.imshow(c['sta_unscaled'][:, :, c['max_i'][2]].reshape((60, 80,)),
               cmap='Greys',
               vmin=np.min(c['sta_unscaled']),
               vmax=np.max(c['sta_unscaled']))
    plt.title('Receptive field')

    ax = plt.subplot(3, 3, 8)
    f_size = 5
    plt.imshow(c['sta_unscaled'][c['max_i'][0]-f_size:c['max_i'][0]+f_size+1,
                                 c['max_i'][1]-f_size:c['max_i'][1]+f_size+1,
                                 int(c['max_i'][2])],
               cmap='Greys',
               vmin=np.min(c['sta_unscaled']),
               vmax=np.max(c['sta_unscaled']),
               extent=[-375, 375, -375, 375])
    ax.add_patch(matplotlib.patches.Rectangle(
        (-37.5, -37.5), 75, 75, linewidth=3,
        edgecolor='C2', facecolor='none'))
    plt.title('Center pixel')
    plt.xticks(np.arange(-300, 301, 100))
    plt.xlabel('Distance [µm]')
    plt.ylabel('Distance [µm]')
    plt.tight_layout(pad=5, h_pad=1, w_pad=1.8)
    plt.savefig(savepath, dpi=200, bbox_inches='tight')
#    plt.show()
    plt.close()
