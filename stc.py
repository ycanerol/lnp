#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 13:28:17 2017

@author: ycan

Spike-triggered covariance
"""
import numpy as np
import matplotlib.pyplot as plt

sta_temp = sta(spikes, stimulus, filter_length)


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

recovered_stc = stc(spikes, stimulus, filter_length,
                    sta(spikes, stimulus, filter_length))

# %%
w, v = np.linalg.eig(recovered_stc)
# column v[:,i] is the eigenvector corresponding to the eigenvalue w[i]
sorted_eig = np.argsort(w)[::-1]
w = w[sorted_eig]
v = v[:, sorted_eig]

fig = plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(w, 'o', markersize=2)
plt.xlabel('Eigenvalue index')
plt.ylabel('Variance')

eigen_indices = [0, 1]
eigen_legends = []

plt.subplot(1, 2, 2)
for i in eigen_indices:
    plt.plot(v[:, i])
    eigen_legends.append(str('Eigenvector '+str(i)))
plt.plot(recovered_kernel,':')
eigen_legends.append('STA')
plt.legend(eigen_legends, fontsize='x-small')
plt.title('Filters recovered by STC')
plt.xlabel('?')
plt.ylabel('?')

#plt.plot(v[:, -1])
#plt.plot(v[:, -2])
#plt.legend(['1', '2', '-1', '-2'], fontsize='x-small')
plt.show()

