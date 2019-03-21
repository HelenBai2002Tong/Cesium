import pandas
import sys
import random
import math
import operator
import numpy as np
from numpy.random import permutation
from mpl_toolkits.mplot3d import Axes3D


import matplotlib.pyplot as plt


with open("iris.csv", 'r') as csvfile:
    
     iris_dataset = pandas.read_csv(csvfile)



print(iris_dataset.columns.values)

# 打印每一列题头名字
#print(iris_dataset.iloc[:,0:4]) #打印前4列数据所有内容
#print(iris_dataset.iloc[:,4]) #打印第5列数据所有内容


## 对数据进行随机化处理，取30%作为测试集，70%作为训练集

# Randomly shuffle the index of iris_dataset.

random_indices = permutation(iris_dataset.index)


# Set a cutoff for how many items we want in the test set (in this case 30% of the items)
test_ratio=0.3
test_cutoff = math.floor(test_ratio*len(iris_dataset))

# Generate the test set by taking the first 30% of the randomly shuffled indices.
test = iris_dataset.loc[random_indices[0:test_cutoff]]

# Generate the train set with the rest of the data.

train = iris_dataset.loc[random_indices[test_cutoff:]]

print('test sample:', test.shape)
print('train sample:', train.shape)



## 拆分数据与标签
test_labels = np.array(test.iloc[:,4])   #测试集标签，即类别
test_data = np.array(test.iloc[:,0:4])   #测试集数据
train_labels = np.array(train.iloc[:,4]) #训练集标签，即类别
train_data = np.array(train.iloc[:,0:4]) #训练集数据

print('test labels:', test_labels.shape)
print('test data:', test_data.shape)
print('train labels:', train_labels.shape)
print('train data:', train_data.shape)




def kNN(x, data, labels, k):
    num = data.shape[0]
    distance = np.tile(x, (num, 1)) - data #欧氏距离计算开始
    distance = distance ** 2               #每个元素平方
    distance = distance.sum(axis=1)        #矩阵每行相加
    distance = distance ** 0.5             #欧氏距离计算结束
    sortedIndex = distance.argsort()       #返回从小到大排序的索引
    classCount = {}                        #初始化一个空字典
    for i in range (k):                    #统计前k个数据类的数量
        label = labels[sortedIndex[i]]
        classCount[label] = classCount.get(label, 0) + 1 #更新key,value,如果key不在字段中默认value为0
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True) #从大到小按类别数目排序
    print(sortedClassCount)
    return sortedClassCount[0][0]


## 测试
error = 0
for i in range (test_data.shape[0]):
    result = kNN(test_data[i, :], train_data, train_labels, 3)
    print('返回的结果是: %s, 真实结果是: %s' % (result, test_labels[i]))
    if result != test_labels[i]:
        error += 1
print('正确率为: %f%%' % ((1-error / test_data.shape[0] )* 100))


#可视化 画出散点图
xyz = np.array(iris_dataset.iloc[:,[0,1,2]])   #测试集数据
print(xyz.shape)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
type1 = ax.scatter(xyz[0:50, 0], xyz[0:50, 1], xyz[0:50, 2], c='r', marker='^')
type2 = ax.scatter(xyz[50:100, 0], xyz[50:100, 1], xyz[50:100, 2], c='b', marker='o')
type3 = ax.scatter(xyz[100:150, 0], xyz[100:150, 1], xyz[100:150, 2], c='y', marker='*')
ax.legend((type1, type2, type3), ('Iris-setosa', 'Iris-versicolor', 'Iris-virginica'))
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()

sys.exit(0)

