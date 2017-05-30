#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 12:51:21 2017

@author: ycan

Analysis of real data with full field flicker stimulus

Importing lnp only works if the directory containing LNP functions is added to
the python path variable like the following.

import sys
sys.path.append('/Users/ycan/Documents/official/gottingen/lab rotations\
/LR3 Gollisch/scripts/')

This only needs to be done once.

"""

import h5py
import numpy as np
import lnp
from collections import Counter
import matplotlib.pyplot as plt

main_dir = '/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/data/Experiments/Salamander/2014_01_21/'
stimulus_type = 2
# Change stimulus type:
# full field flicker is 2
# checkeflicker is 3
cluster_save = main_dir+'clusterSave.txt'

if stimulus_type == 2:
    stimulus_path = '/Users/ycan/Documents/official/gottingen/\
lab rotations/LR3 Gollisch/data/fff2h'
    frames_path = 'frametimes/2_fff2blinks_frametimings.mat'
elif stimulus_type == 3:
    stimulus_path = '/Users/ycan/Documents/official/gottingen/\
lab rotations/LR3 Gollisch/data/checkerflicker'
    frames_path = 'frametimes/3_checkerflicker10x10bw2blinks_frametimings.mat'

f = open(cluster_save, 'r')
files = []
for line in f:
    a, b, c = line.split(' ')
    if int(c) < 4:
        files.append('{}{:02.0f}'.format(a, int(b)))
f.close()

first_run_flag = True

for filename in files:
    if first_run_flag:
        f = h5py.File(main_dir+frames_path, 'r')
        ftimes = (np.array(f.get('ftimes'))/1000)[:, 0]
        dt = np.average(np.ediff1d(ftimes))
        # Average difference between two frames in miliseconds
        f.close()

        total_frames = ftimes.shape[0]
        filter_length = 20  # Specified in nr of frames

        stimulus_file = open(stimulus_path)
        stimulus = np.array([float(line) for line in stimulus_file])[:total_frames]
        stimulus_file.close()
        first_run_flag = False

    spike_path = main_dir+'rasters/'+str(stimulus_type)+'_SP_C'+filename+'.txt'
    save_path = main_dir+'analyzed/'+str(stimulus_type)+'_SP_C'+filename+'.png'

    spike_file = open(spike_path)
    spike_times = np.array([float(line) for line in spike_file])
    spike_file.close()

    spike_counts = Counter(np.digitize(spike_times, ftimes))
    spikes = np.array([spike_counts[i] for i in range(total_frames)])
    # Bin spikes

    # Start the analysis
    sta = lnp.sta(spikes, stimulus, filter_length, total_frames)[0]
    # Use scaled STA

    generator = np.convolve(sta, stimulus,
                            mode='full')[:-filter_length+1]

    bins_sta, spikecount_sta = lnp.q_nlt_recovery(spikes, generator,
                                                  60, dt)

    eigen_indices = [0, 1, -2, -1]
    bin_nr = 60

    w, v, bins_stc, spikecount_stc, eigen_legends = lnp.stc(spikes, stimulus,
                                                            filter_length,
                                                            total_frames, dt,
                                                            eigen_indices,
                                                            bin_nr)

    # %%
    rows = 1
    columns = 3
    fig = plt.figure(figsize=(20, 5))
    plt.suptitle('Full field flicker for {}'.format(
                    spike_path.split('Experiments')[1]))

    plt.subplot(rows, columns, 1)
    plt.plot(sta, ':')
    plt.plot(v[:, eigen_indices])
    plt.title('Filters')
    plt.legend(['STA']+eigen_legends, fontsize='x-small')
    plt.xticks(np.linspace(0, filter_length, filter_length/2+1))
    plt.xlabel('Time')
    plt.ylabel('Relative filter strength')

    plt.subplot(rows, columns, 2)
    plt.plot(bins_sta, spikecount_sta, '.', alpha=.6)
    plt.plot(bins_stc, spikecount_stc, '.', alpha=.6)
    plt.title('Non-linearities')
    plt.legend(['STA']+eigen_legends, fontsize='x-small')
    plt.xlabel('Linear output')
    plt.ylabel('Firing rate')

    plt.subplot(rows, columns, 3)

    plt.plot(w, 'o')
    plt.title('Eigenvalues of covariance matrix')
    plt.xlabel('Eigenvalue index')
    plt.ylabel('Variance')

    plt.savefig(save_path, dpi=200, bbox_inches='tight')
    plt.close()
