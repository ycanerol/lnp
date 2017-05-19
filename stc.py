#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 13:28:17 2017

@author: ycan

Spike-triggered covariance
"""
import numpy as np
import matplotlib.pyplot as plt

matplotlib.rcParams['figure.dpi'] = 100

sta_temp = sta(spikes, stimulus, filter_length)[1] # Unscaled STA


def stc(spikes, stimulus, filter_length, sta_temp):
    covariance = np.zeros((filter_length, filter_length))
    for i in range(filter_length, total_frames):
        if spikes[i] != 0:
            snippet = stimulus[i:i-filter_length:-1]
            # Snippets are inverted before being added
            snippet = snippet-np.dot(snippet,sta_temp)*sta_temp
            # Project out the STA from snippets
            snpta = np.array(snippet-sta_temp)[np.newaxis, :]
            
            covariance = covariance+np.dot(snpta.T, snpta)*spikes[i]
    return covariance/(sum(spikes)-1)

recovered_stc = stc(spikes, stimulus, filter_length, sta_temp)

# %%
w, v = np.linalg.eig(recovered_stc)
# column v[:,i] is the eigenvector corresponding to the eigenvalue w[i]
sorted_eig = np.argsort(w)[::-1]
w = w[sorted_eig]
v = v[:, sorted_eig]

eigen_indices=np.where(np.abs(w-1)>.05)[0]
manual_eigen_indices = [0, -1]

filtered_recovery_stc1 = np.convolve(v[:, eigen_indices[0]], stimulus,
                                     mode='full')[:-filter_length+1]

filtered_recovery_stc2 = np.convolve(v[:, eigen_indices[0]], stimulus,
                                     mode='full')[:-filter_length+1]

logbins_stc1, spikecount_in_logbins_stc1 = log_nlt_recovery(spikes,
                                                            filtered_recovery_stc1,
                                                            60, k)
#quantiles_stc1,spikecount_in_bins_stc1 = q_nlt_recovery(spikes, filtered_recovery,100)    
logbins_stc2, spikecount_in_logbins_stc2 = log_nlt_recovery(spikes,
                                                            filtered_recovery_stc2,
                                                            60, k)  



