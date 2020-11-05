#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 10:48:14 2020

@author: marcey
"""

import numpy as np
#
#WORLD
#primary = np.array([[40., 1160., 1.],
#                    [40., 40., 5.],
#                    [260., 40., 4.],
#                    [260., 1160., 3.]])
#
#BASELINK
#secondary = np.array([[610., 560., 4.],
#                      [610., -560., 6.],
#                      [390., -560., 7.],
#                      [390., 560., 2.]])

#Trying points
#primaryP = np.array([[0.05,0.05,0.15,1]])
#primaryP = np.array([[0,0,0,1]])
##point 1
#primaryP = np.array([[0.081, 0.097, 0.209,1]])
##point 2
#primaryP = np.array([[0.101, -0.048, 0.207,1]])
#point 340,45,34,19
#primaryP = np.array([[0.038, 0.018, 0.269,1]])
#point needle 0 0 0 0
#primaryP = np.array([[0.061, 0.006, 0.265,1]])

primaryP = np.array([[-0.000183651,0.00254228,0.315878,1]])

### try outs
#primaryP = np.array([[0,0,0.05,1]])



#primary = np.array([[0.05,0.05,0.15],
#                    [-0.05, 0.05, 0.15],
#                    [0.05, -0.05, 0.15],
#                    [-0.05, -0.05, 0.05]])
#
#secondary = np.array([[0.05,0.05, 0.05],
#                      [-0.05, 0.05, 0.05],
#                      [0.05, -0.05, 0.05],
#                      [-0.05, -0.05, -0.05]])

secondary = np.array([[-0.043, 0.042, 0.201],
                    [-0.034, -0.028, 0.201],
                    [0.113, -0.01, 0.202],
                    [0.061, 0.006, 0.265]])

primary = np.array([[0.0716758, -0.0404695, 0.2245],
                      [0.0769076, 0.0293347, 0.2245],
                      [-0.0716764, 0.0404695, 0.2245],
                      [0.0318683, 0.00708969, 0.306906]])

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
transformP= np.dot(primaryP, A)


print(A)
print("Target:")
print(secondary)
print("Result:")
print(transform(primary))
print("Result point:")
print(transformP)
print("Max error:", np.abs(secondary - transform(primary)).max())