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
        #0 172 0
        #6 255 255
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

        lower_blue2 = np.array([0,172,0])
        upper_blue2 = np.array([6,255,255])
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
            if M['m00']>threshold2:
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
        lower_blue2 = np.array([0,172,0])
        upper_blue2 = np.array([6,255,255])
        # Threshold the HSV image to get only blue colors
        hsvb = cv2.inRange(hsv2, lower_blue2, upper_blue2)
        #hsvb2 = cv2.inRange(hsv2, lower_blue21, upper_blue2)
        #hsvb=hsvb2+hsvb
        hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_CLOSE, kernel)
        #hsvb=cv2.morphologyEx(hsvb, cv2.MORPH_OPEN, kernel)

        ####Detection Code###########
        im2,contours,hierarchy= cv2.findContours(hsvb, 1, 2)

        #( actual distance 5.7 cm with 5.7 cm)
        #print(len(contours))
        for cnt in contours:
            M=cv2.moments(cnt)
            if M['m00']>threshold2:
                #print('blob detected')
                x,y,w,h = cv2.boundingRect(cnt)
                zDepth=aligned_depth_frame.get_distance(int(x),int(y))
                end=(x+w,y+h)
                distance=dist.euclidean((x,y), end)
                centroid=(x+w/2,y+h/2)
                point2=(x+w,y+h/2)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
                cv2.rectangle(frame, centroid, (centroid[0]+1, centroid[1]+1), (0, 255, 0), 1)
                cv2.rectangle(frame, point2, (point2[0]+1, point2[1]+1), (0, 255, 0), 1)
                zDepth=aligned_depth_frame.get_distance(int(x+w/2),int(y+h/2))
                zDepth1=aligned_depth_frame.get_distance(int(x+w),int(y+h/2))
                rl_point = rs.rs2_deproject_pixel_to_point(depth_intrin, [int(x+w/2),int(y+h/2)], zDepth)
                rl_point2 = rs.rs2_deproject_pixel_to_point(depth_intrin, [int(x+w),int(y+h/2)], zDepth1)
                t_init_b.append([(x,y),(w,h),distance,M['m00'],zDepth,rl_point])
                distance_rl=dist.euclidean(rl_point, rl_point2)
                #print('distance',distance_rl,'depthright',zDepth1,'depthmiddle',zDepth,'rlpoint',rl_point,'rlpoint2',rl_point2)
                print('zDepth',zDepth1)
                #print('rlpoint middle',rl_point,'rlpoint2',rl_point2)
                print('rlpoint2',rl_point2)
                print('distance',distance_rl)
        #print('t_init_b',t_init_b)


    while not rospy.is_shutdown():
        #rate.sleep()
        try:
            ######### this is practically main #############
            while True:
                # Get frameset of color and depth
                frames = pipeline.wait_for_frames()
                # frames.get_depth_frame() is a 640x360 depth image

                # Align the depth frame to color frame
                aligned_frames = align.process(frames)

                # Get aligned frames
                aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
                color_frame = aligned_frames.get_color_frame()

                depth_intrin = aligned_depth_frame.profile.as_video_stream_profile().intrinsics
                color_intrin = color_frame.profile.as_video_stream_profile().intrinsics

                #print('depth_intrin',depth_intrin)
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


                ### create hsv images so you can show them not needed in the future
                hsvr=red_hsv()
                hsvb=blue_hsv()

                del t_init_b[:]
                detection_b(hsv2)



                # apply colormap to the depth for show
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.02), cv2.COLORMAP_JET)

                hello_str = "hello world %s" % rospy.get_time()
                mess.data=[1,2]
                #rospy.loginfo(hello_str)
                pub.publish(mess)
                #print('my trackers_b',my_trackerb)                #detection_r(hsv)

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
