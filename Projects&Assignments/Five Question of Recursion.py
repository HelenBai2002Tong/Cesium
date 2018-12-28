import turtle as t
def mysum(m,n):
    '''
    m,n[int]
    m<n
    return: sum from m to n
    '''
    if m ==n :
        return m
    else:
        return m+mysum(m+1,n)

def fact(n):
    '''
    n:int
    out:n!
    '''
    if n==0:
        return 1
    else:
        return n*fact(n-1)

def power(base,exp):
    '''
    :param base: int
    :param exp: int
    :return: base**exp
    '''
    if exp==0:
        return 1
    else:
        return base*(power(base,exp-1))

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

def fib_iter(n):
    a=0
    b=1
    c=1
    l=[1,]
    for i in range(n):
        c=a+b
        a=b
        b=c
        l.append(c)
    return sum(l)

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

help(mysum)