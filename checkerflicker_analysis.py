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

        total_frames = ftimes.shape[0]
        
        total_frames = int(total_frames/5)  # To speed up calculation
        ftimes = ftimes[:total_frames]       # To speed up calculation
        filter_length = 20  # Specified in nr of frames

        rnd_numbers, seed = randpy.ran1(-10000, total_frames*sx*sy)
        rnd_numbers = np.array(rnd_numbers).reshape(sx, sy, 
                                          total_frames, order='F')
        rnd_numbers = np.where(rnd_numbers > .5, 1 , -1)
        stimulus = rnd_numbers

        first_run_flag = False

    spike_path = main_dir+'rasters/'+str(stimulus_type)+'_SP_C'+filename+'.txt'
    save_path = main_dir+'analyzed/'+str(stimulus_type)+'_SP_C'+filename+'.png'

    spike_file = open(spike_path)
    spike_times = np.array([float(line) for line in spike_file])
    spike_file.close()

    spike_counts = Counter(np.digitize(spike_times, ftimes))
    spikes = np.array([spike_counts[i] for i in range(total_frames)])

#%%
    sta_scaled, sta_unscaled, max_i, temporal = lnpc.sta(spikes,
                                                         stimulus,
                                                         filter_length,
                                                         total_frames)
    
        
    plt.figure(figsize=(15, 15), dpi=200)
    for i in range(20):
        plt.subplot(4, 5, i+1)
        plt.imshow(sta_unscaled[:, :, i], cmap='Greys',
                   vmin=np.min(sta_unscaled),
                   vmax=np.max(sta_unscaled))
    plt.show()

    plt.plot(temporal)
    plt.show()
    f_size = 3
    plt.imshow(sta_unscaled[max_i[0]-f_size:max_i[0]+f_size+1,
                          max_i[1]-f_size:max_i[1]+f_size+1,
                          int(max_i[2])], cmap='Greys',
                          vmin=np.min(sta_unscaled),
                          vmax=np.max(sta_unscaled))
