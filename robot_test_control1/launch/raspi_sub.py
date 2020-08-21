#!/usr/bin/env python
import rospy
from std_msgs.msg import Int64MultiArray
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension
import numpy
import sys
import serial
import time

port='/dev/ttyACM0'
ard = serial.Serial(port,9600,timeout=5)
#oldvalues=[0,0,0]
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)

    serialCommand = 'Serial Data: '+ str(1) + ',' + \
                    str(data.data[0]) + ',' + \
                    str(data.data[1]) + ',' + \
                    str(data.data[2]) + ',' + \
                    str(data.data[3])

    #self.msg.setText(serialCommand + ??)
    print(serialCommand)

    if port == '':
        print("None")
    elif port == '/dev/ttyACM0':
        try:
            ard.write(serialCommand.encode())
            print('Arduino Host: Connected')
        except:
            print("Serial Data: Failed")
            print(port)
            print('Arduino Host: Not Connected to Linux')

    elif port == 'COM5':
        try:
            ard.write(serialCommand.encode())
            print('Arduino Host: Connected')
        except:
            print("Serial Data: Failed")
            print(self.port)
            print('Arduino Host: Not Connected to Windows')


def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listenerpi', anonymous=True)

    rospy.Subscriber("values", Int64MultiArray, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
