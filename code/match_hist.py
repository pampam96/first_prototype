#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 09:53:54 2020

@author: marcey
"""
import cv2
from skimage import exposure
from skimage.exposure import match_histograms


cap = cv2.VideoCapture(6)

while(cap.isOpened()):
    ret,frame = cap.read()
    
    ref= cv2.imread('frame_h.jpg')

    if frame is None: 
        #print("empty frame")
        break
    
    matched=match_histograms(frame, ref, multichannel=True)
    cv2.imshow('matched', matched)
    cv2.imshow('Frame', frame)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord('q'):
        break
   
    if key == ord('s'):
        cv2.imwrite("frame_h.jpg", frame)
        
cap.release()
cv2.destroyAllWindows()