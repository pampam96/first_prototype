#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String,Int32,Int32MultiArray
import cv2                                # state of the art computer vision algorithms library
import numpy as np                        # fundamental package for scientific computing
import matplotlib.pyplot as plt           # 2D plotting library producing publication quality figures
import pyrealsense2 as rs                 # Intel RealSense cross-platform open-source API
from scipy.spatial import distance as dist
print("Environment Ready")

def talker():

    ####### ROS variables ######
    pub = rospy.Publisher('distance', Int32MultiArray, queue_size=10)
    rospy.init_node('dSender', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    mess=Int32MultiArray()
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

    ##### other variables #######
    threshold=100
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
    def red_hsv():
        lower_red = np.array([0,143,0])
        upper_red = np.array([12,255,255])

        lower_red2 = np.array([118,73,0])
        upper_red2 = np.array([179,255,255])

        hsvr1 = cv2.inRange(hsv, lower_red, upper_red)
        hsvr2 = cv2.inRange(hsv, lower_red2, upper_red2)
        hsvr=hsvr1 +hsvr2
        #hsvr=cv2.morphologyEx(hsvr, cv2.MORPH_CLOSE, kernel)
        hsvr=cv2.morphologyEx(hsvr, cv2.MORPH_OPEN, kernel)
        return hsvr

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
                #print('bounding rec', x,y,w,h)
                xy,wh,r=cv2.minAreaRect(cnt)
                #print('rectangle', rect)#this has (x,y),(w,h),(rot)
                #box=cv2.boxPoints(rect)# four x,y
                #print('box',box)
                #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                #cv2.rectangle(frame, (int(xy[0]),int(xy[1])), (int(xy[0] + wh[0]), int(xy[1] + wh[1])), (0, 255, 255), 1)

                zDepth=aligned_depth_frame.get_distance(int(x+w/2),int(y+h/2))
                track_init.append([(x,y),(w,h),M['m00'],zDepth])
        #print('t_init_r',track_init)
        for i,t in enumerate(track_init):
            if t[3]>0.40:
                del track_init[i]
        #return(hsvr)

    def detection_b(hsv2):

        # define range of blue color in HSV
        lower_blue = np.array([104,170,0])
        upper_blue = np.array([179,255,255])

        lower_blue2 = np.array([107,100,0])
        lower_blue21 = np.array([35,150,0])
        upper_blue2 = np.array([134,255,255])
        # Threshold the HSV image to get only blue colors
        hsvb = cv2.inRange(hsv2, lower_blue2, upper_blue2)
        #hsvb2 = cv2.inRange(hsv2, lower_blue21, upper_blue2)
        #hsvb=hsvb2+hsvb
        #hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_CLOSE, kernel)
        #hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_OPEN, kernel)

        ####Detection Code###########
        im2,contours,hierarchy= cv2.findContours(hsvb, 1, 2)

        #print(len(contours))
        for cnt in contours:
            M=cv2.moments(cnt)
            if M['m00']>threshold:
                #print('blob detected')
                x,y,w,h = cv2.boundingRect(cnt)
                zDepth=aligned_depth_frame.get_distance(int(x),int(y))
                #cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                if zDepth<0.40:
                    t_init_b.append([(x,y),(w,h),M['m00'],zDepth])
        #print('t_init_b',t_init_b)
        for i,t in enumerate(t_init_b):
            if t[3]>0.46:
                del t_init_b[i]


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
            marker1 = dist.euclidean(marker[0][3], (276,230))
            marker2 = dist.euclidean(marker[1][3], reference[0][3])
            marker3 = dist.euclidean(marker[2][3], reference[1][3])

            distances.append(marker1)
            distances.append(marker2)
            distances.append(marker3)
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

    ########## histogram matching #########
    def calculate_cdf(histogram):
    """
    This method calculates the cumulative distribution function
    :param array histogram: The values of the histogram
    :return: normalized_cdf: The normalized cumulative distribution function
    :rtype: array
    """
    # Get the cumulative sum of the elements
        cdf = histogram.cumsum()

    # Normalize the cdf
        normalized_cdf = cdf / float(cdf.max())

        return normalized_cdf

    def calculate_lookup(src_cdf, ref_cdf):
    """
    This method creates the lookup table
    :param array src_cdf: The cdf for the source image
    :param array ref_cdf: The cdf for the reference image
    :return: lookup_table: The lookup table
    :rtype: array
    """
        lookup_table = np.zeros(256)
        lookup_val = 0
        for src_pixel_val in range(len(src_cdf)):
            lookup_val
            for ref_pixel_val in range(len(ref_cdf)):
                if ref_cdf[ref_pixel_val] >= src_cdf[src_pixel_val]:
                    lookup_val = ref_pixel_val
                    break
            lookup_table[src_pixel_val] = lookup_val
        return lookup_table

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

                depth_image = np.asanyarray(aligned_depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())

                frame=color_image#+7
                frame2=color_image#+7
                frame_count=frame_count+1

                #frame_changed,a,b=autoAdjustments_with_convertScaleAbs(frame)

                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                hsv2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)

                #### update the trackers
                (success, boxes) = trackers.update(frame)
                (successb, boxesb) = trackers_b.update(frame)

                #1print('success1',success)
                #print('success2',successb)

                ### iterate through trackers, draw them on frame and update my tracker list
                for i,box in enumerate(boxes):
                    pix_height=[]
                    xy_pix_height=[]
                    (x, y, w, h) = [int(v) for v in box]
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
                    centroid=(x+w/2,y+h/2)
                    #centroid2=(int(x+w),int(y+h))
                    centroid3=(int(x+w/3),int(y+h/3))
                    ######
                    cv2.rectangle(frame, centroid, (centroid[0]+1, centroid[1]+1), (0, 255, 0), 1)
                    #cv2.rectangle(frame, centroid2, (centroid2[0]+1, centroid2[1]+1), (0, 255, 0), 1)
                    cv2.rectangle(frame, centroid3, (centroid3[0]+1, centroid3[1]+1), (0, 255, 0), 1)

                    ######
                    cv2.putText(frame,str(i),(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),3)

                    zDepth=aligned_depth_frame.get_distance(int(x+w/2),int(y+h/2))
                    my_trackerr[i][2]=zDepth
                    my_trackerr[i][3]=centroid

                    for i in range(x,x+w):
                        for j in range(y,y+h):
                            zd=aligned_depth_frame.get_distance(int(i),int(j))
                            val=abs(zd-zDepth)
                            if val<0.01:
                                pix_height.append(zd)
                                xy=(i,j)
                                xy_pix_height.append(xy)

                    #for xy in xy_pix_height:
                    #    cv2.rectangle(frame, xy, (xy[0]+1, xy[1]+1), (0, 255, 0), 1)

                    #zDepth1=aligned_depth_frame.get_distance(int(x+w/0.5),int(y+h/0.5))
                    zDepth2=aligned_depth_frame.get_distance(int(x+w/3),int(y+h/3))

                    print('Depths of points around',pix_height)



                ### iterate through trackers, draw them on frame and update my tracker list
                for i,box in enumerate(boxesb):
                    pix_height=[]
                    xy_pix_height=[]
                    (x, y, w, h) = [int(v) for v in box]
                    centroid=(x+w/2,y+h/2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
                    cv2.rectangle(frame, centroid, (centroid[0]+1, centroid[1]+1), (0, 255, 0), 1)
                    cv2.putText(frame,str(i),(x,y),cv2.FONT_HERSHEY_SIMPLEX,1,(255, 255, 255),3)
                    zDepthb=aligned_depth_frame.get_distance(int(x+w/2),int(y+h/2))
                    my_trackerb[i][2]=zDepthb
                    my_trackerb[i][3]=centroid

                    for i in range(x,x+w):
                        for j in range(y,y+h):
                            zd=aligned_depth_frame.get_distance(int(i),int(j))
                            val=abs(zd-zDepthb)
                            if val<0.01:
                                pix_height.append(zd)
                                xy=(i,j)
                                xy_pix_height.append(xy)

                    #for xy in xy_pix_height:
                    #    cv2.rectangle(frame, xy, (xy[0]+1, xy[1]+1), (0, 255, 0), 1)



                ### create hsv images so you can show them not needed in the future
                hsvr=red_hsv()
                hsvb=blue_hsv()

                # apply colormap to the depth for show
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.02), cv2.COLORMAP_JET)

                hello_str = "hello world %s" % rospy.get_time()
                mess.data=distances
                #rospy.loginfo(hello_str)
                pub.publish(mess)
                del distances[:]
                #print('my trackers_b',my_trackerb)
                distance(my_trackerr,my_trackerb)
                #detection_r(hsv)

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

                cv2.namedWindow('frame_changed', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('frame_changed', normal_frame)

                key = cv2.waitKey(1)
                # Press esc or 'q' to close the image window
                if key & 0xFF == ord('q') or key == 27:
                    cv2.destroyAllWindows()
                    break

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
                    for bl in track_init:
                        tracker = OPENCV_OBJECT_TRACKERS[trackername]()
                        trackers.add(tracker, frame, (bl[0][0],bl[0][1],bl[1][0],bl[1][1]))
                        centroid=(bl[0][0]+bl[1][0]/2,bl[0][1]+bl[1][1]/2)
                        ### apend to my list of trackers
                        my_trackerr.append([bl[0],bl[1],0,centroid])
                    #### iterate through detected and init a tracker for reference
                    for bl in t_init_b:
                        tracker = OPENCV_OBJECT_TRACKERS[trackername]()
                        trackers_b.add(tracker, frame, (bl[0][0],bl[0][1],bl[1][0],bl[1][1]))
                        centroid=(bl[0][0]+bl[1][0]/2,bl[0][1]+bl[1][1]/2)
                        ### append to my list of trackers
                        my_trackerb.append([bl[0],bl[1],0,centroid])

                #elif frame_count==120:
                elif success==False or successb==False or frame_count==100:

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
                    for box in boxes:
                        (x, y, w, h) = [int(v) for v in box]
                        old_trackerc.append((x,y))
                        old_trackerb.append((w,h))

                    old_value=old_trackerc
                    #reference appending on needed lists
                    ### iterating through detector
                    for obj in t_init_b:
                        det_b.append(obj[0])
                    ### iterating through the old tracker
                    for box in boxesb:
                        (x, y, w, h) = [int(v) for v in box]
                        old_tbc.append((x,y))
                        old_tbb.append((w,h))

                    #matcher for marker
                    matcher(old_trackerc,detector)
                    #matcher for reference
                    matcherb(old_tbc,det_b)

                    ### clear marker multitracker class
                    trackers.clear()
                    ### create new kcf tracker class
                    trackers = cv2.MultiTracker_create()

                    #### add trackers to the new multiObject
                    for i, bl in enumerate(old_trackerc):
                        tracker = OPENCV_OBJECT_TRACKERS[trackername]()
                        #print('',old_trackerb)
                        new_area=0
                        old_area=0

                        if len(bl)==4:
                            new_area=bl[1][0]*bl[1][1]
                            old_area=old_trackerb[i][0]*old_trackerb[i][1]

                        ### if it has been matched get new width and length
                        if len(bl)==4 and new_area>old_area-100 :
                            print('its getting new square')
                            trackers.add(tracker, frame, (bl[0][0],bl[0][1],bl[1][0],bl[1][1]))
                            print('new square is ',bl[1][0],bl[1][1])
                            #trackers.add(tracker, frame, (bl[0][0],bl[0][1],old_trackerb[i][0],old_trackerb[i][1]))
                        elif len(bl)==4 and new_area<old_area-15:
                            trackers.add(tracker, frame, (bl[0][0],bl[0][1],old_trackerb[i][0],old_trackerb[i][1]))
                        else:
                            ### if it hasnt been matched keep old values
                            trackers.add(tracker, frame, (bl[0],bl[1],old_trackerb[i][0],old_trackerb[i][1]))

                    ### clear marker multitracker class
                    trackers_b.clear()
                    ### create new kcf tracker class
                    trackers_b = cv2.MultiTracker_create()
                    #print(len(t_init_b))

                    #### add trackers to the new multiObject
                    for i, bl in enumerate(old_tbc):
                        tracker = OPENCV_OBJECT_TRACKERS[trackername]()
                        new_area=0
                        old_area=0

                        if len(bl)==4:
                            new_area=bl[1][0]*bl[1][1]
                            old_area=old_tbb[i][0]*old_tbb[i][1]

                        ### if it has been matched get new width and length
                        if len(bl)==4 and new_area>old_area-100:
                            trackers_b.add(tracker, frame, (bl[0][0],bl[0][1],bl[1][0],bl[1][1]))
                            #trackers_b.add(tracker, frame, (bl[0][0],bl[0][1],old_tbb[i][0],old_tbb[i][1]))
                        elif len(bl)==4 and new_area<old_area-15:
                            trackers_b.add(tracker, frame, (bl[0][0],bl[0][1],old_tbb[i][0],old_tbb[i][1]))
                        elif len(bl)!=4:
                        ### if it hasnt been matched keep old values
                            trackers_b.add(tracker, frame, (bl[0],bl[1],old_tbb[i][0],old_tbb[i][1]))
                    frame_count=61


        finally:
            pipeline.stop()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
