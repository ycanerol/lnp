#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  8 16:08:09 2017

@author: ycan
"""
#%%
import numpy as np
import matplotlib.pyplot as plt

kernel_size=20
total_frames=1000

stimulus=np.random.normal(0,3,total_frames) # Generate gaussian 

frames=np.array(np.arange(0,total_frames))
frames=np.linspace(0,1,total_frames)


f1=np.exp(-(frames-0.15)**2/0.002)-np.exp(-(frames-0.17)**2/0.001)
f1=(f1-np.mean(f1))/np.sqrt(sum(f1**2)) #normalize filter

filtered=np.convolve(f1[:kernel_size],stimulus,mode='same')
   
plt.plot(frames,stimulus)
plt.title('Stimulus')
plt.show()
plt.plot(frames,filtered)
plt.title('Filtered stimulus')
plt.show()
#%%
k=np.arange(-kernel_size,kernel_size,1)

def nlt1(k):
    res=[]
    for i in k:
        if i<=0:
            res.append(0)
        else:
            res.append(i*0.1)
    return res            
def nlt2(k):return  np.exp(k*.5)*0.01

plt.plot(k,nlt1(k))
plt.title('Non-linear transformation 1')
plt.show()
#

plt.plot(k,nlt2(k))
plt.title('Non-linear transformation 2')
plt.show()

#%%
#Firing rates
fire_rates=nlt2(filtered)
plt.bar(frames,fire_rates)
plt.title('Firing rates using nlt2 {} frames'.format(total_frames))
#plt.axis([0,600,0,2])
plt.show()

#Spikes
spikes=np.array([])
for i in fire_rates:
    spikes=np.append(spikes,np.random.poisson(i,1))
plt.scatter(frames,spikes)
print(sum(spikes[spikes!=0]))
