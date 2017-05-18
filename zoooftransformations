#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 15:45:34 2017

@author: ycan

Zoo of linear filters and non-linear transformations
"""

import matplotlib.pyplot as plt
import matplotlib

rows = 2
columns = 1
fig = plt.figure(figsize=(6, 8))

plt.subplot(rows, columns, 1)
filter_legends = []
for i in range(1, 5):
    plt.plot(linear_filter(t, i), alpha=.5)
    filter_legends.append(str('Filter '+str(i)))
plt.legend(filter_legends)
plt.title('Filters')

plt.subplot(rows, columns, 2)
nlt_legends = []
for i in range(1, 7):
    plt.plot(k,nlt(k, i), alpha=.5)
    nlt_legends.append(str('NLT '+str(i)))
plt.legend(nlt_legends)
plt.title('Non-linear transformations')
