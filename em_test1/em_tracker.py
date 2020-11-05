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
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pytransform3d.rotations import *

#
x = []
y = []
z = []
index=[]

with open('9_11_09_48_18_sm.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x.append(round(float(row[0]),0)/1000)
        y.append(round(float(row[1]),0)/1000)
        z.append(round(-float(row[2]),0)/1000)
        index.append(i)

# Creating figure 
#fig = plt.figure(figsize = (10, 7)) 
#ax = plt.axes(projection ="3d") 
        
# creating transformation figure
plt.figure(figsize=(12, 5))
try:
    ax = plt.subplot(121, projection="3d", aspect="equal")
except NotImplementedError:
    # HACK: workaround for bug in new matplotlib versions (ca. 3.02):
    # "It is not currently possible to manually set the aspect"
    ax = plt.subplot(121, projection="3d")
  
# Creating plot 
ax.scatter(x, y, z, color = "green"); 
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
        x2.append(round(float(row[0]),0)/1000)
        y2.append(round(float(row[1]),0)/1000)
        z2.append(round(-float(row[2]),0)/1000)
        index2.append(i)

# Creating figure 
  
# Creating plot 
ax.scatter(x2, y2, z2, color = "blue"); 
plt.title("simple 3D scatter plot") 
#  
#show plot 

plt.show()


x3 = []
y3 = []
z3 = []
index3=[]

with open('9_11_10_01_21_cm.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x3.append(round(float(row[0]),0)/1000)
        y3.append(round(float(row[1]),0)/1000)
        z3.append(round(-float(row[2]),0)/1000)
        index2.append(i)

  
# Creating plot 
ax.scatter(x3, y3, z3, color = "red"); 
plt.title("simple 3D scatter plot") 
#  
#show plot 
plt.show()


x4 = []
y4 = []
z4 = []
index4=[]

with open('9_11_10_04_00_points.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x4.append(round(float(row[0]),0)/1000)
        y4.append(round(float(row[1]),0)/1000)
        z4.append(round(-float(row[2]),0)/1000)
        index4.append(i)

  
# Creating plot 
#how they were beforeee
#ax.scatter3D(x4, y4, z4, color = "black"); 
ax.scatter(x4, y4, z4, color = "black"); 
plt.title("simple 3D scatter plot") 
#  
#show plot 

x5 = []
y5 = []
z5 = []
rx = []
ry = []
rz = []
rw = []
index5=[]

##340,45,34,19
#with open('9_11_10_40_02_points.txt','r') as csvfile:
#    
##0,45,34,19
#with open('9_11_10_41_37_points.txt','r') as csvfile:
#
##0,0,0,19
#with open('9_11_10_44_07_points.txt','r') as csvfile:
#    
##0,0,0,0
#with open('9_11_10_44_47_points.txt','r') as csvfile:
#    
##0,0,112,112
#with open('9_11_10_46_20_points.txt','r') as csvfile:
#    
##0,0,112,112 to 340,0,112,112
#with open('9_11_10_46_20_points.txt','r') as csvfile:
#    
##340,0,112,112 to 340,0,0,0
#with open('9_11_10_48_59_points.txt','r') as csvfile:
#    
##340,0,0,0 to 340,90,0,0
#with open('9_11_10_50_54_points.txt','r') as csvfile:
#    
##340,90,0,0 to 340,90,112,112
#with open('9_11_10_50_54_points.txt','r') as csvfile:
#
##340,90,0,0 to 340,90,112,112
#with open('9_11_10_52_22_points.txt','r') as csvfile:
#    
##340,90,112,112 to 0,90,112,112
#with open('9_11_10_53_29_points.txt','r') as csvfile:
    
#0,90,112,112 to 0,90,0,0
#with open('9_11_10_56_26_points.txt','r') as csvfile:

#0,90,0,0 to 0,45,0,0
#with open('9_11_10_58_04_points.txt','r') as csvfile:

#0,45,0,0 to 170,45,0,0
#with open('9_11_11_00_00_points.txt','r') as csvfile:

#170,45,0,0 to 170,45,30,0 by 3rd changing by 10
#with open('9_11_11_02_47_points.txt','r') as csvfile:

#170,45,0,0 to 170,45,56,56
#with open('9_11_11_06_53_points.txt','r') as csvfile:

#170,45,56,56 to 170,45,56,56-50-45-40
#with open('9_11_11_08_29_points.txt','r') as csvfile:

#degrees

#169,45,0,0 to 169,45,29,16 90deg
#with open('9_11_15_54_36_points.txt','r') as csvfile:

#169,45,29,16 to 169,45,07,16 8/20deg
#with open('9_11_16_00_00_points.txt','r') as csvfile:

#169,45,7,16 to 169,45,54,16 7-15-24-34-54 -20deg
#with open('9_11_16_07_20_points.txt','r') as csvfile:

#169,45,54,16 to 340,45,54,16 to 0,45,54,16 -20deg
#with open('9_11_16_12_49_points.txt','r') as csvfile:

#0,45,07,16
#with open('9_11_16_18_14_points.txt','r') as csvfile:

#340,45,60,16 to 0,45,60,16 -36deg
#with open('9_11_16_29_46_points.txt','r') as csvfile:


    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x5.append(round(float(row[0]),0)/1000)
        y5.append(round(float(row[1]),0)/1000)
        z5.append(round(-float(row[2]),0)/1000)
        rx.append(float(row[3]))
        ry.append(float(row[4]))
        rz.append(float(row[5]))
        rw.append(float(row[6]))
        index5.append(i)

  
# Creating plot 
ax.scatter(x5, y5, z5, color = "pink"); 
plt.title("simple 3D scatter plot") 

ax.scatter(x5[-1], y5[-1], z5[-1], color = "red"); 
plt.title("simple 3D scatter plot") 

plt.show()
R1=np.eye(3)
#ax=plot_basis(R=np.eye(3), ax_s=4)

#
p = np.array([x5[0], y5[0], z5[0]])
##q = quaternion_from_axis_angle(a)
q=[rx[0],ry[0],rz[0],rw[0]]
#R = matrix_from_quaternion(q)
#plot_basis(ax, R, p)
##  
##show plot 
#
#p = np.array([-1.0, -1.0, -1.0])
#q = quaternion_from_axis_angle(a)
#q=[-0.05200234428048134,-0.0014000632800161839,0.044702015817165375,0.9976449608802795]
R = matrix_from_quaternion(q)
#nw=plot_basis(ax, R, p)

plt.show()