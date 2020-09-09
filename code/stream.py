#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 13:13:57 2020

@author: marcey
"""
#!/usr/bin/env python
import numpy as np
import cv2

#cap = cv2.VideoCapture('chaplin.avi')
cap = cv2.VideoCapture(6)
frame_count=0

kernel=np.ones((5,5),np.uint8)

# initialize a dictionary that maps strings to their corresponding
# OpenCV object tracker implementations
trackername="kcf"
OPENCV_OBJECT_TRACKERS = {
	"csrt": cv2.TrackerCSRT_create,
	"kcf": cv2.TrackerKCF_create,
	"boosting": cv2.TrackerBoosting_create,
	"mil": cv2.TrackerMIL_create,
	"tld": cv2.TrackerTLD_create,
	"medianflow": cv2.TrackerMedianFlow_create,
	"mosse": cv2.TrackerMOSSE_create
}
# initialize OpenCV's special multi-object tracker
trackers = cv2.MultiTracker_create()

def red_hsv():
    lower_red = np.array([0,143,0])
    upper_red = np.array([12,255,255])
    
    lower_red2 = np.array([118,138,0])
    upper_red2 = np.array([179,255,255])
    
    hsvr1 = cv2.inRange(hsv, lower_red, upper_red)
    hsvr2 = cv2.inRange(hsv, lower_red2, upper_red2)
    hsvr=hsvr1+hsvr2
    hsvr=cv2.morphologyEx(hsvr, cv2.MORPH_OPEN, kernel)
    return hsvr

def blue_hsv():
    # define range of blue color in HSV
    lower_blue = np.array([100,227,0])
    upper_blue = np.array([179,255,255])
    # Threshold the HSV image to get only blue colors
    hsvb = cv2.inRange(hsv, lower_blue, upper_blue)
    hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_OPEN, kernel)

while(cap.isOpened()):
    
    ret, frame = cap.read()
    frame_count=frame_count+1
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    (success, boxes) = trackers.update(frame)
	# loop over the bounding boxes and draw then on the frame
    for box in boxes:
        (x, y, w, h) = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    if frame is None: 
        print("empty frame")
        break

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    hsvr=red_hsv()    
    hsvb=blue_hsv()

    cv2.imshow('frame',frame)
    cv2.imshow('hsvb',hsv)

    #cv2.imshow('hsvb',hsvb)
    #cv2.imshow('hsvr',hsvr)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("s"):
		# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
        box = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)
		# create a new object tracker for the bounding box and add it
		# to our multi-object tracker
        tracker = OPENCV_OBJECT_TRACKERS[trackername]()
        #trackers.add(cv2.TrackerKCF_create(), frame, box)
        trackers.add(tracker, frame, box)
    
    elif key == ord("q"):
        break
    
   # if frame_count==50:
  #      cv2.imwrite("frame%d.jpg" % frame_count, frame) 
cap.release()
cv2.destroyAllWindows()
