import turtle
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


turtle.speed(7)
turtle.hideturtle()
turtle.bgcolor("lavenderblush")
def draw_branch(branch_length):
    if branch_length > 5:
        if branch_length < 40:
            turtle.color('palevioletred')
        else:
            turtle.color('pink')
        turtle.forward(branch_length)
        turtle.right(25)
        draw_branch(branch_length-15)
        turtle.left(50)
        draw_branch(branch_length-15)
        if branch_length < 40:
            turtle.color('palevioletred')
        else:
            turtle.color('pink')
        turtle.right(25)
        turtle.backward(branch_length)

turtle.color('palevioletred')
turtle.right(90)
turtle.fd(100)
turtle.left(180)
draw_branch(100)