#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 12:51:21 2017

@author: ycan

Analysis of real data

Importing lnp only works if the directory containing LNP functions is added to 
the python path variable like the following. 

sys.path.append('/Users/ycan/Documents/official/gottingen/lab rotations
/LR3 Gollisch/scripts/')

This only needs to be done once.

"""

import h5py
import numpy as np
import os, sys
from lnp import *

stimulus_path = '/Users/ycan/Documents/official/gottingen/lab rotations/LR3 Gollisch/data/fff2h'
frames_path = '/Users/ycan/Documents/official/gottingen/lab rotations/LR3 Gollisch/data/Experiments/Salamander/2014_01_21/frametimes/2_fff2blinks_frametimings.mat'
spike_path = '/Users/ycan/Documents/official/gottingen/lab rotations/LR3 Gollisch/data/Experiments/Salamander/2014_01_21/rasters/1_SP_C101.txt'

f = h5py.File(frames_path, 'r')
ftimes = np.array(f.get('ftimes'))
f.close(); del f
#%%
stimulus_file = open(stimulus_path)
stimulus = np.array([float(line) for line in stimulus_file])
stimulus_file.close()

spike_file = open(spike_path)
spikes = np.array([float(line) for line in spike_file])
spike_file.close()



