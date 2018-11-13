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

def reversing(mystr):
    a=Stack()
    for i in mystr:
        a.push(i)
    res=''
    while not a.IsEmpty():
        res=res+a.pop()
    return res
print(reversing("abcde"))

def checkbracket(symbol):
    a=Stack()
    for i in symbol:
        a.push(i)
    b = 0
    c = 0
    while not a.IsEmpty():
        k=a.pop()
        if k == ")":
            b+=1
        if k == "(":
            c+=1
    if b == c:
        return True
    else:
        return False
print(checkbracket('((()))'))
print(checkbracket('(()'))