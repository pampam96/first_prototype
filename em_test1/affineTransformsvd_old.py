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
primaryP = np.array([[0.081, 0.097, 0.209,1]])
##point 2
#primaryP = np.array([[0.101, -0.048, 0.207,1]])
#point 340,45,34,19
#primaryP = np.array([[0.038, 0.018, 0.269,1]])
#point needle 0 0 0 0
#primaryP = np.array([[0.061, 0.006, 0.265,1]])

### try outs
#primaryP = np.array([[0,0,0,1]])

primary = np.array([[-0.043, 0.042, 0.201],
                    [-0.034, -0.028, 0.201],
                    [0.113, -0.01, 0.202],
                    [0.0318683, 0.00708969, 0.306906]])

secondary = np.array([[0.0716758, -0.0404695, 0.2245],
                      [0.0769076, 0.0293347, 0.2245],
                      [-0.0716764, 0.0404695, 0.2245],
                      [0.061, 0.006, 0.265]])



pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))])
pad2 = lambda x: np.vstack([x, [1, 1, 1, 1]])
unpad = lambda x: x[:,:-1]

# 1 : Find centroid of both datasets

#mean across column 0, rows 1
primaryCentroid=np.mean(primary, axis=0)
#print("mean1",primaryCentroid)
secondaryCentroid=np.mean(secondary, axis=0)
#print("mean2",secondaryCentroid)

#primaryCentroid.shape to check size

# 2 : Bring both dataset to the origin then find the optimal rotation R

# Here we are bringing centroid to origin to remove translation component
primaryOrigin=(primary-primaryCentroid)
#primaryOrigin=primaryOrigin.conj().T
print("primaryOrigin",primary-primaryCentroid)

secondaryOrigin=(secondary-secondaryCentroid)
secondaryOrigin=secondaryOrigin.T
#secondaryOrigin=secondaryOrigin.conj().T
print("secondaryOrigin",secondaryOrigin)


#W = np.identity(primaryOrigin.shape[1])

### This is our E
#S = primaryOrigin.dot(W).dot(secondaryOrigin.conj().T)
H=primaryOrigin.dot(secondaryOrigin)

U,S,V=np.linalg.svd(H)

#Q=np.identity(V.shape[1])

#XX=V.dot(U.conj().T)

#Q=np.linalg.det(XX)

# Have found the rotation
print("v column",V[:, 2])
R= V.dot(U.T)
detR=np.linalg.det(R)
if detR<0:
    print("V",V)
print("R",R)
print("detR",detR)
#
#T=secondaryCentroid.conj().T - R.dot(primaryCentroid.conj().T)
#
#TransM=np.identity(4)
#
#for i in range(0,3):
#    for j in range(0,3):
#        #print(i)
#        TransM[i,j]=R[i,j]
#        TransM[3,i]=T[i] 
#
#
#primaryC=primary.conj().T
#primaryC=pad2(primaryC)
#print(primaryC)
#
#
#transform = lambda x: unpad(np.dot(pad(x), TransM))
#transformP= np.dot(primaryP, TransM)
##TransformedP=TransM.dot(primaryC)
##print(primary)
#print("Target:")
#print(secondary)
#print("Result:")
#print(transform(primary))
#print("Result point:")
#print(transformP)
##print(TransformedP)
##print("transformation Matrix")
##print(TransM)
