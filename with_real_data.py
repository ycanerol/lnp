#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 12:51:21 2017

@author: ycan

Analysis of real data

Importing lnp only works if the directory containing LNP functions is added to
the python path variable like the following.

sys.path.append('/Users/ycan/Documents/official/gottingen/lab rotations \
/LR3 Gollisch/scripts/')

This only needs to be done once.

"""

import h5py
import numpy as np
import os, sys
import lnp
from collections import Counter
import matplotlib.pyplot as plt

main_dir = '/Users/ycan/Documents/official/gottingen/lab rotations/LR3 Gollisch/data/'
stimulus_path = 'fff2h'
frames_path = 'Experiments/Salamander/2014_01_21/frametimes/2_fff2blinks_frametimings.mat'
spike_path = 'Experiments/Salamander/2014_01_21/rasters/2_SP_C101.txt'

f = h5py.File(main_dir+frames_path, 'r')
ftimes = (np.array(f.get('ftimes'))/1000)[:, 0]
dt = np.average(np.ediff1d(ftimes))
# Average difference between two frames in miliseconds
f.close()
del f

total_frames = ftimes.shape[0]
filter_length = 20  # Specified in nr of frames

stimulus_file = open(main_dir+stimulus_path)
stimulus = np.array([float(line) for line in stimulus_file])
stimulus_file.close()

spike_file = open(main_dir+spike_path)
spike_times = np.array([float(line) for line in spike_file])
spike_file.close()

spike_counts = Counter(np.digitize(spike_times, ftimes))
spikes = np.zeros(total_frames)
spikes = np.array([spike_counts[i] for i in range(total_frames)])
# Bin spikes

stimulus = stimulus[:total_frames]

# Start the analysis

sta = lnp.sta(spikes, stimulus, filter_length, total_frames)[0]
# Use scaled STA

generator = np.convolve(sta, stimulus,
                        mode='full')[:-filter_length+1]

logbins_sta, spikecount_in_logbins_sta = lnp.q_nlt_recovery(spikes, generator,
                                                            60, dt)

plt.plot(sta)
plt.show()
plt.scatter(logbins_sta,spikecount_in_logbins_sta,s=6,alpha=.6)
plt.show()
#%%
w, v = lnp.stc(spikes, stimulus, filter_length, total_frames, dt)


#
#eigen_indices=np.where(np.abs(w-1)>.05)[0]
#manual_eigen_indices = [0, -1]
#
#eigen_legends = []
#for i in manual_eigen_indices:
#    plt.plot(v[:, i])
#    eigen_legends.append(str('Eigenvector '+str(i)))
#plt.plot(sta,':')
#eigen_legends.append('STA')
#plt.legend(eigen_legends, fontsize='x-small')
#plt.title('Filters recovered by STC')
#plt.xlabel('?')
#plt.ylabel('?')