#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 19:51:18 2020

@author: marcey
"""


import numpy as np
import matplotlib.pyplot as plt
from pytransform3d.rotations import matrix_from_euler_xyz
from pytransform3d.transformations import transform_from, plot_transform
from pytransform3d.camera import make_world_grid, world2image
import csv


cam2world = transform_from(matrix_from_euler_xyz([np.pi - 1, 0.2, 0.2]),
                           [0.2, -1, 0.5])
focal_length = 0.0036
sensor_size = (0.00367, 0.00274)
image_size = (640, 480)

world_grid = make_world_grid()
image_grid = world2image(world_grid, cam2world, sensor_size, image_size,
                         focal_length)

###############

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

###############
plt.figure(figsize=(12, 5))
try:
    ax = plt.subplot(121, projection="3d", aspect="equal")
except NotImplementedError:
    # HACK: workaround for bug in new matplotlib versions (ca. 3.02):
    # "It is not currently possible to manually set the aspect"
    ax = plt.subplot(121, projection="3d")
ax.view_init(elev=30, azim=-70)
ax.set_xlim((-1, 1))
ax.set_ylim((-1, 1))
ax.set_zlim((-1, 1))
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
plot_transform(ax)
#plot_transform(ax, A2B=cam2world)
ax.set_title("Camera and world frames")

#ax=plot_basis(R=np.eye(3), ax_s=4)
p = np.array([-1.0, -1.0, -1.0])
q=[-0.05200234428048134,-0.0014000632800161839,0.044702015817165375,0.9976449608802795]
R = matrix_from_quaternion(q)
#nw=plot_basis(ax, R, p)

#ax.scatter(world_grid[:, 0], world_grid[:, 1], world_grid[:, 2])
#ax.scatter(world_grid[-1, 0], world_grid[-1, 1], world_grid[-1, 2], color="r")
ax.scatter(x, y, z, color="b")
#for p in world_grid[::10]:
#    ax.plot([p[0], cam2world[0, 3]],
#            [p[1], cam2world[1, 3]],
#            [p[2], cam2world[2, 3]], c="k", alpha=0.2, lw=2)

#ax = plt.subplot(122, aspect="equal")
#ax.set_title("Camera image")
#ax.set_xlim(0, image_size[0])\