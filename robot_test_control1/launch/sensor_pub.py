#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState


def talker():
    pub = rospy.Publisher('chatter', Float64MultiArray, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    joint_state=Float64MultiArray()
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        joint_state.data=[-0.0002866227271205446,0.3,0.7]
        rospy.loginfo(joint_state)
        pub.publish(joint_state)
        rate.sleep()

if __name__ == '__main__':
    talker()
    rospy.spin()
