import turtle as t
def sum(m,n):
    if m ==n :
        return m
    else:
        return m+sum(m+1,n)

def fact(n):
    if n==0:
        return 1
    else:
        return n*fact(n-1)

def power(base,exp):
    if exp==0:
        return 1
    else:
        return power*(base(base,exp-1))

def fib(n):
    if n ==0 or n ==1:
        return 1
    else:
        return(fib(n-1)+fib(n-2))

def fibs(n):
    if n < 0 :
        return 0
    if n == 0:
        return 1
    else:
        return (fib(n)+fibs(n-1))


def move(l):
    if l > 5:
        if l < 40:
            t.color('palevioletred')
        else:
            t.color('pink')
        t.fd(l)
        t.lt(30)
        move(l-15)
        t.rt(60)
        move(l-15)
        t.penup()
        t.lt(30)
        t.backward(l)
        t.pendown()
t.speed(7)
t.hideturtle()
t.bgcolor("lavenderblush")
t.rt(90)
t.fd(100)
t.rt(180)
move(100)
t.mainloop()