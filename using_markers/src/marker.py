#!/usr/bin/env python

from visualization_msgs.msg import Marker
import rospy
import math

def talker():
    topic = 'visualization_marker'
    publisher = rospy.Publisher(topic, Marker,queue_size=10)
    rospy.init_node('register', anonymous=True)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        marker = Marker()
        marker.header.frame_id = "/camera_link"
        marker.type = marker.SPHERE
        marker.action = marker.ADD
        marker.scale.x = 0.02
        marker.scale.y = 0.02
        marker.scale.z = 0.02
        marker.color.a = 1.0
        marker.color.r = 1.0
        marker.color.g = 1.0
        marker.color.b = 0.0
        marker.pose.orientation.w = 1.0
        marker.pose.position.x = 0
        marker.pose.position.y = 0
        marker.pose.position.z = 0

        #rospy.loginfo(hello_str)
        publisher.publish(marker)
        rospy.sleep(0.01)

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
