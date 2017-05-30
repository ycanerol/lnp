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
    max_i = np.squeeze(np.where(np.abs(sta_gaussian) ==
                              np.max(np.abs(sta_gaussian))))
    temporal = sta_unscaled[max_i[0], max_i[1], :].reshape(20,)
    temporal = temporal / np.sqrt(np.sum(np.power(temporal, 2)))
    spatial_i = (range(max_i[0]-1, max_i[0]+1),
                 range(max_i[1]-1, max_i[1]+1),
                 int(max_i[2]))
    return sta_scaled, sta_unscaled, max_i, temporal
    # Unscaled might be needed for STC


def stim_weighted(sta, max_i, stimulus):
    # Turns the checkerflicker stimulus into more Gaussian-like
    f_size = 5
    weights = sta[max_i[0]-f_size-1:max_i[0]+f_size,
                  max_i[1]-f_size-1:max_i[1]+f_size,
                  max_i[2]].reshape((2*f_size+1, 2*f_size+1))
    if weights.max() < np.max(np.abs(weights)):
        weights = -weights
    stim_small = stimulus[max_i[0]-f_size-1:max_i[0]+f_size,
                          max_i[1]-f_size-1:max_i[1]+f_size,:]
    stim_weighed = np.array([])
    for i in range(stim_small.shape[2]):
        stim_weighed = np.append(stim_weighed, np.sum(stim_small[:, :, i] *
                                                      weights))
    return stim_weighed


def nlt_recovery(spikes, filtered_recovery, bin_nr, dt):
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


def stc(spikes, stimulus, filter_length, total_frames, dt,
        eigen_indices=[0, 1, -2, -1], bin_nr=60):
    # Non-centered STC
    covariance = np.zeros((filter_length, filter_length))
    for i in range(filter_length, total_frames):
        if spikes[i] != 0:
            snippet = stimulus[i:i-filter_length:-1]
            snippet = np.reshape(snippet, (1, 20))
            covariance = covariance+np.dot(snippet.T, snippet)*spikes[i]
    covariance = covariance/(np.sum(spikes)-1)
    eigenvalues, eigenvectors = np.linalg.eig(covariance)

    sorted_eig = np.argsort(eigenvalues)[::-1]
    eigenvalues = eigenvalues[sorted_eig]
    eigenvectors = eigenvectors[:, sorted_eig]

    # Calculating nonlinearities
    generator_stc = np.zeros((total_frames, len(eigen_indices)))
    bins_stc = np.zeros((bin_nr, len(eigen_indices)))
    spikecount_stc = np.zeros((bin_nr, len(eigen_indices)))
    eigen_legends = []

    for i in range(len(eigen_indices)):
        generator_stc[:, i] = np.convolve(eigenvectors[:, eigen_indices[i]],
                                          stimulus,
                                          mode='full')[:-filter_length+1]
        bins_stc[:, i],\
        spikecount_stc[:, i] = nlt_recovery(spikes,
                                            generator_stc[:, i], 60, dt)
        if eigen_indices[i] < 0:
            eigen_legends.append('Eigenvector {}'
                                 .format(filter_length+int(eigen_indices[i])))
        else:
            eigen_legends.append('Eigenvector {}'.format(int(eigen_indices[i])))

    return eigenvalues, eigenvectors, bins_stc, spikecount_stc, eigen_legends
