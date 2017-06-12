#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 16:03:08 2017

@author: ycan

Analyze checkerflicker stimulus for cells

"""
import sys
import h5py
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
# Custom packages
try:
    import lnp_checkerflicker as lnpc
    import lnp
except:
    sys.path.append('/Users/ycan/Documents/official/gottingen/lab rotations\
/LR3 Gollisch/scripts/')
    import lnp_checkerflicker as lnpc
    import lnp

main_dir = '/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/data/Experiments/Salamander/2014_02_25/'
stimulus_type = 3
# Change stimulus type:
# full field flicker is 2
# checkerflicker is 3
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

#files=['101']

first_run_flag = True

for filename in files:
    if first_run_flag:
        f = h5py.File(main_dir+frames_path, 'r')
        ftimes = (np.array(f.get('ftimes'))/1000)[:, 0]
        dt = np.average(np.ediff1d(ftimes))
        # Average difference between two frames in miliseconds
        f.close()

        total_frames = ftimes.shape[0]
        ftimes = ftimes[:total_frames]
        filter_length = 20  # Specified in nr of frames

        stimulus = np.load('/Users/ycan/Documents/official/gottingen/lab \
rotations/LR3 Gollisch/data/checkerflickerstimulus.npy')[:, :, :total_frames]

        first_run_flag = False

    spike_path = main_dir+'rasters/'+str(stimulus_type)+'_SP_C'+filename+'.txt'
    save_path = main_dir+'analyzed/'+str(stimulus_type)+'_SP_C'+filename

    spike_file = open(spike_path)
    spike_times = np.array([float(line) for line in spike_file])
    spike_file.close()

    spike_counts = Counter(np.digitize(spike_times, ftimes))
    spikes = np.array([spike_counts[i] for i in range(total_frames)])

    total_spikes = np.sum(spikes)
    if total_spikes < 2:
        continue

# %%
    sta_unscaled, max_i, temporal = lnpc.sta(spikes,
                                             stimulus,
                                             filter_length,
                                             total_frames)
    max_i = lnpc.check_max_i(sta_unscaled, max_i)

    stim_gaus = lnpc.stim_weighted(sta_unscaled, max_i, stimulus)

    sta_weighted, _ = lnp.sta(spikes, stim_gaus, filter_length, total_frames)

    w, v, _, _, _ = lnpc.stc(spikes, stim_gaus,
                             filter_length, total_frames, dt)

    bins = []
    spike_counts_in_bins = []
    for i in [sta_weighted, v[:, 0]]:
        a, b = lnpc.nlt_recovery(spikes, stim_gaus, i, 60, dt)
        bins.append(a)
        spike_counts_in_bins.append(b)

    sta_weighted, bins[0], \
    spike_counts_in_bins[0], \
    _, _ = lnpc.onoffindex(sta_weighted, bins[0],
                           spike_counts_in_bins[0])

    v[:, 0], bins[1],\
    spike_counts_in_bins[1],\
    peak, onoffindex = lnpc.onoffindex(v[:, 0], bins[1],
                                       spike_counts_in_bins[1])

#%%
    np.savez(save_path,
             sta_unscaled=sta_unscaled,
             sta_weighted=sta_weighted,
             stimulus_type=stimulus_type,
             total_frames=total_frames,
             temporal=temporal,
             v=v,
             w=w,
             max_i=max_i,
             spike_path=spike_path,
             filename=filename,
             bins=bins,
             spike_counts_in_bins=spike_counts_in_bins,
             onoffindex=onoffindex,
             total_spikes=total_spikes,
             peak=peak
             )
