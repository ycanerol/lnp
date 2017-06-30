#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 30 10:41:00 2017

@author: ycan

Make tables for latex 
"""
#%%
#OFF, ON-OFF, ON
b=np.array([0,0,0])
for data in [all_f, all_c, all_o]:
    a= np.array([np.where(data < -0.5)[0].size,
                 np.where(np.abs(data) < 0.5)[0].size,
                 np.where(data > 0.5)[0].size])/data.size
    b = np.vstack((b,a))
b = b[1:,:]    
rh = ['Full-field flicker', 'Checkerflicker', 'On-off steps']
b=b*100

for i in range(3):
    print('{} & {:4.1f} & {:4.1f} & {:4.1f} \\\\'.format(rh[i],b[i,0],b[i,1],b[i,2]))

