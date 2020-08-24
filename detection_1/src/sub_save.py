#!/usr/bin/env python
import rospy
from std_msgs.msg import String,Int32,Int32MultiArray

in_1=[];

distance=[]
value=[]
bool=1
def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    global distance
    value=data.data
    #distance=data.data
    files=["test1_10.txt","test2_10.txt","test3_10.txt"]
    print('distance',distance,'value',value)
    if len(distance)==3 and len(value)==3:
        for i in range(3):
            test=[distance[i],value[i]]
            test=str(test).strip('[]')
            with open(files[i], "a") as myfile:
                myfile.write(test+"\n")


def callback2(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    global distance
    distance=data.data
    #print('distance2',distance)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    global value

    #value = input("Please enter a string:\n")

    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("Uinput", Int32MultiArray, callback)
    rospy.Subscriber("distance", Int32MultiArray, callback2)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':



    #value = input("Please enter a string:\n")

    listener()

    #rospy.init_node('listener', anonymous=True)
    #rospy.Subscriber("chatter", String, callback)
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()
    print('main distance',distance,'value',value)
