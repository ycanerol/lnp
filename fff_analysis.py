#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 12:51:21 2017

@author: ycan

Analysis of real data with full field flicker stimulus

"""
import sys
import h5py
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
try:
    import lnp
    import lnp_checkerflicker as lnpc
except:
    sys.path.append('/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/scripts/')
    import lnp
    import lnp_checkerflicker as lnpc

main_dir = '/Users/ycan/Documents/official/gottingen/lab rotations/\
LR3 Gollisch/data/Experiments/Salamander/2014_01_27/'
stimulus_type = 2
# Change stimulus type:
# full field flicker is 2
# checkerflicker is 3
cluster_save = main_dir+'clusterSave.txt'

if stimulus_type == 2:
    stimulus_path = '/Users/ycan/Documents/official/gottingen/\
lab rotations/LR3 Gollisch/data/fff2h.npy'
    frames_path = 'frametimes/2_fff2blinks_frametimings.mat'
elif stimulus_type == 3:
    stimulus_path = '/Users/ycan/Documents/official/gottingen/\
lab rotations/LR3 Gollisch/data/checkerflickerstimulus.npy'
    frames_path = 'frametimes/3_checkerflicker10x10bw2blinks_frametimings.mat'

f = open(cluster_save, 'r')
files = []
for line in f:
    a, b, c = line.split(' ')
    if int(c) < 4:
        files.append('{}{:02.0f}'.format(a, int(b)))
f.close()

#files = ['502']

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

        stimulus = np.load(stimulus_path)[:total_frames]
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

    # Bin spikes

    # Start the analysis
    sta = lnp.sta(spikes, stimulus, filter_length, total_frames)[0]
    # Use scaled STA

    generator = np.convolve(sta, stimulus,
                            mode='full')[:-filter_length+1]

    bins_sta, spikecount_sta = lnp.q_nlt_recovery(spikes, generator,
                                                  60, dt)

    eigen_indices = [0]
    bin_nr = 60

    w, v, bins_stc, spikecount_stc, eigen_legends = lnp.stc(spikes, stimulus,
                                                            filter_length,
                                                            total_frames, dt,
                                                            eigen_indices,
                                                            bin_nr)
    sta, bins_sta, \
    spikecount_sta, _, _ = lnpc.onoffindex(sta, bins_sta,
                                           spikecount_sta)

    v[:, 0], bins_stc,\
    spikecount_stc, peak, onoffindex = lnpc.onoffindex(v[:, 0], bins_stc,
                                                       spikecount_stc)

#%%
    np.savez(save_path,
             sta=sta,
             stimulus_type=stimulus_type,
             total_frames=total_frames,
             spikecount_sta=spikecount_sta,
             spikecount_stc=spikecount_stc,
             bins_sta=bins_sta,
             bins_stc=bins_stc,
             filename=filename,
             onoffindex=onoffindex,
             v=v,
             w=w,
             spike_path=spike_path,
             total_spikes=total_spikes,
             peak=peak
             )
