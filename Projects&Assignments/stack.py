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

def checkgeneral(symbol):
    s=Stack()
    o = ["(", "[", "{"]
    def match(a,b):
        o=["(","[","{"]
        p=[")","]","}"]
        i=o.index(a)
        j=p.index(b)
        return i == j
    for i in symbol:
        if i in o:
            s.push(i)
        else:
            if s.IsEmpty()==True:
                return False
            else:
                l=s.peek()
                if match(l,i):
                    s.pop()
                else:
                    return False
    if s.IsEmpty():
        return True
    else:
        return False

print(checkgeneral('{{([][])}()}'))
print(checkgeneral('[{()]'))

def dectobi(number):
    s=Stack()
    while number >0:
        s.push(number%2)
        number=number//2
    a=''
    while not s.IsEmpty():
        a=a+str(s.pop())
    a=int(a)
    return a

print(dectobi(117))

def convert(number,n):
    digits="0123456789ABCDEFGHIJK"
    s=Stack()
    while number >0:
        k=digits[number % n]
        s.push(k)
        number=number//n
    a=''
    while not s.IsEmpty():
        a=a+str(s.pop())
    return a

print(convert(2020,16))
