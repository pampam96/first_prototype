#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
from scipy.spatial import distance
import csv

##printing pointsss

#### REAL LIFE POINT EM TRACKER
primary = np.array([[-0.105, 0.06, 0.204], 
                    [-0.114, -0.01, 0.203],
                    [0.034, -0.028, 0.201],
                    [-0.1, -0.047, 0.205],
                    [0.048, 0.037, 0.202],
                    [-0.079, 0.096, 0.1185],
                    [-0.1, -0.047, 0.1155]])

#### SIMULATION POINT
secondary = np.array([[0.0716758, -0.0404695, 0.2245],
                      [0.0769076, 0.0293347, 0.2245],
                      [-0.0716764, 0.0404695, 0.2245],
                      [0.0602721, 0.0657678, 0.2295],
                      [-0.0769076, -0.0293347, 0.2245],
                      [0.0500323, -0.0738573, 0.14],
                      [0.0602715, 0.0657678, 0.14]])



######DIFERENT ANGLES
#primaryP = np.array([[0.038,0.018, 0.269]]) #at 340,45,34,19
#primaryP = np.array([[0.033, 0.011, 0.27]]) #at 0,45,34,19
#primaryP = np.array([[0.061, 0.006, 0.265]]) #at 0,0,0,19

###EM tracker points

# to check the transform
#primaryT1 = np.array([[0.012, -0.064, 0.205]]) #at 0,0,0,0

primaryP1 = np.array([[-0.062 , 0.009 , 0.264]]) #at 0,0,0,0
primaryP2 = np.array([[-0.008 , -0.003 , 0.263]]) #at 0,90,0,0
primaryP3 = np.array([[-0.072 , -0.061 , 0.264]]) #at 0,0,112,112
primaryP4 = np.array([[-0.018 , -0.072 , 0.262]]) #at 0,90,112,112
primaryP5 = np.array([[-0.008 , 0.093 , 0.266]]) #at 340,0,112,112
primaryP6 = np.array([[-0.066 , 0.092 , 0.266]]) #at 340,90,112,112
primaryP7 = np.array([[-0.064 , 0.022 , 0.265]]) #at 340,90,0,0
primaryP8 = np.array([[-0.007 , 0.024 , 0.265]]) #at 340,0,0,0
#primaryP9 = np.array([[-0.044 , 0.012 , 0.265]]) #at 170,45,0,0
#primaryP10 = np.array([[0.0, 0.009, 0.275]]) #at 170,45,0,30
#primaryP11 = np.array([[-0.062, -0.005, 0.2654]]) #at 0,0,0,19
##print(primaryP)

#tracker_points = np.array([[0.061, 0.006, 0.265], 
#                    [0.006, -0.0, 0.265],
#                    [0.076 , -0.057 , 0.265],
#                    [0.016 , -0.069 , 0.265],
#                    [0.015 , 0.099 , 0.265],
#                    [0.072 , 0.095 , 0.265],
#                    [0.069 , 0.025 , 0.265],
#                    [0.011 , 0.028 , 0.265]])
#
#for j in range(8):
#    red=ax.scatter3D(tracker_points[j,0],tracker_points[j,1],tracker_points[j,2], color = "red"); #at 0,0,0,0
#primaryP = np.array(tracker_points[0])

#print(primaryP)
# Creating figure 
#fig = plt.figure(figsize = (10, 7)) 
#ax = plt.axes(projection ="3d") 
#  
## Creating plot 
#for point in primary:
#    ax.scatter3D(point[0], point[1], point[2], color = "green"); 
#ax.scatter3D(primaryP[0][0], primaryP[0][1], primaryP[0][2], color = "red");
#    
#    
#plt.title("EM Tracker") 
#ax.legend()
#ax.set_xlabel("x")
#ax.set_ylabel("y")
#ax.set_zlabel("z")


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

res_R, res_t=transform_rigid(primary, secondary)

secondary_trans=(res_R@primary.T) + res_t

#secondaryT1_trans=(res_R@primaryT1.T) + res_t
secondaryP=[]
secondaryP.append((res_R@primaryP1.T) + res_t)
secondaryP.append((res_R@primaryP2.T) + res_t)
secondaryP.append((res_R@primaryP3.T) + res_t)
secondaryP.append((res_R@primaryP4.T) + res_t)
secondaryP.append((res_R@primaryP5.T) + res_t)
secondaryP.append((res_R@primaryP6.T) + res_t)
secondaryP.append((res_R@primaryP7.T) + res_t)
secondaryP.append((res_R@primaryP8.T) + res_t)

#secondaryP2_trans=(res_R@primaryP2.T) + res_t
#secondaryP3_trans=(res_R@primaryP3.T) + res_t
#secondaryP4_trans=(res_R@primaryP4.T) + res_t
#secondaryP5_trans=(res_R@primaryP5.T) + res_t
#secondaryP6_trans=(res_R@primaryP6.T) + res_t
#secondaryP7_trans=(res_R@primaryP7.T) + res_t
#secondaryP8_trans=(res_R@primaryP8.T) + res_t
#secondaryP10_trans=(res_R@primaryP10.T) + res_t


# Creating figure 
fig = plt.figure(figsize = (10, 7)) 
ax = plt.axes(projection ="3d") 
  
# Creating plot 
#for i,point in enumerate(secondary):
#    ax.scatter3D(-point[0], -point[1], point[2], color = "green");
#    secondary_flipped[i]=[-point[0], -point[1], point[2]]
print(secondaryP)
#print(secondaryP[0][1][0])

file="em_tracker2.txt"
for i, point in enumerate(secondaryP):
    blue=ax.scatter3D(point[0],point[1],point[2], color = "blue");
    test=[point[0][0],point[1][0],point[2][0]]
    test=str(test).strip('[]')
    with open(file, "a") as myfile:
        myfile.write(test+"\n")
    

#blue=ax.scatter3D(secondaryP2_trans[0],secondaryP2_trans[1],secondaryP2_trans[2], color = "blue");
#blue=ax.scatter3D(secondaryP1_trans[0],secondaryP1_trans[1],secondaryP1_trans[2], color = "blue");
#blue=ax.scatter3D(secondaryP3_trans[0],secondaryP3_trans[1],secondaryP3_trans[2], color = "blue");
#blue=ax.scatter3D(secondaryP4_trans[0],secondaryP4_trans[1],secondaryP4_trans[2], color = "blue");
#blue=ax.scatter3D(secondaryP5_trans[0],secondaryP5_trans[1],secondaryP5_trans[2], color = "blue");
#blue=ax.scatter3D(secondaryP6_trans[0],secondaryP6_trans[1],secondaryP6_trans[2], color = "blue");
#blue=ax.scatter3D(secondaryP7_trans[0],secondaryP7_trans[1],secondaryP7_trans[2], color = "blue");
#blue=ax.scatter3D(secondaryP8_trans[0],secondaryP8_trans[1],secondaryP8_trans[2], color = "blue");
##ax.scatter3D(secondaryP10_trans[0],secondaryP10_trans[1],secondaryP10_trans[2], color = "red");

#file="em_tracker2.txt"
#    test=[x,y,z,rx,ry,rz,rw]
#    test=str(test).strip('[]')
#    with open(file, "a") as myfile:
#        myfile.write(test+"\n")
#### SIMULATION POINTS


simulation_points = np.array([[0.0318124, 0.00649151, 0.303736],
                    [-0.0305187, 0.0110839, 0.303736], 
                    [0.0370463, 0.076208, 0.303736],
                    [-0.025279, 0.0808773, 0.303736],
                    [-0.0256637, -0.0808036, 0.303736],
                    [0.0366114, -0.0765, 0.304332],
                    [0.031789, -0.00660496, 0.304332],
                    [-0.030558, -0.0109749, 0.303736]])
    
#no 3 part
joint_values = np.array([[0,0,0,0], 
                    [0,90,0,0],
                    [0,0,112,112],
                    [0,90,112,112],
                    [340,0,112,112],
                    [340,90,112,112],
                    [340,90,0,0],
                    [340,0,0,0]])


#j=2
file="em_trackersim.txt"
file2="distances.txt"
for j in range(8):
    red=ax.scatter3D(simulation_points[j,0],simulation_points[j,1],simulation_points[j,2], color = "red"); #at 0,0,0,0
    point_tracker=(secondaryP[j][0][0],secondaryP[j][1][0],secondaryP[j][2][0])
    point_sim=(simulation_points[j][0],simulation_points[j][1],simulation_points[j][2])
    
    print("point_tracker",point_tracker)
    print("point_sim",point_sim)
    xdst = distance.euclidean(point_tracker[0],point_sim[0])*1000
    ydst = distance.euclidean(point_tracker[1],point_sim[1])*1000
    zdst = distance.euclidean(point_tracker[2],point_sim[2])*1000
    print("distances",xdst,ydst,zdst)
    test=[simulation_points[j,0],simulation_points[j,1],simulation_points[j,2]]
    test=str(test).strip('[]')
    with open(file, "a") as myfile:
        myfile.write(test+"\n")
    
    test2=[xdst,ydst,zdst]
    test2=str(test2).strip('[]')
    with open(file2, "a") as myfile:
        myfile.write(test2+"\n")
        
ax.scatter3D(0,0,0, color = "red"); #at 0,0,0,0

#title=(joint_values[j,0],joint_values[j,1],joint_values[j,2],joint_values[j,3])
#title=str(title).strip('[]') 
#plt.title(f"Simulation at {title}") 
plt.title("Workspace extreme points in simulation vs em tracker measurements") 


ax.legend((blue, red), ('Em tracker data', 'Simulation Data'))
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

#a1 = (secondaryP8_trans[0],secondaryP8_trans[1],secondaryP8_trans[2])
#b1 = (simulation_points[j,0],simulation_points[j,1],simulation_points[j,2])
##Distance measured::
#for i in range (3):
#    xdst = distance.euclidean(a1[i], b1[i])
#    print("dst",xdst) 



#print("transformed point",secondaryP10_trans[0],secondaryP10_trans[1],secondaryP10_trans[2])

