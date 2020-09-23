import matplotlib.pyplot as plt
import csv

x = []
y = []
index=[]

x2 = []
y2 = []
index2=[]

with open('data/test2_3_it1.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x.append(int(row[0]))
        y.append(int(row[1]))
        index.append(i)
        
with open('data/test2_2_it1.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x2.append(int(row[0]))
        y2.append(int(row[1]))
        index2.append(i)

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
plt.scatter(y,x,c='blue', s=2,alpha=0.2,edgecolors='None')
plt.scatter(y2,x2,c='red',s=2, alpha=0.2, edgecolors='None')
plt.xlabel('Distance')
plt.ylabel('Real Value')
plt.title('test2')
plt.legend()
plt.show()
