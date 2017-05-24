#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 16:03:08 2017

@author: ycan

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
        filter_length = 20  # Specified in nr of frames

        rnd_numbers, seed = randpy.ran1(-10000, int(total_frames/10)*sx*sy)
        rnd_numbers = np.array(rnd_numbers).reshape(sx, sy, int(total_frames/10))

        first_run_flag = False

    spike_path = main_dir+'rasters/'+str(stimulus_type)+'_SP_C'+filename+'.txt'
    save_path = main_dir+'analyzed/'+str(stimulus_type)+'_SP_C'+filename+'.png'

    spike_file = open(spike_path)
    spike_times = np.array([float(line) for line in spike_file])
    spike_file.close()

    spike_counts = Counter(np.digitize(spike_times, ftimes))
    spikes = np.array([spike_counts[i] for i in range(total_frames)])


