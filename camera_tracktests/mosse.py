import matplotlib.pyplot as plt
import csv

d1 = []
d2 = []
a1 = []
a2 = []
index=[]

d1_1 = []
d2_1 = []
a1_1 = []
a2_1= []
index=[]

#x2 = []
#y2 = []
#index2=[]

with open('mosse_10_23_16_59_55.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        d1.append(int(float(row[0]))-38)
        d2.append(int(float(row[1]))-56)
        a2.append(int(float(row[2])*0.6944444))
        a1.append(int(float(row[3])*0.625))
        index.append(i)
        
with open('mosse_10_23_17_13_31.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        d1_1.append(int(float(row[0]))-38)
        d2_1.append(int(float(row[1]))-56)
        a2_1.append(int(float(row[2])*0.6944444))
        a1_1.append(int(float(row[3])*0.625))
        index.append(i)
#with open('data/test2_2_it1.txt','r') as csvfile:
#    plots = csv.reader(csvfile, delimiter=',')
#    for i,row in enumerate(plots):
#        x2.append(int(row[0]))
#        y2.append(int(row[1]))
#        index2.append(i)

#plt.scatter(x,y,c='red', s=2)
#plt.figure()
#plt.scatter(index,x,c='red', s=2)
#plt.scatter(index,y,c='blue', s=2)
#plt.xlabel('Value')
#plt.ylabel('Iteration')
#plt.title('Real value in blue vs distance in red')
#plt.legend()
#plt.show()
        
#plt.figure()
##plt.scatter(x,y,c='red', s=2)
#plt.scatter(index,x,c='red', s=2)
#plt.scatter(index,y,c='blue', s=2)
#plt.xlabel('Distance')
#plt.ylabel('Real Value')
#plt.title('test 2_3')
#plt.legend()
#plt.show()

#plt.figure()
##plt.scatter(x2,y2,c='blue', s=2)
#plt.scatter(index2,x2,c='red',s=2, alpha=0.2, edgecolors='None')
#plt.scatter(index2,y2,c='blue', s=2)
#plt.xlabel('Distance')
#plt.ylabel('Real Value')
#plt.title('test2')
#plt.legend()
#plt.show()
#
        
##figure3
#plt.figure()
##plt.scatter(x2,y2,c='blue', s=2)
#plt.scatter(index2,x2,c='red',s=2, alpha=0.2, edgecolors='None')
#plt.scatter(index,x,c='blue', s=2,edgecolors='None')
#plt.xlabel('Distance')
#plt.ylabel('Real Value')
#plt.title('test2')
#plt.legend()
#plt.show()

#figure4
plt.figure()
#plt.scatter(x2,y2,c='blue', s=2)
plt.scatter(a1,d1,c='blue', s=2,alpha=0.5,edgecolors='None')
plt.scatter(a1_1,d1_1,c='green', s=2,alpha=0.5,edgecolors='None')
plt.xlabel('Real Value in mm')
plt.ylabel('Distance in mm')
plt.title('MOSSE Tests Side motor')
plt.legend()
plt.show()

plt.figure()
plt.scatter(a2_1,d2_1,c='black',s=2, alpha=0.2, edgecolors='None')
plt.scatter(a2,d2,c='red',s=2, alpha=0.2, edgecolors='None')
plt.xlabel('Real Value in mm')
plt.ylabel('Distance in mm')
plt.title('MOSSE Tests Middle motor')
plt.legend()
plt.show()