# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 11:06:56 2019

@author: Administrator
"""
#读入数据
from sklearn import datasets  
iris = datasets.load_iris()  # 创建iris的数据，把属性存在X，类别标签存在y
iris_X = iris.data
iris_y = iris.target


# 把所有的data分成了要用来学习的data和用来测试的data   X_test和y_test测试的比例占了总数据的30%
from sklearn.model_selection import train_test_split #
X_train,X_test,y_train,y_test = train_test_split(iris_X,iris_y,test_size = 0.3)


#训练模型
from sklearn.neighbors import KNeighborsClassifier 
knn = KNeighborsClassifier(n_neighbors=5) #定义用sklearn中的KNN分类算法 
knn.fit(X_train,y_train)    # 用KNN进行数据集的学习，把创建的data放进去，他就自动帮你完成train的步骤


# 用训练好的模型进行分类
print(knn.predict(X_test))   #这里的knn就是已经train好了的knn
print(y_test)    # 对比真实值
print(knn.score(X_test,y_test)) #输出模型准确率 