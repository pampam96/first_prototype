#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  2 09:29:58 2020

@author: marcey
"""
import numpy as np
from sklearn import datasets, linear_model
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
import csv

x = []
y = []
index=[]

x2 = []
y2 = []
index2=[]

## side motor

with open('test2_3.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x.append(int(row[0]))
        y.append(int(row[1]))
        index.append(i)
        
with open('test2_2.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x2.append(int(row[0]))
        y2.append(int(row[1]))
        index2.append(i)


# Split the data into training/testing sets
test_nr=int(len(x)*0.8)
x_train = x[:test_nr]
x_test = x[test_nr:]


# Split the targets into training/testing sets
y_train = y[:test_nr]
y_test = y[test_nr:]

# Create linear regression object
regr = linear_model.LinearRegression()

##linear regression
poly = PolynomialFeatures(degree = 4) 

Input=[('polynomial',PolynomialFeatures(degree=4)),('modal',LinearRegression())]
pipe=Pipeline(Input)

x_train=np.array(x_train).reshape(-1,1)
y_train=np.array(y_train).reshape(-1,1)
x_test=np.array(x_test).reshape(-1,1)
y_test=np.array(y_test).reshape(-1,1)

# Train the model using the training sets
regr.fit(x_train, y_train)
y_pred = regr.predict(x_test)

##poly fit
X_poly = poly.fit_transform(x_train) 
poly.fit(X_poly, y_train) 
lin2 = LinearRegression() 
lin2.fit(X_poly, y_train) 

##second try with polyfit
pipe.fit(x_train,y_train)
poly_pred=pipe.predict(x_test)
#sorting predicted values with respect to predictor
sorted_zip = sorted(zip(x_test,poly_pred))
x_poly, poly_pred = zip(*sorted_zip)

#prediction part
# Plot outputs

plt.scatter(x_test, y_test,  color='black')
plt.plot(x_test, y_pred, color='blue', linewidth=3)

plt.xticks(())
plt.yticks(())
plt.title('Polynomial Regression') 
plt.xlabel('Raw distance data') 
plt.ylabel('Actual step') 

plt.show()


# Visualising the Polynomial Regression results 
#plt.scatter(x_test, y_test, color = 'blue') 
  
plt.plot(x_test, lin2.predict(poly.fit_transform(x_test)), color = 'red') 
plt.title('Polynomial Regression') 
plt.xlabel('Raw distance data') 
plt.ylabel('Actual step') 
  
plt.show() 


plt.plot(x_poly,poly_pred,color='g',label='Polynomial Regression')
plt.xlabel('Raw Distance data',fontsize=16)
plt.ylabel('Actual step',fontsize=16)
plt.legend()
plt.show()


