#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 13:20:10 2020

@author: marcey
"""

import cv2
import numpy as np


#cap = cv2.VideoCapture('output.avi')
cap = cv2.VideoCapture(6)

def nothing(x):
    pass
# Creating a window for later use
cv2.namedWindow('result')

# Starting with 100's to prevent error while masking
h,s,v = 100,100,100
h1,s1,v1 = 100,100,100

# Creating track bar
cv2.createTrackbar('h', 'result',0,179,nothing)
cv2.createTrackbar('s', 'result',0,255,nothing)
cv2.createTrackbar('v', 'result',0,255,nothing)

cv2.createTrackbar('h1', 'result',0,179,nothing)
cv2.createTrackbar('s1', 'result',0,255,nothing)
cv2.createTrackbar('v1', 'result',0,255,nothing)
while(1):

    _, frame = cap.read()

    if frame is None: 
        print("empty frame")
        break
    frame=frame
    #converting to HSV
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

    # get info from track bar and appy to result
    h = cv2.getTrackbarPos('h','result')
    s = cv2.getTrackbarPos('s','result')
    v = cv2.getTrackbarPos('v','result')
    
    h1 = cv2.getTrackbarPos('h1','result')
    s1 = cv2.getTrackbarPos('s1','result')
    v1 = cv2.getTrackbarPos('v1','result')

    # Normal masking algorithm
    lower_blue = np.array([h,s,v])
    #upper_blue = np.array([180,255,255])
    upper_blue = np.array([h1,s1,v1])

    mask = cv2.inRange(hsv,lower_blue, upper_blue)

    result = cv2.bitwise_and(frame,frame,mask = mask)

    result=cv2.resize(result, (960, 540)) 
    cv2.imshow('result',result)

    k = cv2.waitKey(5) & 0xFF
    if k == ord("q"):
        break

cap.release()

cv2.destroyAllWindows()