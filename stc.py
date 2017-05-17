#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 13:28:17 2017

@author: ycan

Spike-triggered covariance
"""
from datetime import datetime
import numpy as np
import matplotlib.pyplot as plt
execution_timer = datetime.now()

sta_temp = sta(spikes, stimulus, filter_length)


def stc(spikes, stimulus, filter_length, sta_temp):
    covariance = np.zeros((filter_length, filter_length))
    for i in range(filter_length, total_frames):
        if spikes[i] != 0:
            snippet = stimulus[i:i-filter_length:-1]
            # Snippets are inverted before being added
            snpta = np.array(snippet-sta_temp)[np.newaxis,:]
            covariance = covariance+np.dot(snpta.T, snpta)*spikes[i]
    return covariance/(sum(spikes)-1)

recovered_stc = stc(spikes, stimulus, filter_length,
                    sta(spikes, stimulus, filter_length))
runtime = str(datetime.now()-execution_timer).split('.')[0]
print('Duration: {}'.format(runtime))

# %%
w, v = np.linalg.eig(recovered_stc)
# column v[:,i] is the eigenvector corresponding to the eigenvalue w[i]
sorted_eig = np.argsort(w)[::-1]
w = w[sorted_eig]
v = v[:, sorted_eig]

fig=plt.figure(figsize=(12, 4))

plt.subplot(1,2,1)
plt.plot(w, 'o', markersize=2)

plt.subplot(1,2,2)
plt.plot(v[:, 0])
plt.plot(v[:, 1])
plt.plot(recovered_kernel)
plt.legend(['0', '1', 'STA'], fontsize='x-small')


#plt.plot(v[:, -1])
#plt.plot(v[:, -2])
#plt.legend(['1', '2', '-1', '-2'], fontsize='x-small')
plt.show()

