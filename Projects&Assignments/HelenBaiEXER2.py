# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 21:19:02 2018

@author: admin
"""
# 1
a="All work and no play makes Jack a dull boy."
b="All"
c="work"
d="no"
e="play"
f="makes"
g="Jack"
h="a"
i="dull"
j="boy"
k="."
print(b,c,d,e,f,g,h,i,j,k)
# 2
a=6*1-2
b=6*(1-2)
# next line is for print
print("the value changes from",a,"to",b)

# 3
#nothing happened?

# 4
bruce=6
print(bruce+4)

# 5
P=10000
n=12
r=0.08
t=int(input("amount of year(s):"))
A=P*(1+r/n)**(n*t)
print(A)

# 6
#ZeroDivisionError: integer division or modulo by zero

# 7
a=51
b=a%24
c=2+b
if c > 12:
    c=c-12
    print("AM",c)
else:
    print("PM",c)

# 8
a=int(input("what time it is:"))
b=int(input("Time to wait:"))
b=b%12
c=a+b
print(c)
    