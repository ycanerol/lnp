#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 11 16:56:57 2017

@author: ycan
"""
import matplotlib.pyplot as plt
import matplotlib
#plt.style.use('dark_background')
plt.style.use('default')
matplotlib.rcParams['grid.alpha'] = 0.2
rows=2
columns=2
fig=plt.figure(figsize=(12,8))

plt.subplot(rows,columns,1)
plt.plot(filter_kernel,alpha=.6)
#plt.title()

plt.subplot(rows,columns,1)
plt.plot(recovered_kernel,alpha=.6)
plt.legend(['Filter','Spike triggered average (STA)'])

plt.subplot(rows,columns,2)
plt.plot(k,nlt(k,nlt_index),alpha=.6)

plt.subplot(rows,columns,2)
plt.scatter(logbins,spikecount_in_logbins,alpha=.6)
plt.title('')
#plt.axis((-30,30,np.min(logbins),np.max(logbins)))

plt.subplot(rows,columns,2)
plt.scatter(quantiles,spikecount_in_bins,alpha=.6)
plt.legend(['Non-linear transformation',
            'Recovered using logbins',
            'Recovered using quantiles'],
            fontsize='small')


plt.show()
print('{} seconds were simulated with {} s time steps.'
      .format(np.round(np.max(t)),dt))
print('{} spikes generated.'.format(int(sum(spikes)))
       )
