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



def postfix(s):
    stack=Stack()
    s=s.split(' ')
    for i in s:
        if i.isdigit():
            stack.push(i)
        else:
            a=stack.pop()
            b=stack.pop()
            list1=[b,i,a]
            string=''
            for i in list1:
                string=string+str(i)
            result=eval(string)
            stack.push(result)
    return stack.pop()

def intopost(s):
    prec={}
    prec["*"]=2
    prec["/"]=2
    prec['-']=1
    prec["+"]=1
    prec["("]=0
    prec[")"]=0
    oper=Stack()
    s=s.split(" ")
    output=[]
    for i in s:
        if i.isdigit() or i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            output.append(i)
        elif i == "(":
            oper.push(i)
        elif i == ")":
            k=oper.pop()
            while k != "(":
                output.append(k)
                k=oper.pop()
        else:
            while (not oper.IsEmpty()) and (prec[oper.peek()]>=prec[i]):
                output.append(oper.pop())
            oper.push(i)
    while not oper.IsEmpty():
        output.append(oper.pop())
    result=''
    for i in output:
        result+=i
        result+=" "
    return result
print(intopost("( 3 + 4 )  * A"))