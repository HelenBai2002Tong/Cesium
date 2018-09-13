num=27
x=abs(num)
a=0
b=max(1,x)
guess=0.5*(a+b)
e=0.01
while abs(guess**3-x) >e:
    if guess**3>x:
        b=guess
        guess=0.5*(a+b)
    if guess**3<x:
        a=guess
        guess=0.5*(a+b)
if num<0:
    guess=-guess
print(guess,"is the answer")

