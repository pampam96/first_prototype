#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 11:15:23 2020

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


pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))])
unpad = lambda x: x[:,:-1]

#mean across column 0, rows 1
primaryCentroid=np.mean(primary, axis=0)
secondaryCentroid=np.mean(secondary, axis=0)

#primaryCentroid.shape to check size

primaryOrigin=(primary-primaryCentroid).conj().T
secondaryOrigin=(secondary-secondaryCentroid).conj().T

W = np.identity(primaryOrigin.shape[1])

S = primaryOrigin.dot(W).dot(secondaryOrigin.conj().T)

U,S,V=np.linalg.svd(S)

#Q=np.identity(V.shape[1])

XX=V.dot(U.conj().T)

Q=np.linalg.det(XX)

R= V.dot(Q).dot(U.T)
#print(R)

T=secondaryCentroid.conj().T - R.dot(primaryCentroid.conj().T)
#print(T)

TransM=np.identity(4)

for i in range(0,3):
    for j in range(0,3):
        #print(i)
        TransM[i,j]=R[i,j]
        TransM[3,i]=T[i] 

#primaryC=pad(primary) 
#primaryC=primaryC.conj().T
#primaryB=primaryC.conj().T
#print(primaryC)   
#print(primaryB)   

transform = lambda x: unpad(np.dot(pad(x), TransM))
#TransformedP=TransM.dot(primary)

print(transform(primary))
