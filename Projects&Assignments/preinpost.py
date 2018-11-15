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

print(postfix("10 2 8 * + 3 -"))
