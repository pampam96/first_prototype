#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from std_msgs.msg import Float64
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState

joint_name = ['Joint1','Joint2','Joint2_2', 'Joint2_3', 'Joint3_1', 'Joint3_2', 'Joint4', 'Joint4_2', 'Joint5']
joint_position=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
joint_velocity=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
joint_effort=[0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
joint_state = JointState()

for i in range(0,4):
    joint_state.name.append(joint_name[i])
    joint_state.position.append(joint_position[i])
    joint_state.velocity.append(joint_velocity[i])
    joint_state.effort.append(joint_effort[i])

def talker():
    pub = rospy.Publisher('chatter', JointState, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        #for i in range(0,4):
        #    joint_state.name.append(joint_name[i])
        #    joint_state.position.append(joint_position[i])
        #    joint_state.velocity.append(joint_velocity[i])
        #    joint_state.effort.append(joint_effort[i])

        joint_state.position[0]=data.data[0]
        rospy.loginfo(joint_state)
        pub.publish(joint_state)
        rate.sleep()

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    #pub_msg= Int64MultiArray()
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    joint_state.position[0]=data.data[0]
    joint_pub.publish(joint_state)


def listener():
    rospy.init_node('listener', anonymous=True)

if __name__ == '__main__':
    #talker()
    listener()
    rospy.Subscriber("chatter", Float64MultiArray, callback)
    joint_pub= rospy.Publisher('values',JointState, queue_size=10)
    rospy.spin()
