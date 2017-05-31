#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 16:03:08 2017

@author: ycan

If you get the following error, run the import block below.
ModuleNotFoundError: No module named 'lnp_checkerflicker'

import sys
sys.path.append('/Users/ycan/Documents/official/gottingen/\
lab rotations/LR3 Gollisch/RandPy')
sys.path.append('/Users/ycan/Documents/official/gottingen/lab rotations\
/LR3 Gollisch/scripts/')

"""
import h5py
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
# Custom packages
import lnp_checkerflicker as lnpc
import lnp
import randpy

main_dir = '/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/data/Experiments/Salamander/2014_01_21/'
stimulus_type = 3
# Change stimulus type:
# full field flicker is 2
# checkeflicker is 3
frames_path = 'frametimes/3_checkerflicker10x10bw2blinks_frametimings.mat'
cluster_save = main_dir+'clusterSave.txt'

sx = 60
sy = 80

f = open(cluster_save, 'r')
files = []
for line in f:
    a, b, c = line.split(' ')
    if int(c) < 4:
        files.append('{}{:02.0f}'.format(a, int(b)))
f.close()
files = ['101']  # Use only one file for testing purposes

first_run_flag = True

for filename in files:
    if first_run_flag:
        f = h5py.File(main_dir+frames_path, 'r')
        ftimes = (np.array(f.get('ftimes'))/1000)[:, 0]
        dt = np.average(np.ediff1d(ftimes))
        # Average difference between two frames in miliseconds
        f.close()

        divide_by = 1
        total_frames = ftimes.shape[0]
        total_frames = int(total_frames/divide_by)  # To speed up calculation
        ftimes = ftimes[:total_frames]       # To speed up calculation
        filter_length = 20  # Specified in nr of frames

        stimulus = np.load('/Users/ycan/Documents/official/gottingen/lab \
rotations/LR3 Gollisch/data/checkerflickerstimulus.npy')[:, :, :total_frames]

        first_run_flag = False

    spike_path = main_dir+'rasters/'+str(stimulus_type)+'_SP_C'+filename+'.txt'
    save_path = main_dir+'analyzed/'+str(stimulus_type)+'_SP_C'+filename+'.png'

    spike_file = open(spike_path)
    spike_times = np.array([float(line) for line in spike_file])
    spike_file.close()

    spike_counts = Counter(np.digitize(spike_times, ftimes))
    spikes = np.array([spike_counts[i] for i in range(total_frames)])

# %%
    _, sta_unscaled, max_i, temporal = lnpc.sta(spikes,
                                                         stimulus,
                                                         filter_length,
                                                         total_frames)

    stim_gaus = lnpc.stim_weighted(sta_unscaled, max_i, stimulus)

    sta_weighted, _ = lnp.sta(spikes, stim_gaus, filter_length, total_frames)

    w, v, bins_stc, spikecount_stc, _ = lnpc.stc(spikes, stim_gaus,
                                                 filter_length,
                                                 total_frames, dt)
    
#    generator[0] = np.convolve(sta_unscaled, stimulus,
#                            mode='full')[:-filter_length+1]

    
# %%
    plt.figure(figsize=(15, 15), dpi=200)
    plt.title('STA for cell {}'.format(filename))
    for i in range(20):
        plt.subplot(4, 5, i+1)
        plt.imshow(sta_unscaled[:, :, i], cmap='Greys',
                   vmin=np.min(sta_unscaled),
                   vmax=np.max(sta_unscaled))
    plt.show()

    plt.figure(figsize=(15, 10), dpi=200)
    plt.suptitle('Checkerflicker for {}'.format(
            spike_path.split('Experiments')[1]))

    plt.subplot(2, 2, 1)
    plt.plot(temporal)
    plt.plot(sta_weighted)
    plt.plot(v[:, 0])
    plt.title('STA')
    plt.legend(['Brightest px', 'Weighted stimulus', 'Eigenvalue 0'])

    plt.subplot(2, 2, 2)

    plt.legend(['', '', ''])
    plt.title('Non-linearities')
    plt.xlabel('Linear output')
    plt.ylabel('Variance')

    plt.subplot(2, 4, 5)
    plt.imshow(sta_unscaled[:, :, max_i[2]].reshape((sx, sy,)), cmap='Greys',
               vmin=np.min(sta_unscaled),
               vmax=np.max(sta_unscaled))
    plt.title('Receptive field')
    plt.subplot(2, 4, 6)
    f_size = 5
    plt.imshow(sta_unscaled[max_i[0]-f_size:max_i[0]+f_size+1,
                            max_i[1]-f_size:max_i[1]+f_size+1,
                            int(max_i[2])],
               cmap='Greys',
               vmin=np.min(sta_unscaled),
               vmax=np.max(sta_unscaled))
    plt.title('Brightest pixel: {}'.format(max_i))

    plt.subplot(2, 2, 4)
    plt.plot(w, 'o')
    plt.title('Eigenvalues of covariance matrix')
    plt.xlabel('Eigenvalue index')
    plt.ylabel('Variance')

    plt.show()

#    plt.savefig(save_path, dpi=200, bbox_inches='tight')
#    plt.close()
