#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 11:25:16 2020

@author: marcey
"""
distance=[5,5,7]
value=[8,9,107]
files=["test1.txt","test2.txt","test3.txt"]
for i in range(3):
    test=[distance[i],value[i]]
    test=str(test).strip('[]')
    with open(files[i], "a") as myfile:
        myfile.write(test+"\n")