#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import UInt16
from sensor_msgs.msg import JointState


def talker():
    pub = rospy.Publisher('servo', UInt16, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    value=UInt16()
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()

        for i in range(100):
            value.data=2
            rospy.loginfo(value)
            pub.publish(value)
            rate.sleep()

        for i in range(100):
            value.data=1
            rospy.loginfo(value)
            pub.publish(value)
            rate.sleep()

        for i in range(100):
            value.data=0
            rospy.loginfo(value)
            pub.publish(value)
            rate.sleep()

if __name__ == '__main__':
    talker()
    rospy.spin()
