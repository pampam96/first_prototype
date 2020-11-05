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
from scipy.spatial import distance

#
x = []
y = []
z = []
index=[]

def transform(x,y,z):
    
    primaryP = np.array([[x,y,z,1]])


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
    return transformP

with open('9_11_09_48_18_sm.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x.append(round(-float(row[0]),0)/1000)
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
ax.scatter(x[0], y[0], z[0]+0.01, color = "purple"); #Marker 2 at 0
ax.scatter(x[659], y[659], z[659]+0.01, color = "brown"); #Marker 2 at 112
print("Marker 2 at 0",x[0], y[0], z[0])
print("Marker 2 at 112",x[659], y[659], z[659])
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
        x2.append(round(-float(row[0]),0)/1000)
        y2.append(round(float(row[1]),0)/1000)
        z2.append(round(-float(row[2]),0)/1000)
        index2.append(i)

# Creating figure 
  
# Creating plot 
ax.scatter(x2, y2, z2, color = "blue"); 
ax.scatter(x2[0], y2[0], z2[0]+0.01, color = "yellow");  #Marker 1 at 0
print("Marker 1 at 0",x2[0], y2[0], z2[0])
ax.scatter(x2[458], y2[458], z2[458]+0.01, color = "pink"); #Marker 1 at 112
print("Marker 1 at 112",x2[458], y2[458], z2[458])
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
        x3.append(round(-float(row[0]),0)/1000)
        y3.append(round(float(row[1]),0)/1000)
        z3.append(round(-float(row[2]),0)/1000)
        index2.append(i)

  
# Creating plot 
ax.scatter(x3, y3, z3, color = "red");
#ax.scatter(x3[0], y3[0], z3[0]+0.01, color = "blue"); 
#ax.scatter(x3[534], y3[534], z3[534]+0.01, color = "purple"); 
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
        x4.append(round(-float(row[0]),0)/1000)
        y4.append(round(float(row[1]),0)/1000)
        z4.append(round(-float(row[2]),0)/1000)
        index4.append(i)
        
# Creating plot 
#how they were beforeee
#ax.scatter3D(x4, y4, z4, color = "black"); 

#p1 = (x4[4], y4[4], z4[4])
#p2 = (x4[506], y4[506], z4[506]) 
#p3  = (x4[880], y4[880], z4[880])  
#ax.scatter(x4, y4, z4, color = "black"); 
#First one not flipped second one for flipped in x
ax.scatter(x4[880], y4[880], z4[880]-0.0895, color = "black"); #p3 #p4
ax.scatter(x4[880], y4[880], z4[880], color = "black"); #p3 #p4
print("p4",x4[880], y4[880], z4[880])
ax.scatter(x4[4], y4[4], z4[4]-0.0895, color = "blue"); #p2 #p1
ax.scatter(x4[880], y4[880], z4[880], color = "black"); #p3 #p4
print("p1",x4[4], y4[4], z4[4]-0.0895)
ax.scatter(x4[506], y4[506], z4[506]-0.0895, color = "red"); #p1 #p3
ax.scatter(x4[506], y4[506], z4[506], color = "red"); #p1 #p3
print("p3",x4[506], y4[506], z4[506])
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
with open('9_11_10_44_47_points.txt','r') as csvfile:
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

#0,45,33,80 to 340,45,33,80 
#with open('9_11_16_29_46_points.txt','r') as csvfile:


    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x5.append(round(-float(row[0]),0)/1000)
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

#ax.scatter(x5[-1], y5[-1], z5[-1], color = "red");
#ax.scatter(x5[0], y5[0], z5[0], color = "brown");
#ax.scatter(x5[353], y5[353], z5[353]+0.1, color = "brown");
#ax.scatter(0,0,0, color = "red");
print(x5[-1],",", y5[-1],",", z5[-1],",","needle") 
print(x5[0],",", y5[0],",", z5[0],",","needle at 0") 
print(x5[353],",", y5[353],",", z5[353],",","needle at 0") 
plt.title("Chosen Points From the Em tracker data") 

ax.legend()
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")


#######################################################################################
####### second figure COMBINED PLOTSSS

# Creating figure 
fig = plt.figure(figsize = (10, 7)) 
ax = plt.axes(projection ="3d") 

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
with open('9_11_10_44_47_points.txt','r') as csvfile:
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

#0,45,33,80 to 340,45,33,80 
#with open('9_11_16_29_46_points.txt','r') as csvfile:


    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x5.append(round(-float(row[0]),0)/1000)
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
ax.scatter(x5[0], y5[0], z5[0], color = "brown");
ax.scatter(x5[353], y5[353], z5[353]+0.1, color = "brown");
#ax.scatter(0,0,0, color = "red");
print(x5[-1],",", y5[-1],",", z5[-1],",","needle") 
print(x5[0],",", y5[0],",", z5[0],",","needle at 0") 
print(x5[353],",", y5[353],",", z5[353],",","needle at 0") 
plt.title("Chosen Points From the Em tracker data") 

ax.legend()
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")



####### SECOND FIGURE OTHER PLOT COMBINED


x7 = []
y7 = []
z7 = []
rx7 = []
ry7 = []
rz7 = []
rw7 = []
index7=[]

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
with open('9_11_11_00_00_points.txt','r') as csvfile:

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

#0,45,33,80 to 340,45,33,80 
#with open('9_11_16_29_46_points.txt','r') as csvfile:


    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x7.append(round(-float(row[0]),0)/1000)
        y7.append(round(float(row[1]),0)/1000)
        z7.append(round(-float(row[2]),0)/1000)
        rx7.append(float(row[3]))
        ry7.append(float(row[4]))
        rz7.append(float(row[5]))
        rw7.append(float(row[6]))
        index7.append(i)

  
# Creating plot 
ax.scatter(x7, y7, z7, color = "green"); 
plt.title("simple 3D scatter plot") 

ax.scatter(x7[-1], y7[-1], z7[-1]+0.1, color = "red");
ax.scatter(x7[0], y7[0], z7[0]+0.1, color = "red");
ax.scatter(x7[353], y7[353], z7[353]+0.1, color = "brown");
#ax.scatter(0,0,0, color = "red");
print(x7[-1],",", y7[-1],",", z7[-1],",","needle") 
print(x7[0],",", y7[0],",", z7[0],",","needle at 0") 
print(x7[353],",", y7[353],",", z7[353],",","needle at 0") 

plt.title("Needle with joints at 169,45,0,0 to 169,45,29,16 90deg") 

ax.legend()
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")


####### SECOND FIGURE OTHER PLOT COMBINED


x8 = []
y8 = []
z8 = []
rx8 = []
ry8 = []
rz8 = []
rw8 = []
index8=[]

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
with open('9_11_11_02_47_points.txt','r') as csvfile:

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

#0,45,33,80 to 340,45,33,80 
#with open('9_11_16_29_46_points.txt','r') as csvfile:


    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x8.append(round(-float(row[0]),0)/1000)
        y8.append(round(float(row[1]),0)/1000)
        z8.append(round(-float(row[2]),0)/1000)
        rx8.append(float(row[3]))
        ry8.append(float(row[4]))
        rz8.append(float(row[5]))
        rw8.append(float(row[6]))
        index8.append(i)

  
# Creating plot 
ax.scatter(x8, y8, z8, color = "purple"); 
plt.title("simple 3D scatter plot") 

ax.scatter(x8[-1], y8[-1], z8[-1]+0.01, color = "blue");
ax.scatter(x8[0], y8[0], z8[0]+0.01, color = "blue");
#ax.scatter(x8[353], y8[353], z8[353]+0.1, color = "brown");
print("needle 0,0,0,19",x8[-1], y8[-1], z8[-1])
print("needle 0,0,0,19",x8[0], y8[0], z8[0])
plt.title("Needle with joints at workspace of 340") 

ax.legend()
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

#td=transform(-0.000183651,0.00254228,0.315878)
#td=transform(-0.000389851,-0.00243381,0.31231)
#td=transform(0.0309715,-0.00487704,0.315878)
#td=transform(0.0371931,0.0771395,0.3083)
#td=transform(0.0371931,0.0771395,0.3083) #0,0,112,112
#td=transform(0.0319055,0.00730016,0.3083) #0,90,0,0
#td=transform(0.031896,0.00734023,0.3083) #0,0,0,0
#td=transform(0.0365534,-0.0774447,0.3083) #340,90,112,112
#td=transform(-0.0258045,-0.0816581,0.3083) #340,0,112,112
#td=transform(0.010089,0,0.310068) #340,0,112,112
#td=transform(-0.0250248,0.0819004,0.3083) #0,90,112,112
#td=transform(0.0365534,-0.0774447,0.3083) #340,90,112,112
td=transform(0.0327925,0.01915031,0.3083) #0,0,0,19
#print("td",td)
#ax.scatter(td[0][0],td[0][1],td[0][2], color = "blue");

plt.show()

#R1=np.eye(3)
#ax=plot_basis(R=np.eye(3), ax_s=4)
#
##
#p = np.array([x5[0], y5[0], z5[0]])
###q = quaternion_from_axis_angle(a)
#q=[rx[0],ry[0],rz[0],rw[0]]
#R = matrix_from_quaternion(q)
#plot_basis(ax, R, p)
##  
##show plot 
###
###p = np.array([-1.0, -1.0, -1.0])
###q = quaternion_from_axis_angle(a)
###q=[-0.05200234428048134,-0.0014000632800161839,0.044702015817165375,0.9976449608802795]
##R = matrix_from_quaternion(q)
###nw=plot_basis(ax, R, p)
##
#plt.show()
##
#
#needle=(x5[-1], y5[-1], z5[-1])
#
####X distance
#Nx = distance.euclidean(M1[0], needle[0])
#Ny= distance.euclidean(M1[1], needle[1])
#Nz= distance.euclidean(M1[2], needle[2])
#print(Nx,Ny,Nz)
#newXYZ=(-Nx+0.0744442,Nz+0.0845,-Ny+0.0351186)
#worldXYZ=(newXYZ[0],-newXYZ[2],newXYZ[1])
#print(worldXYZ)
#
#
####world coord tryout
#Marker=(0.0716758, -0.0404695, 0.2245)
#distance=(-Nx,-Ny,Nz)
#sim_N=(Marker[0]+distance[0],Marker[1]+distance[1],Marker[2]+distance[2])
#print(sim_N)