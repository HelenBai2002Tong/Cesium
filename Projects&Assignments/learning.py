class Tree:
    def __init__(self,cargo,left=None,right=None):
        self.cargo=cargo
        self.left=left
        self.right=right
def pre(k):
    if k is None:
        return
    print(k.cargo,end=" ")
    pre(k.left)
    pre(k.right)

def inp(k):
    if k is None:
        return
    inp(k.left)
    print(k.cargo,end=" ")
    inp(k.right)

def post(k):
    if k is None:
        return
    post(k.left)
    post(k.right)
    print(k.cargo,end=" ")

a1=Tree("76")
a2=Tree("75")
b1=Tree("79",a1,a2)
b2=Tree("72",Tree("70"),Tree("68"))
a=Tree("83",b1,b2)
#post(a)
#print('\n')
#pre(a)
#print('\n')
#inp(a)

LIMIT = 4
VALUES =[20,6,38,50,40]
for COUNTER1 in range(0, LIMIT):
    MINIMUM = COUNTER1
    for COUNTER2 in range(COUNTER1 + 1, LIMIT+1):
        if VALUES[COUNTER2] < VALUES[MINIMUM]:
            MINIMUM = COUNTER2
    if MINIMUM != COUNTER1:
        TEMPORARY = VALUES[MINIMUM]
        VALUES[MINIMUM] = VALUES[COUNTER1]
        VALUES[COUNTER1] = TEMPORARY
#print(VALUES)

Limit=4
flag=True
VALUES =[20,6,38,50,40]
while flag == True:
    flag = False
    counter = 0
    while counter <= (Limit-1):
        if VALUES[counter]>VALUES[counter+1]:
            temp=VALUES[counter]
            VALUES[counter]=VALUES[counter+1]
            VALUES[counter+1]=temp
            flag=True
        counter+=1
#print(VALUES)

customers=[["James","0","0","0","Cardiff","1"],["Jim","0","0","0","Beijing","1"],["Cat","0","0","0","Cardiff","1"]]
total=0
for i in range(len(customers)):
    if customers[i][4]=="Cardiff":
        total+=1
print(total)

def merge(l1,l2,show=False):
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
    if show==True:
        print(result)
    return result

def merge_sort(list,show=False):
    """
    :param list: a list
    :return: a sorted list
    """
    if show == True:
        print("split",list)
    if len(list)<=1:
        return list
    mid=len(list)//2
    l1=merge_sort(list[:mid],show)
    l2=merge_sort(list[mid:],show)
    if show == True:
        print("merge",l1,l2)
    return merge(l1,l2,show)

merge_sort([13,21,43,34,51,14],True)