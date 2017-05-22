#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 22 14:58:43 2017

@author: ycan

Functions for LNP model

Includes STA, STC to be used in data analysis

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
    return sta_scaled, sta_unscaled # Unscaled might be needed for STC


def log_nlt_recovery(spikes, filtered_recovery, bin_nr):
    logbins = np.logspace(0, np.log(30)/np.log(10), bin_nr)
    logbins = -logbins[::-1]+logbins
    logbindices = np.digitize(filtered_recovery, logbins)
    spikecount_in_logbins = np.array([])
    for i in range(bin_nr):
        spikecount_in_logbins = np.append(spikecount_in_logbins,
                                          (np.average(spikes[np.where
                                                             (logbindices == i)]))/dt)
    return logbins, spikecount_in_logbins


def q_nlt_recovery(spikes, filtered_recovery, bin_nr, dt):
    quantiles = mquantiles(filtered_recovery,
                           np.linspace(0, 1, bin_nr, endpoint=False))
    bindices = np.digitize(filtered_recovery, quantiles)
    # Returns which bin each should go
    spikecount_in_bins = np.array([])
    for i in range(bin_nr):  # Sorts values into bins
        spikecount_in_bins = np.append(spikecount_in_bins,
                                       (np.average(spikes[np.where
                                                          (bindices == i)])/dt))
    return quantiles, spikecount_in_bins


def stc(spikes, stimulus, filter_length, total_frames, dt):
    covariance = np.zeros((filter_length, filter_length))
    sta_temp = sta(spikes, stimulus, filter_length, total_frames)[1]
    # Unscaled STA
    for i in range(filter_length, total_frames):
        if spikes[i] != 0:
            snippet = stimulus[i:i-filter_length:-1]
            # Snippets are inverted before being added
            snippet = snippet-np.dot(snippet, sta_temp)*sta_temp
            # Project out the STA from snippets
            snpta = np.array(snippet-sta_temp)[np.newaxis, :]
            covariance = covariance+np.dot(snpta.T, snpta)*spikes[i]
    return covariance/(sum(spikes)-1)
