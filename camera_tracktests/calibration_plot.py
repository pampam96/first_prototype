#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 07:03:22 2020

@author: marcey
"""
import matplotlib.pyplot as plt

x_rotation=[-2,-3,-3,-3,-3,-3,-3,-3,-3,-3,-7,-3,-3,-3,-3,-3,-3]
x_top=[-2,-2,0,-3,-2,-2,-2,-2,-2,-2,-2,0,-2,-2,-2,0,-2]
x_bottom=[-3,-3,-1,-3,-3,0,0,-3,-3,-1,-3,-3,-3,-3,-3,-3,-3]
x_middle=[-2,-2,-3,-3,-2,-2,-2,-2,-2,-2,-2,-3,-1,-2,0,0,-2]
y=[]

for i in range(len(x_rotation)):
        y.append(i)

#print(len(x_rotation),len(x_top),len(x_bottom),len(x_middle))

#figure4
plt.figure()
#plt.scatter(x2,y2,c='blue', s=2)
plt.scatter(y,x_rotation,c='blue', s=2)
plt.xlabel('Steps left to reach the extreme')
plt.ylabel('Iteration number')
plt.title('Calibration Rotation')
#plt.legend()
plt.show()

#figure4
plt.figure()
#plt.scatter(x2,y2,c='blue', s=2)
plt.scatter(y,x_top,c='red',s=2)
plt.xlabel('Steps left to reach the extreme')
plt.ylabel('Iteration number')
plt.title('Calibration top side translation')
#plt.legend()
plt.show()

#figure4
plt.figure()
#plt.scatter(x2,y2,c='blue', s=2)
plt.scatter(y,x_bottom,c='red',s=2)
plt.xlabel('Steps left to reach the extreme')
plt.ylabel('Iteration number')
plt.title('Calibration bottom side translation')
#plt.legend()
plt.show()

#figure4
plt.figure()
#plt.scatter(x2,y2,c='blue', s=2)
plt.scatter(y,x_middle,c='red',s=2)
plt.xlabel('Steps left to reach the extreme')
plt.ylabel('Iteration number')
plt.title('Calibration middle translation')
#plt.legend()
plt.show()