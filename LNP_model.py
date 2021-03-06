#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  9 18:11:51 2017

@author: ycan
"""
import numpy as np
from scipy.stats.mstats import mquantiles
from datetime import datetime
import matplotlib

execution_timer = datetime.now()

total_frames = 3000000
dt = 0.01   # Time step
t = np.arange(0, total_frames*dt, dt)  # Time vector
filter_time = .6  # The longest feature RGCs respond to is ~600ms
filter_length = int(filter_time/dt)  # Filter is filter_length frames long

cweight = .5  # The weight of combination for the two filters


def make_noise():  # Generate gaussian noise for stimulus
    return np.random.normal(0, 1, total_frames)

stimulus = make_noise()

filter_index1 = 1  # Change filter type here
filter_index2 = 4


def linear_filter(t, filter_index):    # Define filter according to choice
    if filter_index == 1:
        f = np.exp(-(t-.15)**2/.002)-np.exp(-(t-.17)**2/.001)
    elif filter_index == 2:
        f = np.exp(-(t-.05)**2/.002)-2*np.exp(-(t-.22)**2/.001)
    elif filter_index == 3:
        f = np.exp(-(t-0.06)**2/.002)
    elif filter_index == 4:
        f = np.exp(-(.4*t-0.1)**2/0.002)-2*np.exp(-(t-.5)**2/.001)
    else:
        raise ValueError('Invalid filter index')
    f = (f-np.mean(f)) / np.sqrt(sum(f**2))  # Normalize filter
    return f[:filter_length]  # Kernel should be filter_length frames long

filter_kernel1 = linear_filter(t, filter_index1)   # Two parallel filters are
filter_kernel2 = linear_filter(t, filter_index2)   # applied at the same time
filtered1 = np.convolve(filter_kernel1, stimulus,
                        mode='full')[:-filter_length+1]
filtered2 = np.convolve(filter_kernel2, stimulus,
                        mode='full')[:-filter_length+1]

k = np.linspace(-5, 5, 1001)
nlt_index1 = 1
nlt_index2 = 1


def nlt(k, nlt_index):
    if nlt_index == 1:
        nlfunction = lambda x: (0 if x < 0 else 4.2*x)
    elif nlt_index == 2:
        nlfunction = lambda x: np.exp(x*.6)
    elif nlt_index == 3:
        nlfunction = lambda x: -20/(1+np.exp(3*(x-3)))+20
    elif nlt_index == 4:
        nlfunction = lambda x: (-x*.8 if x < 0 else 4*x)
    elif nlt_index == 5:
        nlfunction = lambda x: (.4*x**2 if x < 0 else .9*x**2)
    elif nlt_index == 6:
        nlfunction = lambda x: x**2
    else:
        raise ValueError('Invalid non-linearity index')
    return np.array([nlfunction(x) for x in k])

fire_rates1 = np.array(nlt(filtered1, nlt_index1))
fire_rates2 = np.array(nlt(filtered2, nlt_index2))
fire_rates_sum = cweight*fire_rates1+(1-cweight)*fire_rates2
# Fire rates are combined with a linear weight

spikes = np.array(np.random.poisson(fire_rates_sum*dt))

print('{} spikes generated.'.format(int(sum(spikes))))


def sta(spikes, stimulus, filter_length, total_frames):
    snippets = np.zeros(filter_length)
    for i in range(filter_length, total_frames):
        if spikes[i] != 0:
            snippets = snippets+stimulus[i:i-filter_length:-1]*spikes[i]
            # Snippets are inverted before being added
    sta_unscaled = snippets/sum(spikes)   # Normalize/scale the STA
    sta_scaled = sta_unscaled/np.sqrt(sum(np.power(sta_unscaled, 2)))
    return sta_scaled, sta_unscaled
recovered_kernel = sta(spikes, stimulus, filter_length, total_frames)[0]
# Use scaled STA

filtered_recovery = np.convolve(recovered_kernel, stimulus,
                                mode='full')[:-filter_length+1]


# Variable bin size, log
def log_nlt_recovery(spikes, filtered_recovery, bin_nr, k):
    logbins = np.logspace(0, np.log(max(k))/np.log(10), bin_nr)
    logbins = -logbins[::-1]+logbins
    logbindices = np.digitize(filtered_recovery, logbins)
    spikecount_in_logbins = np.array([])
    for i in range(bin_nr):
        spikecount_in_logbins = np.append(spikecount_in_logbins,
                                          (np.average(spikes[np.where
                                                             (logbindices == i)]))/dt)
    return logbins, spikecount_in_logbins


# Using mquantiles
def q_nlt_recovery(spikes, filtered_recovery, bin_nr, k=0):
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

logbins_sta, spikecount_in_logbins_sta = log_nlt_recovery(
                                                          spikes,
                                                          filtered_recovery,
                                                          60, k)

quantiles_sta, spikecount_in_bins_sta = q_nlt_recovery(spikes,
                                                       filtered_recovery, 100)

runfile('/Users/ycan/Documents/official/gottingen/lab rotations/LR3 Gollisch/scripts/stc.py', wdir='/Users/ycan/Documents/python')

runfile('/Users/ycan/Documents/official/gottingen/lab rotations/LR3 Gollisch/scripts/plotLNP.py', wdir='/Users/ycan/Documents/python')

runtime = str(datetime.now()-execution_timer).split('.')[0]
print('Duration: {}'.format(runtime))
