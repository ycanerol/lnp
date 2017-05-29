#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 24 16:41:38 2017

@author: ycan

Functions for STA and STC analysis for checkerflicker stimulus

"""

import numpy as np
from scipy.stats.mstats import mquantiles


def sta(spikes, stimulus, filter_length, total_frames):
    sx = stimulus.shape[0]
    sy = stimulus.shape[1]
    snippets = np.zeros((sx, sy, filter_length))
    for i in range(filter_length, total_frames):
        if spikes[i] != 0:
            snippets = snippets+stimulus[:, :, i:i-filter_length:-1]*spikes[i]
            # Snippets are inverted before being added
    sta_unscaled = snippets/sum(spikes)   # Normalize/scale the STA
    sta_scaled = sta_unscaled/np.sqrt(sum(np.power(sta_unscaled, 2)))

    max_i = np.array(np.where(np.abs(sta_scaled) == 
                              np.max(np.abs(sta_scaled))))
#    max_i = [int(max_i[i]) for i in range(len(max_i))]
    temporal = sta_unscaled[max_i[0], max_i[1], :].reshape(20,)
#    temporal = temporal - np.average(temporal)  # Normalize wrt mean
    spatial_i = (range(max_i[0]-1, max_i[0]+1),
                 range(max_i[1]-1, max_i[1]+1),
                 int(max_i[2]))
    return sta_scaled, sta_unscaled, max_i, temporal  # Unscaled might be needed for STC