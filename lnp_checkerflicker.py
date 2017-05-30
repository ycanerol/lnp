#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 16:41:38 2017

@author: ycan

Functions for STA and STC analysis for checkerflicker stimulus

"""

import numpy as np
from scipy.stats.mstats import mquantiles
import scipy.ndimage as ndi


def sta(spikes, stimulus, filter_length, total_frames):
    sx = stimulus.shape[0]
    sy = stimulus.shape[1]
    snippets = np.zeros((sx, sy, filter_length))
    for i in range(filter_length, total_frames-filter_length+1):
        if spikes[i] != 0:
            stimulus_reversed = stimulus[:, :, i-filter_length+1:i+1][:,:,::-1]
            snippets = snippets+stimulus_reversed*spikes[i]
            # Snippets are inverted before being added
    sta_unscaled = snippets/np.sum(spikes)   # Normalize/scale the STA
    sta_scaled = sta_unscaled/np.sqrt(np.sum(np.power(sta_unscaled, 2)))

    sta_gaussian = ndi.filters.gaussian_filter(sta_unscaled, sigma=(1, 1, 0))
    # Gaussian is applied before searching for the brightest/darkest pixel
    # to exclude randomly high values outside the receptive field
    max_i = np.array(np.where(np.abs(sta_gaussian) ==
                              np.max(np.abs(sta_gaussian))))
#    max_i = [int(max_i[i]) for i in range(len(max_i))]
    temporal = sta_unscaled[max_i[0], max_i[1], :].reshape(20,)
#    temporal = temporal - np.average(temporal)  # Normalize wrt mean
    spatial_i = (range(max_i[0]-1, max_i[0]+1),
                 range(max_i[1]-1, max_i[1]+1),
                 int(max_i[2]))
    return sta_scaled, sta_unscaled, max_i, temporal  
    # Unscaled might be needed for STC


def stim_weighted(sta, max_i, stimulus):
    # Turns the checkerflicker stimulus into more Gaussian-likeß
    sx = stimulus.shape[0]
    sy = stimulus.shape[1]
    f_size = 5
    weights = sta[max_i[0]-f_size-1:max_i[0]+f_size,
                  max_i[1]-f_size-1:max_i[1]+f_size,
                  max_i[2]].reshape((2*f_size+1, 2*f_size+1))

    stim_weighed = []
    for i in range(stim_small.shape[2]):
        stim_weighed = np.append(stim_weighed, np.sum(stim_small[:,:,i] * 
                                                      weights))
    return stim_weighed
        