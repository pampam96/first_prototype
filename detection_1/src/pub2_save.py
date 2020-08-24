#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String,Int32,Int32MultiArray
import serial
import time

port='/dev/ttyACM0'
# check the timeout if it is a problem??
ard = serial.Serial(port,9600,timeout=5)


def talker():
    num_array=[]
    pub = rospy.Publisher('Uinput', Int32MultiArray, queue_size=10)
    rospy.init_node('inputSender', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        #hello_str = "chatter2 %s" % rospy.get_time()

        #for i in range(3):
            #n = raw_input("num :")
            #num_array.append(int(n))


        #FOR the EM tracker tests
        n = raw_input("num :")
        #num_array.append(int(n))

        #serialCommand = 'Serial Data: '+ str(1) + ',' + \
        #                str(num_array[0]) + ',' + \
        #                str(num_array[2]) + ',' + \
        #                str(0) + ',' + \
        #                str(num_array[1])

###For the em tracker
        serialCommand = 'Serial Data: '+ str(1) + ',' + \
                        str(0) + ',' + \
                        str(n) + ',' + \
                        str(0) + ',' + \
                        str(0)


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

        #first lets make sure that this is enough
        #ideal would be to get an answer from arduino but since we dont have the library
        #we make do
        ###Removed for the em tracker
        #time.sleep(12)
        print(num_array)
        mess=Int32MultiArray()
        mess.data=num_array
        #print('val',val)
        for i in range(100):
            rospy.loginfo(mess)
            pub.publish(mess)
            rate.sleep()
            i=i+1
        del num_array[:]


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
