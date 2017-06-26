#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 15:27:36 2017

@author: ycan
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib
# Function definitions from LNP_model.py


t = np.arange(0,.6,.01)
plt.plot(linear_filter(t,1))
plt.axis('off')
plt.savefig('/Users/ycan/Downloads/linear.svg', format='svg', transparent=True)
plt.show()

k = np.linspace(-5, 5, 1001)
plt.plot(k, nlt(k,2))
plt.axis('off')
plt.savefig('/Users/ycan/Downloads/nonlinear.svg', format='svg', transparent=True)
plt.show()
