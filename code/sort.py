#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 31 13:38:05 2020

@author: marcey
"""
from scipy.spatial import distance as dist


lista=[[(378, 278), (18, 19), 303.0, 0.31200000643730164], [(286, 227), (14, 15), 180.5, 0.39100003242492676], [(332, 54), (38, 23), 163.5, 0.3140000104904175]]

print(len(lista))

def sortThird(val):
    return val[3]
def sortSecond(val):
    return val[2]

lista.sort(key=sortThird,reverse=True)
print('before',lista)
new=lista[1:]
new.sort(key=sortSecond,reverse=True)
lista[1:]=new
#lista = lista[0] + lista[1:len(lista)].sort(key=sortSecond)
print('after',lista)

D=dist.cdist((273,239), (286,227))
print(D)