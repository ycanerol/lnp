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
matplotlib.rcParams['grid.alpha'] = 0.1
rows=2
columns=2
fig=plt.figure(figsize=(12,8))

plt.subplot(rows,columns,1)
plt.plot(filter_kernel1,alpha=.2)
#plt.title()

plt.subplot(rows,columns,1)
plt.plot(filter_kernel2,alpha=.2)

plt.subplot(rows,columns,1)
plt.plot(cweight*filter_kernel1+(1-cweight)*filter_kernel2,alpha=.6)

plt.subplot(rows,columns,1)
plt.plot(recovered_kernel,alpha=.6)

plt.legend(['Filter 1','Filter 2','{}*Filter 1+{}*Filter 2'.format(cweight
            ,np.round(1-cweight,2)),'Spike triggered average (STA)'],
            fontsize='x-small')
plt.grid()
plt.title('Linear transformation')
plt.xlabel('Time [ms]')


plt.subplot(rows,columns,2)
plt.plot(k,nlt(k,nlt_index1),alpha=.6)

plt.subplot(rows,columns,2)
plt.plot(k,nlt(k,nlt_index2),alpha=.6)

plt.plot(k,cweight*nlt(k,nlt_index1)+(1-cweight)*nlt(k,nlt_index2),alpha=.6)

plt.subplot(rows,columns,2)
plt.scatter(logbins,spikecount_in_logbins,s=6,alpha=.6)

plt.subplot(rows,columns,2)
plt.scatter(quantiles,spikecount_in_bins,s=6,alpha=.6)
plt.legend(['Non-linear transformation 1',
            'Non-linear transformation 2',
            '{}*NLT1+{}*NLT2'.format(cweight,np.round(1-cweight,2)),
            'Recovered using logbins',
            'Recovered using quantiles'],
            fontsize='x-small')
plt.title('Non-linear transformation')

plt.show()
print('{} seconds were simulated with {} s time steps.'
      .format(np.round(np.max(t)),dt))
print('{} spikes generated.'.format(int(sum(spikes)))
       )
