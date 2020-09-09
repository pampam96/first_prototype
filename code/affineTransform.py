#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 10:48:14 2020

@author: marcey
"""

import numpy as np

primary = np.array([[40., 1160., 1.],
                    [40., 40., 5.],
                    [260., 40., 4.],
                    [260., 1160., 3.]])

secondary = np.array([[610., 560., 4.],
                      [610., -560., 6.],
                      [390., -560., 7.],
                      [390., 560., 2.]])

# Pad the data with ones, so that our transformation can do translations too
n = primary.shape[0]
pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))])
unpad = lambda x: x[:,:-1]
X = pad(primary)
Y = pad(secondary)

# Solve the least squares problem X * A = Y
# to find our transformation matrix A
A, res, rank, s = np.linalg.lstsq(X, Y,rcond=None)

transform = lambda x: unpad(np.dot(pad(x), A))

print(A)
print("Target:")
print(secondary)
print("Result:")
print(transform(primary))
print("Max error:", np.abs(secondary - transform(primary)).max())