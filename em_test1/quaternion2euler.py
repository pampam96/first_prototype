#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 09:45:19 2020

@author: marcey
"""
import math
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d 
import numpy as np
import csv

x = []
y = []
z = []
rx = []
ry = []
rz = []
rw = []
index=[]

with open('9_11_09_48_18_sm.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x.append(round(float(row[0]),0))
        y.append(round(float(row[1]),0))
        z.append(round(-float(row[2]),0))
        rx.append(round(float(row[3]),0))
        ry.append(round(float(row[4]),0))
        rz.append(round(float(row[5]),0))
        rw.append(round(float(row[6]),0))
        index.append(i)
        
def quaternion_to_euler(x, y, z, w):

    t0 = +2.0 * (w * x + y * z)
    t1 = +1.0 - 2.0 * (x * x + y * y)
    roll = math.atan2(t0, t1)
    t2 = +2.0 * (w * y - z * x)
    t2 = +1.0 if t2 > +1.0 else t2
    t2 = -1.0 if t2 < -1.0 else t2
    pitch = math.asin(t2)
    t3 = +2.0 * (w * z + x * y)
    t4 = +1.0 - 2.0 * (y * y + z * z)
    yaw = math.atan2(t3, t4)
    return [yaw, pitch, roll]


rotation=quaternion_to_euler(rx[i], ry[i], rz[i], rw[i])
print(rotation)
