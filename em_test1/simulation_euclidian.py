#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 22:27:32 2020

@author: marcey
"""

from scipy.spatial import distance
import csv

#length of side motors at 0
a1 = (-0.0769076, -0.0293347, 0.2245)
a2= (0.0716758, -0.0404695, 0.2245)

a12 = (-0.0716764, -0.0404695, 0.2245)
a22= (0.0769069, -0.0293347, 0.2245)


dst = distance.euclidean(a1, a2)
print(dst)

dst22 = distance.euclidean(a12, a22)
print(dst22)

# 0.14400004122950796
# 0.14900335566691106

p1 = (0.05003, -0.0738373, 0.2295)
p2= (-0.0602721, -0.0657678, 0.2295)


dstp12 = distance.euclidean(p1, p2)
print(dstp12)


#####CHOSEN
M2_0=(0.0716758, -0.0404695, 0.2245)
M2_F=(0.0769076, 0.0293347, 0.2245)
M1_F=(-0.0716764, 0.0404695, 0.2245)
P3=(0.0602721, 0.0657678, 0.2295)
P2=(-0.0602721, -0.0657678, 0.2295)
P4=(-0.0500323, 0.0738573, 0.2295)



#dstpM_0F = distance.euclidean(M2_0, M2_F)
#print(dstpM_0F)
M1_0=(-0.0716764, -0.0293347, 0.2245)

print("LALALALALA")
print("points for transform")
print(M2_0,M2_F,M1_F,P3)
print("single point")
print(P2,P4)
