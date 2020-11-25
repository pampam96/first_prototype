#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 11:15:23 2020

@author: marcey
"""
import numpy as np

####Kabsch algorithm

#primary = np.array([[40., 1160., 1.],
#                    [40., 40., 5.],
#                    [260., 40., 4.],
#                    [260., 1160., 3.]])
#
#secondary = np.array([[610., 560., 4.],
#                      [610., -560., 6.],
#                      [390., -560., 7.],
#                      [390., 560., 2.]])

#primary = np.array([[0.05,0.05,0.15],
#                    [-0.05,0.05, 0.15],
#                    [0.05, -0.05, 0.15],
#                    [-0.05, -0.05, 0.05]])
#
#secondary = np.array([[0.05,0.05, 0.05],
#                      [-0.05, 0.05, 0.05],
#                      [0.05, -0.05, 0.05],
#                      [-0.05, 0.05, -0.05]])
#
#primaryP = np.array([[0.05,0.05,0.15,1]])

#Trying points
#primaryP = np.array([[0.05,0.05,0.15,1]])
#primaryP = np.array([[0,0,0,1]])
##point 1
#primaryP = np.array([[0.081, 0.097, 0.209,1]])
#primaryP = np.array([[0.081, 0.097, 0.209]])
##point 2
#primaryP = np.array([[0.101, -0.048, 0.207,1]])
#primaryP = np.array([[0.101, -0.048, 0.207]])
#point 340,45,34,19
#primaryP = np.array([[0.038, 0.018, 0.269,1]])
#primaryP = np.array([[0.038, 0.018, 0.269]])
#point needle 0 0 0 0
#primaryP = np.array([[0.061, 0.006, 0.265,1]])
#primaryP = np.array([[0.061, 0.006, 0.265]])

### try outs
#primaryP = np.array([[0,0,0,1]])
#primaryP = np.array([[0,0.5,0]])


#### REAL LIFE POINT
primary = np.array([[-0.043, 0.042, 0.201], 
                    [-0.034, -0.028, 0.201],
                    [0.113, -0.01, 0.202],
                    [-0.011, -0.063, 0.206],
                    [0.105, 0.059, 0.204],
                    [0.101, -0.048, 0.1175],
                    [-0.011, -0.063, 0.11649999999999999]])

#### SIMULATION POINT
secondary = np.array([[0.0716758, -0.0404695, 0.2245],
                      [0.0769076, 0.0293347, 0.2245],
                      [-0.0716764, 0.0404695, 0.2245],
                      [0.0602721, 0.0657678, 0.2295],
                      [-0.0769076, -0.0293347, 0.2245],
                      [-0.0500323, 0.0738573, 0.14],
                      [0.0602715, 0.0657678, 0.14]])



pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))])
pad2 = lambda x: np.vstack([x, [1, 1, 1, 1]])
unpad = lambda x: x[:,:-1]

#RIGID TRANSFORMS 

# 1 : Find centroid of both datasets 
#mean across column 0, rows 1
def transform_rigid(primary,secondary):
    primary=primary.T
    secondary=secondary.T
    
    primaryCentroid=np.mean(primary, axis=1)
    #print("mean1",primaryCentroid)
    secondaryCentroid=np.mean(secondary, axis=1)
    #print("mean2",secondaryCentroid)

    #primaryCentroid reshape
    primaryCentroid = primaryCentroid.reshape(-1, 1)
    secondaryCentroid = secondaryCentroid.reshape(-1, 1)

    # 2 : Bring both dataset to the origin then find the optimal rotation R

    # Here we are bringing centroid to origin to remove translation component
    primaryOrigin=(primary-primaryCentroid)
    print("primaryOrigin",primary-primaryCentroid)

    secondaryOrigin=(secondary-secondaryCentroid)
    print("secondaryOrigin",secondaryOrigin)

    ### This is our E
    H = primaryOrigin @ np.transpose(secondaryOrigin)

    U,S,V=np.linalg.svd(H)

    R= V.T @ U.T
    #print(R)
    
    # special reflection case
    if np.linalg.det(R) < 0:
        #print("det(R) < R, reflection detected!, correcting for it ...")
        V[2,:] *= -1
        R = V.T @ U.T

    T=-R@ primaryCentroid + secondaryCentroid
    
    return R, T
    
res_R, res_t=transform_rigid(primary,secondary)

secondary_trans=(res_R@primary.T) + res_t

secondaryP_trans=(res_R@primaryP.T) + res_t

    
    
print("Points B")
print(secondary)
print("")
    
print("Points B transformed")
print(secondary_trans.T)
print("")
    
print("Points B transformed")
print(secondaryP_trans.T)
print("")
    