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
