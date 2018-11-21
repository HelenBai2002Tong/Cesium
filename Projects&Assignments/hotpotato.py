import random as rd
class Queue():
    def __init__(self):
        self.queue=[]
    def IsEmpty(self):
        return self.queue==[]
    def enqueue(self,element):
        self.queue=self.queue+[element]
    def size(self):
        return len(self.queue)
    def dequeue(self):
        a=self.queue[0]
        self.queue=self.queue[1:]
        return a
    def __str__(self):
        return str(self.queue)

def hotpotato(namelist,num):
    q=Queue()
    for i in namelist:
        q.enqueue(i)
    while q.size() > 1:
        for i in range(num):
            k=q.dequeue()
            q.enqueue(k)
        q.dequeue()
    return q.dequeue()


def simulation(time,pagespeed):
    print=Queue()
    def pages():
        return rd.randrange(1,21)
    def newtask():
        n=rd.randrange(1,181)
        return n == 180
    def IsBusy(print):
        return print.size()>1
    wait=0
    for i in range(time):
        if newtask():
            timeneed=pages()/pagespeed
            print.enqueue(timeneed)
        if not IsBusy(print):
            k=print.dequeue()
        if IsBusy(print):
            wait=wait+1


