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
        return None
    inp(k.left)
    print(k.cargo,end=" ")
    inp(k.right)

def post(k):
    if k is None:
        return
    post(k.left)
    post(k.right)
    print(k.cargo,end=" ")
a1=Tree("a1")
a2=Tree("a2")
b1=Tree("b1")
b2=Tree("b2")
a=Tree("a",a1,a2)
b=Tree("b",b1,b2)

tree1=Tree("c",a,b)
tree = Tree("+", Tree(1), Tree("*", Tree(2), Tree(3)))
print("pre")
pre(tree)
print("\nin")
inp(tree)
print("\npost")
post(tree)
