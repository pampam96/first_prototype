# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#!/usr/bin/env python
import numpy as np
import cv2
from scipy.spatial import distance as dist

#cap = cv2.VideoCapture('output.avi')
cap = cv2.VideoCapture(6)


threshold=200
threshold2=4000
kernel=np.ones((5,5),np.uint8)
frame_count=0

track_init=[]
old_trackerb=[]
old_trackerc=[]
detector=[]

t_init_b=[]
old_tbb=[]
old_tbc=[]
det_b=[]
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

trackers_b = cv2.MultiTracker_create()

def red_hsv():
    lower_red = np.array([0,143,0])
    upper_red = np.array([12,255,255])
    
    lower_red2 = np.array([118,73,0])
    upper_red2 = np.array([179,255,255])
    
    hsvr1 = cv2.inRange(hsv, lower_red, upper_red)
    hsvr2 = cv2.inRange(hsv, lower_red2, upper_red2)
    hsvr=hsvr1+hsvr2
    hsvr=cv2.morphologyEx(hsvr, cv2.MORPH_OPEN, kernel)
    return hsvr

def blue_hsv():
    # define range of blue color in HSV
    lower_blue = np.array([106,100,0])
    upper_blue = np.array([179,255,98])
    # Threshold the HSV image to get only blue colors
    hsvb = cv2.inRange(hsv, lower_blue, upper_blue)
    hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_OPEN, kernel)
    
    return hsvb
###function##
def detection_r(hsv):
      
    lower_red = np.array([0,143,0])
    upper_red = np.array([12,255,255])
    
    lower_red2 = np.array([118,73,0])
    upper_red2 = np.array([179,255,255])
    
    hsvr1 = cv2.inRange(hsv, lower_red, upper_red)
    hsvr2 = cv2.inRange(hsv, lower_red2, upper_red2)
    hsvr=hsvr1+hsvr2
    hsvr=cv2.morphologyEx(hsvr, cv2.MORPH_OPEN, kernel)
    ####Detection Code###########
    im2,contours,hierarchy= cv2.findContours(hsvr, 1, 2)
    
    #print(len(contours))
    for cnt in contours:
        M=cv2.moments(cnt)
        #and M['m00']<threshold2
        if M['m00']>threshold:
           # print('blob detected')
            x,y,w,h = cv2.boundingRect(cnt)
            #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            track_init.append([(x,y),(w,h),M['m00']])
   # print(track_init)
    #return(hsvr)
        
def detection_b(hsv):
      
    # define range of blue color in HSV
    lower_blue = np.array([106,100,0])
    upper_blue = np.array([179,255,98])
    # Threshold the HSV image to get only blue colors
    hsvb = cv2.inRange(hsv, lower_blue, upper_blue)
    hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_OPEN, kernel)
      
    ####Detection Code###########
    im2,contours,hierarchy= cv2.findContours(hsvb, 1, 2)
    
    #print(len(contours))
    for cnt in contours:
        M=cv2.moments(cnt)
        if M['m00']>threshold:
            #print('blob detected')
            x,y,w,h = cv2.boundingRect(cnt)
            #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            t_init_b.append([(x,y),(w,h),M['m00']])

    return(hsvb) 

def matcher(one,two):
    objectCentroids=one
    inputCentroids=two
    
    D = dist.cdist(objectCentroids, inputCentroids)
    rows = D.min(axis=1).argsort()
    cols = D.argmin(axis=1)[rows]
    
    usedRows = set()
    usedCols = set()
    # loop over the combination of the (row, column) index
    # tuples
    for (row, col) in zip(rows, cols):
	
        if row in usedRows or col in usedCols:
            continue
        old_trackerc[row] = track_init[col]
        usedRows.add(row)
        usedCols.add(col) 
        
def matcherb(one,two):
    objectCentroids=one
    inputCentroids=two
    
    D = dist.cdist(objectCentroids, inputCentroids)
    rows = D.min(axis=1).argsort()
    cols = D.argmin(axis=1)[rows]
    
    usedRows = set()
    usedCols = set()
    # loop over the combination of the (row, column) index
    # tuples
    for (row, col) in zip(rows, cols):
	
        if row in usedRows or col in usedCols:
            continue
        old_tbc[row] = t_init_b[col]
        usedRows.add(row)
        usedCols.add(col)

while(cap.isOpened()):
    
    ret, frame = cap.read()
    
    if frame is None: 
        print("empty frame")
        break
    
    frame=cv2.resize(frame, (960, 540))
    
    frame=frame+5
    frame_count=frame_count+1
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    
	# loop over the bounding boxes and draw then on the frame
    (success, boxes) = trackers.update(frame)
    (successb, boxesb) = trackers_b.update(frame)
    
    for box in boxes:
        (x, y, w, h) = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        
    for box in boxesb:
        (x, y, w, h) = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
    
    
    
    hsvr=red_hsv()    
    hsvb=blue_hsv()
    #hsvb=detection_b(hsv)

    # show frames
    cv2.imshow('frame',frame)
    cv2.imshow('hsvb',hsvb)
    cv2.imshow('hsvr',hsvr)
    
    key = cv2.waitKey(1) & 0xFF
    
    if key == ord("s"):
		# select the bounding box of the object we want to track (make
		# sure you press ENTER or SPACE after selecting the ROI)
        box = cv2.selectROI("Frame", frame, fromCenter=False,
			showCrosshair=True)
        
		# create a new object tracker for the bounding box and add it
		# to our multi-object tracker
        tracker = OPENCV_OBJECT_TRACKERS[trackername]()
        trackers.add(cv2.TrackerKCF_create(), frame, box)
        #print('box',box)
    
    elif key == ord("q"):
        break

    if frame_count==30:
        cv2.imwrite("frame3.jpg", frame) 
        detection_r(hsv)
        detection_b(hsv)
        print('track_init',track_init)
        for bl in track_init:
            tracker = OPENCV_OBJECT_TRACKERS[trackername]()
            trackers.add(tracker, frame, (bl[0][0],bl[0][1],bl[1][0],bl[1][1]))
        for bl in t_init_b:
            tracker = OPENCV_OBJECT_TRACKERS[trackername]()
            trackers_b.add(tracker, frame, (bl[0][0],bl[0][1],bl[1][0],bl[1][1]))

    elif frame_count==70:
        print('frame 70 again')
        
        ##marker variables
        track_init.clear()
        old_trackerb.clear()
        old_trackerc.clear()
        detector.clear()
        detection_r(hsv)
        
        
        ##reference variables
        t_init_b.clear()
        old_tbb.clear()
        old_tbc.clear()
        det_b.clear()
        detection_b(hsv)
        
        #marker detection and appending
        for obj in track_init:
            detector.append(obj[0])
            
        for box in boxes:
             (x, y, w, h) = [int(v) for v in box]
             old_trackerc.append((x,y))
             old_trackerb.append((w,h))
        
        #reference detection and appending     
        for obj in t_init_b:
            det_b.append(obj[0])
            
        for box in boxesb:
             (x, y, w, h) = [int(v) for v in box]
             old_tbc.append((x,y))
             old_tbb.append((w,h))
       # print('old_tracker c',old_trackerc,'old_tracker w',old_trackerb)
        
       #matcher for marker
        matcher(old_trackerc,detector)
        #matcher for reference 
        matcherb(old_tbc,det_b)
       # print('track_init',track_init)
        #print('old_tracker after',old_trackerc)
        
        trackers.clear()
        trackers = cv2.MultiTracker_create()

        print(len(track_init))
        for i, bl in enumerate(old_trackerc):
            tracker = OPENCV_OBJECT_TRACKERS[trackername]()
            #print('bl',bl)
            if len(bl)==3:
               trackers.add(tracker, frame, (bl[0][0],bl[0][1],bl[1][0],bl[1][1]))
            else:
               trackers.add(tracker, frame, (bl[0],bl[1],old_trackerb[i][0],old_trackerb[i][1]))
               
        trackers_b.clear()
        trackers_b = cv2.MultiTracker_create()

        print(len(t_init_b))
        for i, bl in enumerate(old_tbc):
            tracker = OPENCV_OBJECT_TRACKERS[trackername]()
            #print('bl',bl)
            if len(bl)==3:
               trackers_b.add(tracker, frame, (bl[0][0],bl[0][1],bl[1][0],bl[1][1]))
            else:
               trackers_b.add(tracker, frame, (bl[0],bl[1],old_tbb[i][0],old_tbb[i][1]))
                


        

        frame_count=31
cap.release()
cv2.destroyAllWindows()
