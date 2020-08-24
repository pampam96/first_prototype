#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 10:03:03 2020

@author: marcey
"""
import numpy as np
import cv2
import matplotlib.pyplot as plt
from skimage import exposure
from skimage.exposure import match_histograms

img = cv2.imread('frame1.jpg') # reads image 'opencv-logo.png' as grayscale
img_adapteq = exposure.equalize_adapthist(img, clip_limit=0.03)

###equalizing histogram with hsv
#img_hsv= cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#img_hsv[:,:,2]=cv2.equalizeHist(img_hsv[:,:,2])
#img= cv2.cvtColor(img_hsv, cv2.COLOR_HSV2BGR)


ref= cv2.imread('frame2.jpg')
#ref_q=cv2.equalizeHist(ref)

matched=match_histograms(img, ref, multichannel=True)
cv2.imshow('image',img)
cv2.imshow('img_adapteq',img_adapteq)
cv2.imshow('image2',ref)
cv2.imshow('matched',matched)
