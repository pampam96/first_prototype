from scipy.spatial import distance
import csv

x = []
y = []
z = []
index=[]

with open('9_11_09_48_18_sm.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x.append(round(float(row[0]),0)/1000)
        y.append(round(float(row[1]),0)/1000)
        z.append(round(-float(row[2]),0)/1000)
        index.append(i)

a1 = (x[0], y[0], z[0])
b1 = (x[659], y[659], z[659])

dst = distance.euclidean(a1, b1)
print(dst) ### almost as expected for right side 

x2 = []
y2 = []
z2 = []
index2=[]

with open('9_11_09_53_40_smr.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x2.append(round(float(row[0]),0)/1000)
        y2.append(round(float(row[1]),0)/1000)
        z2.append(round(-float(row[2]),0)/1000)
        index2.append(i)
        
a2 = (x2[0], y2[0], z2[0])
b2 = (x2[458], y2[458], z2[458])

dst = distance.euclidean(a2, b2)
print(dst) ### almost as expected for right side 

x3 = []
y3 = []
z3 = []
index3=[]

with open('9_11_10_01_21_cm.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x3.append(round(float(row[0]),0)/1000)
        y3.append(round(float(row[1]),0)/1000)
        z3.append(round(-float(row[2]),0)/1000)
        index2.append(i)
        
#a = (x3[462], y3[462], z3[462])
a3 = (x3[413], y3[413], z3[413])
b3 = (x3[795], y3[795], z3[795])
dst = distance.euclidean(a3, b3)
#min_i = 0
#for i in range(len(x3)):
#    a_test = (x3[i], y3[i], z3[i])
#    dst2 = distance.euclidean(a_test, b3)
#    if dst2==dst:
#        dst = dst2
#        print(i, dst)
#        min_i = i
        
#dst = distance.euclidean(a3, b3)
#print('i', min_i)
print('middle motor',dst) ### almost as expected for right side 
print('middle motor error',0.0625-dst)


###distance from side motor to side motor
dst = distance.euclidean(a1, a2)
dstxy = distance.euclidean((a1[0],a1[1]), (a2[0],a2[1]))
dstxyz = distance.euclidean((a1[0],a1[1],a1[2]), (a2[0],a2[1],a2[2]))
dstz = distance.euclidean(a1[2], a2[2])
print("a1",a1,"a2",a2)
print("as",dstxyz)
print("dstxy",dstxy)
print("dstz",dstz)

###distance from side motor to side motor
dst = distance.euclidean(b1, b2)
print("b1",b1,"b2",b2)

print("bs",dst)

###distance from side motor to side motor
dst = distance.euclidean(a1, b3)
print(dst)

dst = distance.euclidean(a2, a3)
print(dst)

x4 = []
y4 = []
z4 = []
index4=[]

with open('9_11_10_04_00_points.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for i,row in enumerate(plots):
        x4.append(round(float(row[0]),0)/1000)
        y4.append(round(float(row[1]),0)/1000)
        z4.append(round(-float(row[2]),0)/1000)
        index4.append(i)
        
p1 = (x4[4], y4[4], z4[4])
p2 = (x4[506], y4[506], z4[506]) 
p3  = (x4[880], y4[880], z4[880]) 
print(p1,"p1") 

p12 = distance.euclidean(p1, p2)
print("p12",p12)

p23 = distance.euclidean(p2, p3)
print("p23",p23)

#Points in real life
M1=a2
M2=b2
M3=a1
M4=b1
P2=p1
P3=p3
P4=p2
print("LALALALALA")
print("points for transform")
print(M1,M2,M4,P3)
print("single point")
print(P2,P4)

needle=(0.061, 0.006, 0.265)

###X distance
Nx = distance.euclidean(M1[0], needle[0])
Ny= distance.euclidean(M1[1], needle[1])
Nz= distance.euclidean(M1[2], needle[2])

print(Nx,Ny,Nz)

n1=(0.015 ,0.099 ,0.265)
n2=(0.07089979, -0.06420628,  0.26607723)
n12 = distance.euclidean(M1, n1)
print("needle1",n12)
n22 = distance.euclidean(M1, n2)
print("needle2",n22)