#!/usr/bin/env python
# license removed for brevity
import rospy
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray

var_pub = None

def markmaker():
    #pub = rospy.Publisher('visualization_marker_array', MarkerArray, queue_size=40)
    rospy.init_node('markmaker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    markerArray = MarkerArray()
    ##before em tracker
    #positionx=[0,0,-0.04,-0.025,0.015,-0.025,0.055,0.055,0.03,0.01,0.045,0,0.03,-0.055,-0.045]
    #positiony=[0,-0.02,-0.02,-0.04,0.025,0.025,0.025,-0.035,-0.04,-0.045,0,0.045,0.045,0,0.03]

    ##em tracker
    positiony=[0,0,0.04,0.025,-0.015,0.025,-0.055,-0.055,-0.03,-0.01,-0.045,0,-0.03,0.055,0.045]
    positionx=[0,-0.02,-0.02,-0.04,0.025,0.025,0.025,-0.035,-0.04,-0.045,0,0.045,0.045,0,0.03]

    publishonce=True

    while not rospy.is_shutdown():
        if len(markerArray.markers)<2:
            for i in range(14,15):
                marker = Marker()
                marker.id=i
                marker.header.frame_id = "/world"
                marker.type = marker.SPHERE
                marker.action = marker.ADD
                marker.scale.x = 0.002
                marker.scale.y = 0.002
                marker.scale.z = 0.002
                marker.color.a = 1.0
                marker.color.r = 1.0
                marker.color.g = 1.0
                marker.color.b = 0.0
                marker.pose.orientation.w = 1.0
                marker.pose.position.x = positionx[i]
                marker.pose.position.y = positiony[i]
                marker.pose.position.z = 0.1
                markerArray.markers.append(marker)

        marker = Marker()
        marker.header.frame_id = "/map"
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = 0.2
        marker.scale.y = 0.2
        marker.scale.z = 0.2
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = 0
        marker.pose.position.y = 0
        marker.pose.position.z = 0

        #rospy.loginfo(marker)
        #pub.publish(marker)
        #pub.publish(markerArray)
        #while publishonce:
        var_pub.publish(markerArray)
        print(len(markerArray.markers))
        publishonce= False
        rate.sleep()

if __name__ == '__main__':

    var_pub = rospy.Publisher('visualization_marker_array', MarkerArray, queue_size=40)
    markmaker()
    rospy.spin()
