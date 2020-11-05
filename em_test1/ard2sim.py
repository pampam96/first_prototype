#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 22:07:15 2020

@author: marcey
"""

import math as m
arduino_values=[[340,45,34,19],[0,45,34,19],[0,0,34,19],[0,0,0,19],
                [0,0,0,0],[0,0,112,112],[340,0,112,112],[340,0,0,0],
                [340,90,0,0],[340,90,112,112],[0,90,112,112],[0,90,0,0],
                [0,45,0,0],[170,45,0,0],[170,45,5,0],[170,45,10,0],
                [170,45,15,0],[170,45,20,0],[170,45,25,0],[170,45,30,0],
                [170,45,56,56],[170,45,56,50],[170,45,56,45],[170,45,56,40],
                [169,45,29,16],[169,45,7,16],[169,45,54,16],[340,45,29,16],
                [0,45,29,16],[0,45,7,16],[340,45,7,16],[0,45,60,16]]

#arduino_values=[[0,0,0,0]]
#arduino_values=[[340,45,34,19]]

#arduino_value=[340,45,34,19] #angle -0.23121
#arduino_value=[0,45,34,19]
#arduino_value=[0,0,34,19]
#arduino_value=[0,0,19,19]
#arduino_value=[0,0,0,0]
#arduino_value=[0,0,112,112]
#arduino_value=[340,0,112,112]
#arduino_value=[340,0,0,0]
#arduino_value=[340,0,112,112]
#arduino_value=[340,0,0,0]
#arduino_value=[340,90,0,0]
#arduino_value=[340,90,112,112]
#arduino_value=[0,90,112,112]
#arduino_value=[0,90,0,0]
#arduino_value=[0,45,0,0]
#arduino_value=[170,45,0,0]
#
##multiple val
#arduino_value=[170,45,5,0]
#arduino_value=[170,45,10,0]
#arduino_value=[170,45,15,0]
#arduino_value=[170,45,20,0]
#arduino_value=[170,45,25,0]
arduino_values=[[170,45,30,0]]
##
#
#arduino_value=[170,45,56,56]
#
##multiple val
#arduino_value=[170,45,56,50]
#arduino_value=[170,45,56,45]
#arduino_value=[170,45,56,40]
##
#
#arduino_value=[169,45,29,16]
#arduino_value=[169,45,7,16]
#arduino_value=[169,45,54,16]
#arduino_value=[340,45,29,16]
#arduino_value=[0,45,29,16]
#arduino_value=[0,45,7,16]
#arduino_value=[340,45,7,16]
#arduino_value=[0,45,60,16]


#this is a new function needed for side motor
def formater2(value):
    ard_value=((value*0.625)-35)/1000
    return ard_value
#this is a new function needed for center motor distance 0.0625
def formater3(value):
    ard_value=((value*0.6944444)-31.25)/1000
    return ard_value
#this is a new function needed for rotation motor this is to fix it
def formater1(value):
    ard_value=((value*0.0088235)-1.5)*-1
    return ard_value
#my test added code
print("length",len(arduino_values))



for i in range (0,len(arduino_values))  : 
    rotation=formater1(arduino_values[i][0])
    middle=formater3(arduino_values[i][1])
    bottom_trans=formater2(arduino_values[i][2])
    top_trans=formater2(arduino_values[i][3])
    
    if top_trans>bottom_trans:
        val=abs(top_trans-bottom_trans)/0.04
        #print("val",val, "abs",abs(top_trans-bottom_trans))
        angle=m.acos(val)
        #print("angle 1",angle)
    
    if top_trans==bottom_trans:
        b=3+2
        #print("angle 0")
    
    if top_trans<bottom_trans:
        #print("val",val,"abs",abs(top_trans-bottom_trans))
        val=abs(top_trans-bottom_trans)/0.04
        angle=m.acos(val)
        #print("angle 2",angle)
    
    print(rotation,top_trans,middle,bottom_trans)
