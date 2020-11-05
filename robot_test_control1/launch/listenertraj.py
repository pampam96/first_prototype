#!/usr/bin/env python
import rospy
from control_msgs.msg import FollowJointTrajectoryActionGoal
#this imports are also new
from std_msgs.msg import Int64MultiArray
from std_msgs.msg import Float64MultiArray
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension
from std_msgs.msg import Int64
#
import numpy
import math

#this variable is also new
joint_pub = None
orientation = 0
oldvalues=[0,0,0,0]

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.goal.trajectory.points[-1].positions[1])
    global orientation
    global oldvalues
    #this below is the new added code
    pub_msg= Int64MultiArray()
    #pub_msg.data=data.data
    #check1=data.goal.trajectory.points[-1].positions[1]
    #check2=data.goal.trajectory.points[-1].positions[2]
    if orientation==1:
        print('first case')
        ##rotation joint
        joint1=formater2(data.goal.trajectory.points[-1].positions[1])
        joint2=formater3(data.goal.trajectory.points[-1].positions[2])
        pub_msg.data=[1,joint1]
    elif orientation==0:
        #we are here now
        print('second case')
        #print(data.goal.trajectory.points[-1])
        ##rotation calculation
        joint1=formater1(data.goal.trajectory.points[-1].positions[0])
        ##side translation
        joint2=formater2(data.goal.trajectory.points[-1].positions[1])
        ##middle translation
        joint3=formater3(data.goal.trajectory.points[-1].positions[3])
        #pub_msg.data=[joint1,joint2,joint3,10]
        oldvalues=[5,joint1,joint3,joint2,joint2]
        print("inside chain1 callback")
        print(oldvalues)
        print("inside chain1 callback")

    #print(check1,check2)
    joint_pub.publish(pub_msg)
    #old_values=[pub_msg.data[0],pub_msg.data[1],pub_msg.data[2]]

#this is rn not called
def callback3(data):
    global oldvalues
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.goal.trajectory.points[-1].positions[1])
    #this below is the new added code
    pub_msg= Int64MultiArray()
    #pub_msg.data=data.data
    #check1=data.goal.trajectory.points[-1].positions[1]
    #check2=data.goal.trajectory.points[-1].positions[2]
    joint1=formater2(data.goal.trajectory.points[-1].positions[0])

    print("inside chain2 callback previous value")
    print(oldvalues)
    print("inside chain2 callback previous value")

    oldvalues[2]=joint1
    #print(oldvalues)
    print("inside chain2 callback")
    print(oldvalues)
    print("inside chain2 callback")
    #old_values=[pub_msg.data[0],pub_msg.data[1],pub_msg.data[2]]
    pub_msg.data=oldvalues
    #print(check1,check2)
    joint_pub.publish(pub_msg)

#this is a new function needed for side motor
def formater2(value):
    value=((value*1000)+35)/0.625
    #value=(value+35)*0.625
    return int(value)
#this is a new function needed for center motor
def formater3(value):
    #value=((-(value*1000))+31.25)/0.625
    ##new calcualtion
    #value=(((value*1000))+31.25)/0.625
    ##newest calcualation
    value=(((value*1000))+31.25)/0.6944444
    return int(value)
#this is a new function needed for rotation motor this is to fix it
def formater1(value):
    ##old calculation
    #value=((((value+0.31)*180)/3.14)/0.452)+130
    ##new calcualtion gotta check this
    value=(((-1*value)+1.5)/0.0088235)
    return int(value)
#my test added code



def callback2(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    global orientation
    #print(orientation)
    if data.data==2:
        orientation=1
    else:
        orientation=0
    #print(orientation)


#my test added code again
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.

    rospy.init_node('listener', anonymous=True)

    #rospy.Subscriber("/robot_test/chain_position_controller/follow_joint_trajectory/goal", FollowJointTrajectoryActionGoal, callback)

    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()

if __name__ == '__main__':
    listener()
    #listener2()
    rospy.Subscriber("chatter", Int64, callback2)
    #print(orientation,'before main')

    rospy.Subscriber("/robot_test/chain_position_controller/follow_joint_trajectory/goal", FollowJointTrajectoryActionGoal, callback)
    #second subscriber
    rospy.Subscriber("/robot_test/chain_position_controller2/follow_joint_trajectory/goal", FollowJointTrajectoryActionGoal, callback3)

    #trying to have the publisher do different stuff within callbakcs
    joint_pub= rospy.Publisher('values',Int64MultiArray, queue_size=10)

    print(oldvalues)
    #this wasnt here before

    rospy.spin()
    #this wasnt here before
