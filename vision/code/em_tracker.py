#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 14:55:02 2020

@author: marcey
"""

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d 
import numpy as np
import csv

x = []
y = []
z = []
index=[]

with open('9_11_09_48_18_sm.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x.append(round(float(row[0]),0))
        y.append(round(float(row[1]),0))
        z.append(round(float(row[2]),0))
        index.append(i)

#fig = plt.figure()
#ax = fig.gca(projection='3d')

# Make the grid
#x, y, z = np.meshgrid(np.arange(-0.8, 1, 0.2),
#                      np.arange(-0.8, 1, 0.2),
#                      np.arange(-0.8, 1, 0.8))

# Make the direction data for the arrows

#u = np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
#v = -np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
#w = (np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) *
#     np.sin(np.pi * z))
#ax.quiver(x, y, z, u, v, w, length=0.1, normalize=True)

# Creating figure 
fig = plt.figure(figsize = (10, 7)) 
ax = plt.axes(projection ="3d") 
  
# Creating plot 
ax.scatter3D(x, y, z, color = "green"); 
plt.title("simple 3D scatter plot") 
#  
#show plot 

plt.show()

x2 = []
y2 = []
z2 = []
index2=[]

with open('9_11_09_53_40_smr.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x2.append(round(float(row[0]),0))
        y2.append(round(float(row[1]),0))
        z2.append(round(float(row[2]),0))
        index2.append(i)

#fig = plt.figure()
#ax = fig.gca(projection='3d')

# Make the grid
#x, y, z = np.meshgrid(np.arange(-0.8, 1, 0.2),
#                      np.arange(-0.8, 1, 0.2),
#                      np.arange(-0.8, 1, 0.8))

# Make the direction data for the arrows

#u = np.sin(np.pi * x) * np.cos(np.pi * y) * np.cos(np.pi * z)
#v = -np.cos(np.pi * x) * np.sin(np.pi * y) * np.cos(np.pi * z)
#w = (np.sqrt(2.0 / 3.0) * np.cos(np.pi * x) * np.cos(np.pi * y) *
#     np.sin(np.pi * z))
#ax.quiver(x, y, z, u, v, w, length=0.1, normalize=True)

# Creating figure 
  
# Creating plot 
ax.scatter3D(x2, y2, z2, color = "blue"); 
plt.title("simple 3D scatter plot") 
#  
#show plot 

plt.show()