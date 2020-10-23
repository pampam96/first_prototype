#!/usr/bin/env python
import rospy
from std_msgs.msg import String,Int32,Int32MultiArray,Float32MultiArray

in_1=[];

distance=[]
value=[]
bool=1
send_pos=False
num_array=[]

def callback(data):
    #rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    global send_pos
    print("boolean",send_pos)
    if send_pos==False:
        del num_array[:]
        for i in range(4):
            n = raw_input("num :")
            num_array.append(int(n))
        mess.data=[5,num_array[0],num_array[1],num_array[2],num_array[3]]
        send_pos=True
        print("boolean turned True",send_pos)
    if send_pos==True:
        print("boolean inside True",send_pos)
        print("mess",mess.data)
        print("data",data.data)
        comparison=[int(data.data[0]),int(data.data[1]),int(data.data[2]),int(data.data[3])]
        if comparison!=num_array:
            print("not equal")
            pub.publish(mess)
        if comparison==num_array:
            print("reached")
            send_pos=False

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
    ##Publisher
    rospy.Subscriber("chatter", Float32MultiArray, callback)
    rospy.Subscriber("distance", Int32MultiArray, callback2)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':



    #value = input("Please enter a string:\n")

    pub = rospy.Publisher('distance', Int32MultiArray, queue_size=10)

    rospy.init_node('listener', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    mess=Int32MultiArray()
    ###############
    for i in range(4):
        n = raw_input("num :")
        num_array.append(int(n))

    mess.data=[5,num_array[0],num_array[1],num_array[2],num_array[3]]
    pub.publish(mess)

    listener()

    #rospy.init_node('listener', anonymous=True)
    #rospy.Subscriber("chatter", String, callback)
    # spin() simply keeps python from exiting until this node is stopped
    #rospy.spin()
    print('main distance',distance,'value',value)
