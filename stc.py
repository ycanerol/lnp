#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 16 13:28:17 2017

@author: ycan

Spike-triggered covariance
"""
from datetime import datetime
import numpy as np
execution_timer = datetime.now()

sta_temp = sta(spikes, stimulus, filter_length)


def stc(spikes, stimulus, filter_length, sta_temp):
    covariance = np.matrix(np.zeros((filter_length, filter_length)))
    for i in range(filter_length, total_frames):
        if spikes[i] != 0:
            snippet = stimulus[i:i-filter_length:-1]
            # Snippets are inverted before being added
            snpta = np.matrix(snippet-sta_temp)
            covariance = covariance+(snpta.T*snpta)*spikes[i]
    return covariance/(sum(spikes)*filter_length-1)

recovered_stc = stc(spikes, stimulus, filter_length,
                    sta(spikes, stimulus, filter_length))
runtime = str(datetime.now()-execution_timer).split('.')[0]
print('Duration: {}'.format(runtime))


w,v = np.linalg.eig(recovered_stc)
# column v[:,i] is the eigenvector corresponding to the eigenvalue w[i]
plt.plot(w, 'o', markersize=2)
plt.show()
plt.plot(v[:,1],'b')
plt.plot(v[:,2],'g')
