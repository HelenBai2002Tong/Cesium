import turtle as t
import random as rd
t.hideturtle()
t.screensize(400,300,"steelblue")
t.speed(0)
t.tracer(10)


def curvemove(a,b,c,d):
    t.left(a)
    for i in range(b):
        t.left(c)
        t.forward(d)


def curvemove2(a,b,c,d,e,f):
    t.left(a)
    for i in range(b):
        x = rd.randint(1, 3)
        t.pensize(x)
        temp = [e,f]
        y = rd.choice(seq=temp)
        t.color(y, y)
        t.left(c)
        t.forward(d)
        t.left(90)
        t.fd(0.5)
        t.fd(-0.5)
        t.left(270)

t.color("cornflowerblue","cornflowerblue")
t.begin_fill()
t.pendown()
t.goto(-400,-600)
t.goto(400,-600)
t.goto(400,0)
t.goto(-400,0)
t.goto(-400,-600)
t.end_fill()

t.penup()
t.home()
t.left(180)
t.fd(300)
t.right(180)
t.pendown()
t.color("white","white")

t.begin_fill()

curvemove(14,600,0.08,0.6)
curvemove(-55,100,-0.05,0.01)
curvemove(0,250,-0.06,0.1)
curvemove(0,550,0.08,0.15)

curvemove(-60,200,-0.13,0.01)
curvemove(-20,950,0.045,0.3)

t.goto(-300,0)
t.end_fill()

t.color("midnightblue","midnightblue")
t.begin_fill()
t.setheading(0)
curvemove(14,500,0.08,0.6)
t.setheading(0)
curvemove(-75,500,0.02,0.03)
curvemove(55,100,0.05,0.01)
curvemove(40,1000,-0.005,0.03)
curvemove(-55,100,-0.05,0.01)

curvemove(-50,1200,0.01,0.035)
curvemove(80,100,0.01,0.01)
curvemove(65,2000,-0.01,0.03)

curvemove(-75,100,-0.05,0.01)
curvemove(-50,100,0.01,0.035)
curvemove(-10,750,0.005,0.053)

curvemove(5,1200,0.1,0.01)
curvemove(-130,750,0.015,0.05)

curvemove(10,2000,0.05,0.002)
curvemove(35,1300,0.007,0.04)

curvemove(-40,1000,-0.1,0.001)
curvemove(-30,600,0.03,0.05)

curvemove(0,700,0.2,0.001)
curvemove(0,1500,0.0015,0.04)

curvemove(-55,1000,-0.05,0.01)
curvemove(0,145,0.08,0.1)

t.goto(101.50,169.28)
t.setheading(293.775)
curvemove(0,755,0.045,0.3)

t.goto(-300,0)
t.end_fill()

t.penup()
t.home()
t.rt(90)
t.left(270)
t.fd(300)
t.right(180)
t.pendown()
t.color("aliceblue","aliceblue")
t.begin_fill()

curvemove(-14,600,-0.08,0.6)
curvemove(55,100,0.05,0.01)
curvemove(0,250,0.06,0.1)
curvemove(0,550,-0.08,0.15)

curvemove(60,200,0.13,0.01)
curvemove(20,950,-0.045,0.3)

t.goto(-300,0)
t.end_fill()

t.color("darkblue","darkblue")
t.begin_fill()
t.setheading(0)
curvemove(-14,500,-0.08,0.6)
t.setheading(0)
curvemove(75,500,-0.02,0.03)
curvemove(-55,100,-0.05,0.01)
curvemove(-40,1000,0.005,0.03)
curvemove(55,100,0.05,0.01)

curvemove(50,1200,-0.01,0.035)
curvemove(-80,100,-0.01,0.01)
curvemove(-65,2000,0.01,0.03)

curvemove(75,100,0.05,0.01)
curvemove(50,100,-0.01,0.035)
curvemove(10,750,-0.005,0.053)

curvemove(-5,1200,-0.1,0.01)
curvemove(130,750,-0.015,0.05)

curvemove(-10,2000,-0.05,0.002)
curvemove(-35,1300,-0.007,0.04)

curvemove(40,1000,0.1,0.001)
curvemove(30,600,-0.03,0.05)

curvemove(0,700,-0.2,0.001)
curvemove(0,1500,-0.0015,0.04)

curvemove(55,1000,0.05,0.01)
curvemove(0,145,-0.08,0.1)

t.goto(101.50,-169.28)
t.setheading(-293.775)
curvemove(0,755,-0.045,0.3)
t.goto(-300,0)
t.end_fill()

for i in range(500):
    t.penup()
    a=rd.randint(3,5)
    t.pensize(a)
    temp=["midnightblue","darkblue"]
    b=rd.choice(seq=temp)
    t.color(b,b)
    c=rd.randrange(-290,240)
    d=rd.randrange(-2,2)
    t.goto(c,d)
    t.pendown()
    t.fd(1)
t.penup()
t.goto(-300,0)
t.setheading(-0)
t.pendown()
curvemove2(-14,500,-0.08,0.6,"cornflowerblue", "darkblue")
curvemove2(0,100,-0.08,0.6,"cornflowerblue","aliceblue")
curvemove2(55,100,0.05,0.01,"cornflowerblue","aliceblue")
curvemove2(0,250,0.06,0.1,"cornflowerblue","aliceblue")
curvemove2(0,55,-0.8,1.5,"cornflowerblue","aliceblue")
curvemove2(60,200,0.13,0.01,"cornflowerblue","aliceblue")
curvemove2(20,100,-0.09,0.6,"cornflowerblue","aliceblue")
curvemove2(0,760,-0.045,0.3,"cornflowerblue", "darkblue")
t.penup()
t.goto(-56.52,-164.54)
t.setheading(0)
t.pendown()

curvemove2(75,50,-0.2,0.3,"aliceblue","darkblue")
curvemove2(-55,100,-0.05,0.01,"aliceblue","darkblue")
curvemove2(-40,100,0.05,0.3,"aliceblue","darkblue")
curvemove2(55,100,0.05,0.01,"aliceblue","darkblue")
# I am easy to be satisfied
curvemove2(50,120,-0.1,0.35,"aliceblue","darkblue")
curvemove2(-80,100,-0.01,0.01,"aliceblue","darkblue")
curvemove2(-65,200,0.1,0.3,"aliceblue","darkblue")
# to meet you is enough
curvemove2(75,100,0.05,0.01,"aliceblue","darkblue")
curvemove2(50,100,-0.01,0.035,"aliceblue","darkblue")
curvemove2(10,75,-0.05,0.53,"aliceblue","darkblue")
curvemove2(-5,120,-1,0.1,"aliceblue","darkblue")
curvemove2(130,75,-0.15,0.5,"aliceblue","darkblue")
curvemove2(-10,200,-0.5,0.02,"aliceblue","darkblue")
curvemove2(-35,130,-0.07,0.4,"aliceblue","darkblue")

curvemove2(40,100,1,0.01,"aliceblue","darkblue")
curvemove2(30,60,-0.3,0.5,"aliceblue","darkblue")

curvemove2(0,70,-2,0.01,"aliceblue","darkblue")
curvemove2(0,150,-0.015,0.4,"aliceblue","darkblue")

curvemove2(55,100,0.5,0.1,"aliceblue","darkblue")
curvemove2(0,145,-0.08,0.1,"aliceblue","darkblue")

t.color("snow","snow")
for i in range(300):
    t.penup()
    a=rd.randint(5,10)
    t.pensize(a)
    b=rd.randrange(-400,400)
    c=rd.randrange(-300,300)
    t.goto(b,c)
    t.pendown()
    t.fd(1)
t.update()
t.mainloop()
# :)
