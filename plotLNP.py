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
matplotlib.rcParams['figure.dpi'] = 100

rows = 2
columns = 1
fig = plt.figure(figsize=(8, 10))

plt.subplot(rows, columns, 1)
plt.plot(filter_kernel1, alpha=.4)
#plt.title()

plt.subplot(rows, columns, 1)
plt.plot(filter_kernel2, alpha=.4)

plt.subplot(rows, columns, 1)
plt.plot(cweight*filter_kernel1+(1-cweight)*filter_kernel2, alpha=.6)

plt.subplot(rows, columns, 1)
plt.plot(recovered_kernel, alpha=.6)

plt.legend(['Filter {}'.format(filter_index1),
            'Filter {}'.format(filter_index2),
            '{}*Filter {}+{}*Filter {}'.format(cweight, filter_index1, 
             np.round(1-cweight,2),filter_index2),
            'Spike triggered average (STA)'],
            fontsize='x-small')
plt.grid()
plt.title('Linear filters')
plt.xlabel('Time')
plt.ylabel('Relative filter strength')


plt.subplot(rows,columns,2)
plt.plot(k,nlt(k,nlt_index1),alpha=.6)

plt.subplot(rows,columns,2)
plt.plot(k,nlt(k,nlt_index2),alpha=.6)

plt.plot(k,cweight*nlt(k,nlt_index1)+(1-cweight)*nlt(k,nlt_index2),alpha=.6)

plt.subplot(rows,columns,2)
plt.scatter(logbins_sta,spikecount_in_logbins_sta,s=6,alpha=.6)

plt.subplot(rows,columns,2)
plt.scatter(quantiles_sta,spikecount_in_bins_sta,s=6,alpha=.6)
plt.legend(['Non-linear transformation {}'.format(nlt_index1),
            'Non-linear transformation {}'.format(nlt_index2),
            '{}*NLT{}+{}*NLT{}'.format(cweight,nlt_index1,
             np.round(1-cweight,2),nlt_index2),
            'Recovered using logbins',
            'Recovered using quantiles'],
            fontsize='x-small')
plt.title('Non-linear transformation')
plt.xlabel('?')
plt.ylabel('?')

plt.show()
print('{} seconds were simulated with {} s time steps.'
      .format(np.round(np.max(t)),dt))
print('{} spikes generated.'.format(int(sum(spikes)))
       )

# %% Plotting STC

fig = plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.plot(w, 'o', markersize=2)
plt.xlabel('Eigenvalue index')
plt.ylabel('Variance')


eigen_legends = []

plt.subplot(1, 2, 2)
for i in interesting_eigen_indices:
    plt.plot(v[:, i])
    eigen_legends.append(str('Eigenvector '+str(i)))
plt.plot(recovered_kernel,':')
eigen_legends.append('STA')
plt.legend(eigen_legends, fontsize='x-small')
plt.title('Filters recovered by STC')
plt.xlabel('?')
plt.ylabel('?')
plt.show()

