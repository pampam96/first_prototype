#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import UInt16
from sensor_msgs.msg import JointState


def talker():
    pub = rospy.Publisher('servo', Float64MultiArray, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    value=UInt16()
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        value.data=0
        rospy.loginfo(value)
        pub.publish(value)
        rate.sleep()

if __name__ == '__main__':
    talker()
    rospy.spin()
