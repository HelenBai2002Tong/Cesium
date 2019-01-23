import numpy as np
# Q12
def MAT(a):
    length=len(a)
    r=0
    for i in range(length):
        for j in range(length):
            if a[i][j]!=0:
                r+=1
    count=0
    k=0
    values=np.zeros(r)
    rowc=np.zeros(6)
    col=np.zeros(r)
    for i in range(length):
        for j in range(length):
            if a[i][j]!=0:
                values[k]=a[i][j]
                col[k]=j
                k=k+1
                count=count+1
        rowc[i]=count
    print("values",values)
    print("rowc",rowc)
    print("col",col)

a=[[7,0,0,0,0,0],[0,0,0,0,0,0],[0,0,-3,0,9,0],[0,0,0,0,0,0],[0,0,-1,0,0,0],[0,-6,0,0,-5,1]]
MAT(a)

#Q10
class Tree():
    def __init__(self,cargo,left=None,right=None):
        self.cargo=cargo
        self.left=left
        self.right=right

class Stack():
    def __init__(self):
        self.stack=[]
    def IsEmpty(self):
        return self.stack==[]
    def push(self,element):
        self.stack=self.stack+[element]
    def peek(self):
        return self.stack[-1]
    def pop(self):
        a=self.stack[-1]
        self.stack=self.stack[0:-1]
        return a
    def __str__(self):
        return str(self.stack)

def inp(k):
    if k is None:
        return
    inp(k.left)
    print(k.cargo,end=" ")
    inp(k.right)

s=Stack()
names=['alpha','mu','gamma','delta','epsilon','zata','lambda','theta']
for i in names:
    s.push(i)
M=s.pop()
Mytree = Tree(M)
while not s.IsEmpty():
    k=Tree(s.pop())
    finish=-1
    T= Mytree
    while finish == -1:
        if k.cargo >= T.cargo:
            if T.right == None:
                T.right = k
                finish=1
            else:
                T = T.right
        else:
            if T.left == None:
                T.left = k
                finish=1
            else:
                T=T.left

inp(Mytree)








