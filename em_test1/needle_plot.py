#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 09:05:55 2020

@author: marcey
"""
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d 
import numpy as np
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pytransform3d.rotations import *
from scipy.spatial import distance

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')



S_n1=(-0.000183651,0.00254228,0.315878)
T_n1=(0.05576089, -0.00955985,0.31229747)



ax.scatter(S_n1[0], S_n1[1], S_n1[2], color = "green"); 
ax.scatter(T_n1[0], T_n1[1], T_n1[2], color = "purple"); 

plt.show()