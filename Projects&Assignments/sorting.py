import matplotlib.pyplot as plt
import numpy as np
import time as t
def insection_sort(list):
    """
    :param list: containing numbers
    :return: sorted list
    """
    for i in range(1,len(list)):
        temp=list[i]
        k=i
        while k>0 and temp<list[k-1]:
            list[k]=list[k-1]
            k=k-1
        list[k]=temp
    return list

def selection_sort(list):
    """
    :param list: containing numbers
    :return: sorted list
    """
    for i in range(len(list)):
        min = i
        for j in range(i+1,len(list)):
            if list[j]<list[min]:
                min=j
        temp=list[i]
        list[i]=list[min]
        list[min]=temp
    return list

def bubble_sort(list):
    """
    :param list: containing numbers
    :return: sorted list
    """
    for i in range(len(list)-1):
        for j in range(len(list)-1):
            if list[j]>list[j+1]:
                temp=list[j]
                list[j]=list[j+1]
                list[j+1]=temp
    return list

def merge(l1,l2):
    """
    :param l1: a sorted list
    :param l2: a sorted list
    :return: a sorted list containing all objects in l1 and l2
    """
    result=[]
    i=0
    j=0
    while i<len(l1) and j<len(l2):
        if l1[i]<l2[j]:
            result=result+[l1[i]]
            i=i+1
        else:
            result=result+[l2[j]]
            j=j+1
    if i>=len(l1):
        result=result+l2[j:]
    if j>=len(l2):
        result=result+l1[i:]
    return result

def merge_sort(list):
    """
    :param list: a list
    :return: a sorted list
    """
    if len(list)<=1:
        return list
    mid=len(list)//2
    l1=merge_sort(list[:mid])
    l2=merge_sort(list[mid:])
    return merge(l1,l2)

def cal_time(function,length):
    """
    :param function: a sorting function
    :param length: the length of the list input into the function
    :return: the time used to sort it
    """
    a=np.random.rand(length)
    start=t.clock()
    function(a)
    return (t.clock()-start)

fig = plt.figure()
fig.suptitle('Plot of running time for different sorting algorithm')
x=[1000,2000,3000,4000,5000]
y1=[]
y2=[]
y3=[]
y4=[]
for i in x:
    y1.append(cal_time(insection_sort,i))
    y2.append(cal_time(selection_sort,i))
    y3.append(cal_time(bubble_sort,i))
    y4.append(cal_time(merge_sort,i))
l1,=plt.plot(x,y1,color="red",label="insection")
l2,=plt.plot(x,y2,color="green",label="selection")
l3,=plt.plot(x,y3,color="blue",label="bubble")
l4,=plt.plot(x,y4,label="merge")
plt.xlabel("length of step list")
plt.ylabel("time taken(s)")
plt.legend(handles=[l1,l2,l3,l4],labels=["insection","selection","bubble","merge"])
plt.show()



