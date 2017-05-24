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
    snippets = np.zeros(filter_length)
    for i in range(filter_length, total_frames):
        if spikes[i] != 0:
            snippets = snippets+stimulus[i:i-filter_length:-1]*spikes[i]
            # Snippets are inverted before being added
    sta_unscaled = snippets/sum(spikes)   # Normalize/scale the STA
    sta_scaled = sta_unscaled/np.sqrt(sum(np.power(sta_unscaled, 2)))
    return sta_scaled, sta_unscaled  # Unscaled might be needed for STC