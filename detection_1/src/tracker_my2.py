#!/usr/bin/env python
# license removed for brevity
import rospy
import math
from std_msgs.msg import String,Int32,Int32MultiArray
from std_msgs.msg import UInt16
import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
from scipy.spatial import distance as dist
print("Environment Ready")

def talker():

    ####### ROS variables ######
    #pub = rospy.Publisher('servo', UInt16, queue_size=10)
    pub = rospy.Publisher('distance', Int32MultiArray, queue_size=10)

    mess=Int32MultiArray()

    rospy.init_node('dSender', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    #mess=UInt16()

    ###### RealSense variables ##########
    pipeline = rs.pipeline()

    config = rs.config()
    #try if you can do this ???
    #config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    #config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    profile = pipeline.start(config)

    align_to = rs.stream.color
    align = rs.align(align_to)
    ############# Open cv Tracker variables ########

    ######## my tracker #########
    my_trackerb=[]
    my_trackerr=[]
    tracker_g=[]
    tracker_y=[]
    t_y=[]
    init_calibration=False
    second_calibration=False
    done_calib=True
    distance_rl=[]
    rotpoint=[]
    i_g=True

    ##### other variables #######
    threshold=100
    threshold3=1000
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

    distances=[0]

    ##sucess variables
    success=True
    successb=True

    ##### old value of x and y
    old_value=(0,0)

    ######### Open cv functions #########

    #red hsv mask turns into binary
    def red_hsv():
        lower_red = np.array([0,143,83])
        upper_red = np.array([12,255,255])

        lower_red2 = np.array([118,73,83])
        upper_red2 = np.array([179,255,255])
        #upper_red2 = np.array([179,255,200])

        hsvr1 = cv2.inRange(hsv, lower_red, upper_red)
        hsvr2 = cv2.inRange(hsv, lower_red2, upper_red2)
        hsvr=hsvr1 +hsvr2
        #hsvr=cv2.morphologyEx(hsvr, cv2.MORPH_CLOSE, kernel)
        hsvr=cv2.morphologyEx(hsvr, cv2.MORPH_OPEN, kernel)
        #hsvr=cv2.GaussianBlur(hsvr,(3,3),0)
        return hsvr

    #blue hsv calculation
    def blue_hsv():
        # define range of blue color in HSV
        lower_blue = np.array([106,170,0])
        upper_blue = np.array([179,255,98])

        lower_blue2 = np.array([106,100,0])
        lower_blue21 = np.array([35,150,0])
        upper_blue2 = np.array([164,255,255])
        # Threshold the HSV image to get only blue colors
        hsvb = cv2.inRange(hsv2, lower_blue2, upper_blue2)
        #hsvb = cv2.inRange(hsv2, lower_blue2, upper_blue2)
        #hsvb2 = cv2.inRange(hsv2, lower_blue21, upper_blue2)
        #hsvb=hsvb2+hsvb

        hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_CLOSE, kernel)
        hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_OPEN, kernel)
        return hsvb

    #green calculation for the initial calibration
    def green_hsv():

        lower_blue = np.array([52,90,52])
        upper_blue = np.array([94,255,255])

        hsvb = cv2.inRange(hsv2, lower_blue, upper_blue)

        hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_CLOSE, kernel)
        hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_OPEN, kernel)
        return hsvb

    def yellow_hsv():

        lower_blue = np.array([20,67,36])
        upper_blue = np.array([39,255,255])

        hsvb = cv2.inRange(hsv2, lower_blue, upper_blue)

        hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_CLOSE, kernel)
        hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_OPEN, kernel)
        return hsvb

    #detection of the red markers
    def detection_r(hsv):

        #hsv masking
        lower_red = np.array([0,143,83])
        upper_red = np.array([12,255,255])

        lower_red2 = np.array([118,73,83])
        #upper_red2 = np.array([179,255,255])
        upper_red2 = np.array([179,255,158])

        hsvr1 = cv2.inRange(hsv, lower_red, upper_red)
        hsvr2 = cv2.inRange(hsv, lower_red2, upper_red2)
        hsvr=hsvr1+hsvr2

        #morphological operations of opening and closing
        hsvr=cv2.morphologyEx(hsvr, cv2.MORPH_OPEN, kernel)


        ####Detection Code###########
        im2,contours,hierarchy= cv2.findContours(hsvr, 1, 2)

        #go through all the contours
        for cnt in contours:
            M=cv2.moments(cnt)
            epsilon=0.01*cv2.arcLength(cnt,True)
            #print('epsilon',epsilon)
            #Circular objects will have higher number of points.
            approx = cv2.approxPolyDP(cnt,epsilon,True)
            #print('aprox',approx)
            #and M['m00']<threshold2

            #detect only things that are circles and a certain area
            if M['m00']>threshold and len(approx) > 8:
                # print('blob detected')
                x,y,w,h = cv2.boundingRect(cnt)
                #print('bounding rec', x,y,w,h)
                xy,wh,r=cv2.minAreaRect(cnt)
                #print('rectangle', rect)#this has (x,y),(w,h),(rot)
                #box=cv2.boxPoints(rect)# four x,y
                #print('box',box)
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                #cv2.rectangle(frame, (int(xy[0]),int(xy[1])), (int(xy[0] + wh[0]), int(xy[1] + wh[1])), (0, 255, 255), 1)

                ##find its depth in z frame
                zDepth=aligned_depth_frame.get_distance(int(x+w/2),int(y+h/2))

                #print('zDepth',zDepth)
                centroid=(x+w/2,y+h/2)
                #create my tracker list
                track_init.append([(x,y),(w,h),M['m00'],zDepth,centroid])

        #get rid of things that are below a certain depth
        for i,t in enumerate(track_init):
            if t[3]>0.40:
                del track_init[i]


    #simply detection exactly the same as the previous one
    def detection_r2(hsv):

        lower_red = np.array([0,143,83])
        upper_red = np.array([12,255,255])

        lower_red2 = np.array([118,73,83])
        upper_red2 = np.array([179,255,255])

        hsvr1 = cv2.inRange(hsv, lower_red, upper_red)
        hsvr2 = cv2.inRange(hsv, lower_red2, upper_red2)
        hsvr=hsvr1+hsvr2
        hsvr=cv2.morphologyEx(hsvr, cv2.MORPH_OPEN, kernel)
        #hsvr=cv2.GaussianBlur(hsvr,(5,5),0)

            ####Detection Code###########
        im2,contours,hierarchy= cv2.findContours(hsvr, 1, 2)

            #print(len(contours))
        for cnt in contours:
            M=cv2.moments(cnt)
            epsilon=0.01*cv2.arcLength(cnt,True)
                #print('epsilon',epsilon)
                #Circular objects will have higher number of points.
            approx = cv2.approxPolyDP(cnt,epsilon,True)
                #print('aprox',approx)
                #and M['m00']<threshold2
            if M['m00']>threshold and len(approx) > 8:
                    # print('blob detected')
                x,y,w,h = cv2.boundingRect(cnt)
                    #print('bounding rec', x,y,w,h)
                xy,wh,r=cv2.minAreaRect(cnt)
                    #print('rectangle', rect)#this has (x,y),(w,h),(rot)
                    #box=cv2.boxPoints(rect)# four x,y
                    #print('box',box)
                    #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                    #cv2.rectangle(frame, (int(xy[0]),int(xy[1])), (int(xy[0] + wh[0]), int(xy[1] + wh[1])), (0, 255, 255), 1)

                zDepth=aligned_depth_frame.get_distance(int(x+w/2),int(y+h/2))
                    #print('zDepth',zDepth)
                if zDepth<0.4:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                    cv2.rectangle(frame, (int(xy[0]),int(xy[1])), (int(xy[0] + wh[0]), int(xy[1] + wh[1])), (0, 255, 255), 1)

    #detection of green
    def detection_g(hsv2):

        # define range of blue color in HSV
        lower_blue = np.array([52,90,52])
        upper_blue = np.array([94,255,255])

        # Threshold the HSV image to get only blue colors
        hsvb = cv2.inRange(hsv2, lower_blue, upper_blue)
        #hsvb2 = cv2.inRange(hsv2, lower_blue21, upper_blue2)
        #hsvb=hsvb2+hsvb
        #hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_CLOSE, kernel)
        hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_OPEN, kernel)
        hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_CLOSE, kernel)
        #hsvb=cv2.GaussianBlur(hsvb,(5,5),0)

        ####Detection Code###########
        im2,contours,hierarchy= cv2.findContours(hsvb, 1, 2)

        #print(len(contours))
        for cnt in contours:
            M=cv2.moments(cnt)
            if M['m00']>threshold3:
                #print('blob detected')
                x,y,w,h = cv2.boundingRect(cnt)
                centroid=(x+w/2,y+h/2)
                zDepth=aligned_depth_frame.get_distance(int(x+w/2),int(y+h/2))
                #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                #cv2.rectangle(frame, centroid, (centroid[0]+1, centroid[1]+1), (0, 255, 0), 1)
                del tracker_g[:]
                tracker_g.append([(x,y),(w,h),centroid,zDepth])

                #if i_g==True or not tracker_g:
                #    tracker_g.append([(x,y),(w,h),centroid,zDepth])
                #else:
                #    distance_g= dist.euclidean((x,y), tracker_g[0][0])
                #    if distance_g<3:
                #        print("no green update")
                #        print("tracker_g",tracker_g[0])
                #        tracker_g.append([(x,y),(w,h),centroid,zDepth])
                #    elif distance_g>3:
                #        del tracker_g[:]
                #        tracker_g.append([(x,y),(w,h),centroid,zDepth])
                #        print("green update",distance_g)
    def detection_y(hsv2):

        # define range of blue color in HSV
        lower_blue = np.array([20,67,36])
        upper_blue = np.array([39,255,255])

        # Threshold the HSV image to get only blue colors
        hsvb = cv2.inRange(hsv2, lower_blue, upper_blue)
        #hsvb2 = cv2.inRange(hsv2, lower_blue21, upper_blue2)
        #hsvb=hsvb2+hsvb
        #hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_CLOSE, kernel)
        hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_OPEN, kernel)
        hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_CLOSE, kernel)
        #hsvb=cv2.GaussianBlur(hsvb,(5,5),0)

        ####Detection Code###########
        im2,contours,hierarchy= cv2.findContours(hsvb, 1, 2)

        #print(len(contours))
        for cnt in contours:
            M=cv2.moments(cnt)
            epsilon=0.01*cv2.arcLength(cnt,True)
                #print('epsilon',epsilon)
                #Circular objects will have higher number of points.
            approx = cv2.approxPolyDP(cnt,epsilon,True)
            perimeter = cv2.arcLength(cnt,True)
            print('perimeter',perimeter,'area',M['m00'])
                #and M['m00']<threshold2
                #and M['m00']<2000
            if M['m00']>1900 and M['m00']<2600 and len(approx) > 8:
                #print('blob detected')
                x,y,w,h = cv2.boundingRect(cnt)
                centroid=(x+w/2,y+h/2)
                zDepth=aligned_depth_frame.get_distance(int(x+w/2),int(y+h/2))
                print("yellow depth",zDepth)
                del t_y[:]
                if zDepth<0.43 and zDepth>0:
                    t_y.append([(x,y),(w,h),centroid,zDepth])
    #detection of blue references
    def detection_b(hsv2):

        # define range of blue color in HSV
        lower_blue = np.array([104,170,0])
        upper_blue = np.array([179,255,255])

        lower_blue2 = np.array([106,100,0])
        lower_blue21 = np.array([35,150,0])
        upper_blue2 = np.array([164,255,255])
        #upper_blue2 = np.array([134,255,255])

        # Threshold the HSV image to get only blue colors
        hsvb = cv2.inRange(hsv2, lower_blue2, upper_blue2)
        #hsvb2 = cv2.inRange(hsv2, lower_blue21, upper_blue2)
        #hsvb=hsvb2+hsvb
        hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_CLOSE, kernel)
        hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_OPEN, kernel)

        ####Detection Code###########
        im2,contours,hierarchy= cv2.findContours(hsvb, 1, 2)

        #print(len(contours))
        for cnt in contours:
            M=cv2.moments(cnt)
            epsilon=0.01*cv2.arcLength(cnt,True)
            #print('epsilon',epsilon)
            #Circular objects will have higher number of points.
            approx = cv2.approxPolyDP(cnt,epsilon,True)
            #print('aprox',approx)
            #and M['m00']<threshold2
            if M['m00']>threshold and len(approx) > 8:
                #print('blob detected')
                x,y,w,h = cv2.boundingRect(cnt)
                zDepth=aligned_depth_frame.get_distance(int(x+w/2),int(y+h/2))
                #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                #print('zDepth blue',zDepth)
                centroid=(x+w/2,y+h/2)
                if zDepth<0.34:
                    t_init_b.append([(x,y),(w,h),M['m00'],zDepth,centroid])


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
            #old_trackerc[row] = detector[col]
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

            #old_tbc[row] = det_b[col]
            old_tbc[row] = t_init_b[col]

            usedRows.add(row)
            usedCols.add(col)

    def sortThird(val):
        return val[3]
    def sortSecond(val):
        return val[2]

    def distance(marker,reference):
        if(len(marker)<3):
            print('not enough markers detected')
        elif(len(reference)<2):
            print('not enough references detected')
        else:
            #print('distance can be measured')
            ##print('marker',marker[0][3])
            #print('rotpoint',rotpoint)
            #print('marker',marker[0])
            #xy,wh,depth,centroid,i for marker and reference


            #real world distances
            rl_pointm1 = rs.rs2_deproject_pixel_to_point(depth_intrin, [int(marker[0][3][0]),int(marker[0][3][1])], marker[0][2])
            rl_pointm2 = rs.rs2_deproject_pixel_to_point(depth_intrin, [int(marker[1][3][0]),int(marker[1][3][1])], marker[1][2])
            rl_pointm3 = rs.rs2_deproject_pixel_to_point(depth_intrin, [int(marker[2][3][0]),int(marker[2][3][1])], marker[2][2])

            rl_pointr1 = rs.rs2_deproject_pixel_to_point(depth_intrin, [int(reference[0][3][0]),int(reference[0][3][1])], reference[0][2])
            rl_pointr2 = rs.rs2_deproject_pixel_to_point(depth_intrin, [int(reference[1][3][0]),int(reference[1][3][1])], reference[1][2])
            #rotation point
            rl_pointr3 = rs.rs2_deproject_pixel_to_point(depth_intrin, [int(rotpoint[0][0][0]),int(rotpoint[0][0][1])],rotpoint[0][1])

            #print('real markers',rl_pointm1,rl_pointm2,rl_pointm3)
            #print('real references',rl_pointr1,rl_pointr2,rl_pointr3)
            #euclidian in 3D ???
            #[0.10853161662817001, -0.004322144202888012, 0.3850000202655792]
            distance1= dist.euclidean(rl_pointm1, rl_pointr3)
            distance2= dist.euclidean(rl_pointm2, rl_pointr1)
            distance3= dist.euclidean(rl_pointm3, rl_pointr2)

            del distance_rl[:]
            #distance of rotational motor
            distance_rl.append(distance1*1000)

            #distance of side translation
            distance_rl.append(distance2*1000)

            #distance of middle translation
            distance_rl.append(distance3*1000)

            #print(distance_rl)
            #pixel coordinates
            #marker1 = dist.euclidean(marker[0][0], (276,230))
            #marker2 = dist.euclidean(marker[1][0], reference[0][0])
            #marker3 = dist.euclidean(marker[2][0], reference[1][0])

            #distances.append(marker1)
            #distances.append(marker2)
            #distances.append(marker3)
            #print('d1',marker1,'d2',marker2,'d3',marker3)

    ######## image prepro
    def autoAdjustments_with_convertScaleAbs(img):
        alow = img.min()
        ahigh = img.max()
        amax = 255
        amin = 0

        # calculate alpha, beta
        alpha = ((amax - amin) / (ahigh - alow))
        beta = amin - alow * alpha
        # perform the operation
        new_img = cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

        return [new_img, alpha, beta]

    def get_angle(p1, p2):
        return math.atan2(p1[1]*1000 - p2[1]*1000, p1[0]*1000 - p2[0]*1000) * 180/math.pi

    def get_angle3(a, b, c):
        ang= math.degrees(math.atan2(c[1]-b[1],c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0]))
        return ang + 360 if ang < 0 else ang

    def get_angle3d(a, b, c):
         # Create vectors from points
         ba = [ aa-bb for aa,bb in zip(a,b) ]
         bc = [ cc-bb for cc,bb in zip(c,b) ]
         print("ba",ba,"bc",bc,a,b,c)

         # Normalize vector
         nba = math.sqrt( sum ( (x**2.0 for x in ba) ) )
         ba = [ x/nba for x in ba ]

         nbc = math.sqrt( sum ( (x**2.0 for x in bc) ) )
         bc = [ x/nbc for x in bc ]

         #print("ba",ba,"bc",bc)

         # Calculate scalar from normalized vectors
         scale = sum ( (aa*bb for aa,bb in zip(ba,bc)) )
         print("scale",scale)

         # calculate the angle in radian
         angle = math.acos(scale)
         return angle

    while not rospy.is_shutdown():
        #rate.sleep()
        try:
            ######### this is practically main #############
            while True:
                # Get frameset of color and depth
                frames = pipeline.wait_for_frames()
                ref= cv2.imread('/home/marcey/vision/frame3.jpg')

                # frames.get_depth_frame() is a 640x360 depth image

                # Align the depth frame to color frame
                aligned_frames = align.process(frames)

                # Get aligned frames
                aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
                color_frame = aligned_frames.get_color_frame()

                # Validate that both frames are valid
                if not aligned_depth_frame or not color_frame:
                    continue

                depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
                color_intrin = color_frame.profile.as_video_stream_profile().intrinsics

                depth_image = np.asanyarray(aligned_depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())

                frame=color_image#+7
                frame2=color_image#+7
                frame_count=frame_count+1

                #frame_changed,a,b=autoAdjustments_with_convertScaleAbs(frame)

                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

                ### create hsv images so you can show them not needed in the future
                hsvr=red_hsv()
                hsvb=blue_hsv()
                hsvg=green_hsv()
                hsvy=yellow_hsv()

                #print('init_calibration',init_calibration)

                ######## when we reach a certain frame with stable exposure we init trackers ########
                if frame_count==60:

                    #### detection is done for markers and reference#####
                    detection_r(hsv)
                    detection_b(hsv2)

                    #### markers are sorted on distance and area ####
                    track_init.sort(key=sortThird,reverse=True)
                    new=track_init[1:]
                    new.sort(key=sortSecond,reverse=True)
                    track_init[1:]=new

                    ### references are sorted on area ####
                    t_init_b.sort(key=sortSecond,reverse=True)


                    #### iterate through detected and init a tracker for marker
                    for i,bl in enumerate(track_init):
                        centroid=bl[4]
                        ### apend to my list of trackers
                        #xy,wh,depth,centroid,i
                        my_trackerr.append([bl[0],bl[1],bl[3],centroid,i])
                    #### iterate through detected and init a tracker for reference
                    for i,bl in enumerate(t_init_b):
                        centroid=bl[4]
                        ### append to my list of trackers
                        my_trackerb.append([bl[0],bl[1],bl[3],centroid,i])

                #elif frame_count==100:
                elif frame_count >=61:
                    #or frame_count==62

                    print('youve done it again')
                    ##marker variables to reinit tracker
                    del track_init[:], old_trackerb[:], old_trackerc[:],detector[:]
                    ## marker detection
                    detection_r(hsv)

                    ##reference variables to re init tracker
                    del t_init_b[:], old_tbb[:],old_tbc[:],det_b[:]
                    ## reference detection
                    detection_b(hsv2)

                    #marker appending on needed lists
                    ### iterating through detector
                    for obj in track_init:
                        detector.append(obj[0])
                    ### iterating through the old tracker
                    for box in my_trackerr:
                        old_trackerc.append(box[0])

                    #reference appending on needed lists
                    ### iterating through detector
                    for obj in t_init_b:
                        det_b.append(obj[0])
                    ### iterating through the old tracker
                    for box in my_trackerb:
                        old_tbc.append(box[0])

                    #matcher for marker
                    matcher(old_trackerc,detector)

                    #### make this less ugly plsss codee siso guglyyyyy
                    ################
                    for i,tr in enumerate(my_trackerr):

                        #print(old_trackerc[i])
                        if len(old_trackerc[i])>3:
                            #updating xy
                            distance_old=dist.euclidean(tr[0],old_trackerc[i][0])
                            #print("old distance",distance_old)
                            if distance_old>2:
                                tr[0]=old_trackerc[i][0]
                                #updating centroid
                                centroid=(tr[0][0]+ old_trackerc[i][1][0]/2 ,tr[0][1]+old_trackerc[i][1][1]/2)
                                #tr[3]=old_trackerc[i][4]
                                tr[3]=centroid
                                #print("calculated centroid",centroid, "detected centroid",tr[3])
                                #depth update
                                tr[2]=old_trackerc[i][3]
                            elif distance_old<2:
                                print("no update")
                        else:
                            tr[0]=old_trackerc[i]


                    #matcher for reference
                    matcherb(old_tbc,det_b)

                    for i,tb in enumerate(my_trackerb):
                        #updating centroid
                        #print(old_tbc[i])
                        if len(old_tbc[i])>3:
                            distance_old=dist.euclidean(tb[0],old_tbc[i][0])
                            #print("old distance",distance_old)
                            if distance_old>2:
                                #updating xy
                                tb[0]=old_tbc[i][0]
                                #updating centroid
                                tb[3]=old_tbc[i][4]
                                #updating depth
                                tb[2]=old_tbc[i][3]
                            elif distance_old<2:
                                print("no update")
                        else:
                            tb[0]=old_tbc[i]


                ##show on screen

                #print('my_trackerr',my_trackerr)
                for tr in my_trackerr:
                    cv2.rectangle(frame, tr[0], (tr[0][0] + tr[1][0], tr[0][1] + tr[1][1]), (0, 0, 255), 1)
                    cv2.rectangle(frame, tr[3], (tr[3][0]+1, tr[3][1]+1), (0, 255, 0), 1)
                    cv2.putText(frame,str(tr[4]),tr[0],cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),3)

                #print('my_trackerb',my_trackerb)
                for tb in my_trackerb:
                    cv2.rectangle(frame, tb[0], (tb[0][0] + tb[1][0], tb[0][1] + tb[1][1]), (0, 0, 255), 1)
                    cv2.rectangle(frame, tb[3], (tb[3][0]+1, tb[3][1]+1), (0, 255, 0), 1)
                    cv2.putText(frame,str(tb[4]),tb[0],cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),3)

                #print('init_calibration',init_calibration)

                if init_calibration==False and len(my_trackerr)>1:
                    #del tracker_g[:]
                    print('Doing calibration of green')
                    detection_g(hsv)
                    i_g=False

                    if len(tracker_g)>0:
                        #print detected
                        ##print the tracker to see how it is working
                        cv2.rectangle(frame,(tracker_g[0][0]),(tracker_g[0][0][0]+tracker_g[0][1][0],tracker_g[0][0][1]+tracker_g[0][1][0]),(255,0,0),2)
                        cv2.rectangle(frame, tracker_g[0][2], (tracker_g[0][2][0]+1, tracker_g[0][2][1]+1), (0, 255, 0), 1)

                        ##do the rest
                        # real life green point
                        rl_pointg1 = rs.rs2_deproject_pixel_to_point(depth_intrin, [int(tracker_g[0][2][0]),int(tracker_g[0][2][1])], tracker_g[0][3])
                        # real life red point
                        rl_pointr2 = rs.rs2_deproject_pixel_to_point(depth_intrin, [int(my_trackerr[0][3][0]),int(my_trackerr[0][3][1])], my_trackerr[0][2])
                        # real life blue point
                        rl_pointb2 = rs.rs2_deproject_pixel_to_point(depth_intrin, [int(my_trackerb[0][3][0]),int(my_trackerb[0][3][1])], my_trackerb[0][2])

                        xz_distance=(dist.euclidean((rl_pointg1[0],rl_pointg1[2]),(rl_pointr2[0],rl_pointr2[2])))*1000
                        xy_rdistance=(dist.euclidean((rl_pointg1[0],rl_pointg1[1]),(rl_pointr2[0],rl_pointr2[1])))*1000
                        xy_rbdistance=(dist.euclidean((rl_pointb2[0],rl_pointb2[1]),(rl_pointr2[0],rl_pointr2[1])))*1000

                        xy_distance=(dist.euclidean(tracker_g[0][2],my_trackerr[0][3]))

                        yz_distance=(dist.euclidean((rl_pointg1[1],rl_pointg1[2]),(rl_pointr2[1],rl_pointr2[2])))*1000

                        angle= get_angle((rl_pointg1[0],rl_pointg1[1]),(rl_pointr2[0],rl_pointr2[1]))
                        angle3= get_angle3((rl_pointg1[0],rl_pointg1[1]),(rl_pointr2[0],rl_pointr2[1]),(rl_pointb2[0],rl_pointb2[1]))
                        angle3d= get_angle3d(rl_pointg1,rl_pointr2,rl_pointb2)

                        #xyz
                        distance_g=(dist.euclidean(rl_pointg1,rl_pointr2))*1000
                        distance_gb=(dist.euclidean(rl_pointb2,rl_pointr2))*1000
                        print('distanceG',distance_g,"xy",xy_distance,"yz",yz_distance,"angle",angle, "angle3",angle3,"angle3d",angle3d)

                        #and distance_g<60
                        #if distance_g<=155 and:
                        #old code
                        #if angle<=156.5 and angle>151 and xy_distance<116:
                        if angle3d<=2.5 and angle3d>2.44 and xy_distance<116:
                            mess.data=[0,1,0]
                            for i in range(30):
                                pub.publish(mess)
                                del rotpoint[:]
                                print('why is this happening again??')
                                dummy=[my_trackerr[0][3],my_trackerr[0][2]]
                                rotpoint.append(dummy)
                                print('why is this happening again??')
                            ##publish this for a little bitty
                            ##aka publish that is case one and stop
                            init_calibration=True
                        else:
                            mess.data=[0,2,0]
                            pub.publish(mess)

                    elif len(tracker_g)==0:
                        mess.data=[0,2,0]
                        pub.publish(mess)
                    #print(tracker_g)
                    #print(init_calibration)

                elif init_calibration==True and done_calib==True and second_calibration==False:

                    distance(my_trackerr,my_trackerb)
                    print('needed',distance_rl)
                    ##so that actually gets passed on

                    ##distance 1 is for side translation
                    ##distance 2 is for middle translation

                    if distance_rl[1]<37 and distance_rl[2]<58:
                        mess.data=[3,1,1]
                        pub.publish(mess)
                        second_calibration=True;
                    elif distance_rl[1]<37 and distance_rl[2]>58:
                        mess.data=[3,1,2]
                        pub.publish(mess)
                    elif distance_rl[1]>37 and distance_rl[2]<58:
                        mess.data=[3,2,1]
                        pub.publish(mess)
                    elif distance_rl[1]>37 and distance_rl[2]>58:
                        mess.data=[3,2,2]
                        pub.publish(mess)

                    #mess2.data=distance_rl
                    #print(mess2.data)
                elif second_calibration==True:
                    print("we are now doing the bottom lalala")
                    detection_y(hsv)
                    if t_y and not tracker_y:
                        tracker_y.append(t_y[0])
                    elif t_y and tracker_y:
                        tracker_y_o=tracker_y[0]
                        print("trackery",tracker_y_o,"ydetect",t_y)
                        d_y=dist.euclidean(tracker_y_o[2],t_y[0][2])
                        if d_y>2:
                            tracker_y[0]=t_y[0]
                        elif d_y<2:
                            tracker_y[0]=tracker_y_o
                    elif not t_y:
                        del tracker_y[:]
                        print("no detection keep moving")

                    if len(tracker_y)>0:
                        #print detected
                        ##print the tracker to see how it is working
                        cv2.rectangle(frame,(tracker_y[0][0]),(tracker_y[0][0][0]+tracker_y[0][1][0],tracker_y[0][0][1]+tracker_y[0][1][0]),(255,0,0),2)
                        cv2.rectangle(frame, tracker_y[0][2], (tracker_y[0][2][0]+1, tracker_y[0][2][1]+1), (0, 255, 0), 1)

                        rl_pointy1 = rs.rs2_deproject_pixel_to_point(depth_intrin, [int(tracker_y[0][2][0]),int(tracker_y[0][2][1])], tracker_y[0][3])
                        rl_pointry1 = rs.rs2_deproject_pixel_to_point(depth_intrin, [int(my_trackerb[0][3][0]),int(my_trackerb[0][3][1])], my_trackerb[0][2])

                        distance_y=(dist.euclidean(rl_pointy1,rl_pointry1))*1000
                        print("distance_y",distance_y)
                        if distance_y>110.8:
                            mess.data=[4,1,0]
                            pub.publish(mess)
                        elif distance_y<110.8:
                            mess.data=[4,2,0]
                            pub.publish(mess)
                    elif len(tracker_y)==0:
                        mess.data=[4,2,0]
                        pub.publish(mess)


                # apply colormap to the depth for show
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.02), cv2.COLORMAP_JET)

                hello_str = "hello world %s" % rospy.get_time()
                #rospy.loginfo(hello_str)
                #mess.data=distances
                #pub.publish(mess)


                #print('my trackers_r',my_trackerr)
                #print('my trackers_b',my_trackerb)
                cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('Align Example', depth_colormap)

                cv2.namedWindow('Align Example2', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('Align Example2', frame)

                cv2.namedWindow('hsvr', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('hsvr', hsvr)

                cv2.namedWindow('hsvb', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('hsvb', hsvb)

                cv2.namedWindow('hsvg', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('hsvg', hsvg)

                cv2.namedWindow('hsvy', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('hsvy', hsvy)

                #cv2.namedWindow('frame_changed', cv2.WINDOW_AUTOSIZE)
                #cv2.imshow('frame_changed', normal_frame)

                key = cv2.waitKey(1)
                # Press esc or 'q' to close the image window
                if key & 0xFF == ord('q') or key == 27:
                    cv2.destroyAllWindows()
                    break




        finally:
            pipeline.stop()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
