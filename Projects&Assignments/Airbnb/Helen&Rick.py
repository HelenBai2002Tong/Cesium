import pandas
import sys
import random
import math
import operator
import numpy as np
from numpy.random import permutation
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

with open("dc_airbnb.csv", 'r') as csvfile:
    room_data = pandas.read_csv(csvfile)
#print(room_data.columns.values)


random_indices = permutation(room_data.index)
test_ratio=0.3
test_cutoff = math.floor(test_ratio*len(room_data))
test = room_data.loc[random_indices[0:test_cutoff]]
train = room_data.loc[random_indices[test_cutoff:]]

test_labels = np.array(test.iloc[: ,8])
test_data = np.array(test.iloc[:,3:7])
train_labels = np.array(train.iloc[:,8])
train_data = np.array(train.iloc[:,3:7])

for i in range(len(test_data)):
    if test_data[i][1]=='Entire home/apt':
        test_data[i][1]=10
    if test_data[i][1]=="Private room":
        test_data[i][1]=3
    if test_data[i][1]=="Shared room":
        test_data[i][1]=1

for i in range(len(train_data)):
    if train_data[i][1]=='Entire home/apt':
        train_data[i][1]=10
    if train_data[i][1]=="Private room":
        train_data[i][1]=3
    if train_data[i][1]=="Shared room":
        train_data[i][1]=1


for i in range(len(test_data)):
    for j in range(4):
        test_data[i][j]=float(test_data[i][j])


for i in range(len(train_data)):
    for j in range(4):
        train_data[i][j]=float(train_data[i][j])

def kNN(x,data, labels, k):
    num = data.shape[0]
    distance = np.tile(x, (num, 1)) - data
    distance = distance ** 2
    distance = distance.sum(axis=1)
    distance = distance ** 0.5
    sortedIndex = distance.argsort()
    classCount = {}
    for i in range (k):
        label = labels[sortedIndex[i]]
        classCount[label] = classCount.get(label, 0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    #print(sortedClassCount)
    return sortedClassCount[0][0]

def correct_rate(a,b):
    rate=1-(abs(a-b)/b)
    return rate
x_axis=[]
y_axis=[]
for j in range(3,2000,20):
    myc = []
    x_axis.append(j)
    for i in range (test_data.shape[0]):
        result = kNN(test_data[i, :], train_data, train_labels, j)
        #print('返回的结果是: %s, 真实结果是: %s' % (result, test_labels[i]))
        myc.append(correct_rate(result,test_labels[i]))
    sum1=sum(myc)
    rate=sum1/(test_data.shape[0])
    y_axis.append(rate)

plt.scatter(x_axis,y_axis)
plt.show()