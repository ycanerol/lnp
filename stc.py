#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 13:28:17 2017

@author: ycan

Spike-triggered covariance
"""

def stc(spikes,stimulus,filter_length):
    covariance=np.matrix(np.zeros(filter_length,filter_length))
    sta=sta(spikes,stimulus,filter_length)
    for i in range(filter_length,total_frames):
        snippet=stimulus[i:i-filter_length:-1]
        # Snippets are inverted before being added
        snpta=[snippet-sta]
        covariance=covariance+snpta.T*snpta*spikes[i]
    return covariance/fil    