class Node:
    def __init__(self,initdata):
        self.data=initdata
        self.next=None
    def getData(self):
        return self.data
    def getNext(self):
        return self.next
    def setData(self,new):
        self.data=new
    def setNext(self,newnext):
        self.next=newnext

class LinkedList:
    def __init__(self):
        self.head=None
    def IsEmpty(self):
        return self.head==None
    def add(self,item):
        temp=Node(item)
        temp.setNext(self.head)
        self.head=temp
    def size(self):
        num=0
        a=self.head
        while not a==None:
            num+=1
            a=a.getNext()
        return num
    def search(self,item):
        a=self.head
        found=False
        while a != None and found==False:
            if item==a.getData():
                found=True
            a=a.getNext()
        return found
    def remove(self,item):
        previous=None
        current=self.head
        found=False
        while not found and current!=None:
            if current.getData() == item:
                found=True
            else:
                previous=current
                current=current.getNext()
        if previous != None:
            previous.setNext(current.getNext())
        else:
            self.head=current.getNext()
    def append(self,item):
        a=self.head
        b=self.head
        while a != None:
            b=a
            a=a.getNext()
        b.setNext(Node(item))
    def index(self,item):
        a=self.head
        found=False
        num=0
        while a != None and found==False:
            if item==a.getData():
                found=True
            a=a.getNext()
            num+=1
        return num-1

    def insert(self,item,pos):
        a=self.head
        b=None
        item=Node(item)
        for i in range(pos-1):
            a=a.getNext()
            b=a
        if b != None:
            b.setNext(item)
            (b.getNext()).setNext(a)
        else:
            k=a.getNext()
            a.setNext(item)
            item.setNext(k)
mylist = LinkedList()

mylist.add(31)
mylist.add(77)
mylist.add(17)
mylist.add(93)
mylist.add(26)
mylist.add(54)

print(mylist.size())
print(mylist.search(93))
print(mylist.search(100))

mylist.add(100)
print(mylist.search(100))
print(mylist.size())

mylist.remove(54)
print(mylist.size())
mylist.remove(93)
print(mylist.size())

print(mylist.size())
mylist.insert(93,1)
print(mylist.search(93))
print(mylist.index(93))



