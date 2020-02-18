import turtle as t
t.speed(10)
def drawH(size,center):
    t.penup()
    t.goto(center)
    t.pendown()
    t.setheading(0)
    t.fd(size/3)
    t.rt(90)
    t.fd(size/2)
    t.rt(180)
    t.fd(size)
    t.penup()
    t.goto(center)
    t.pendown()
    t.lt(90)
    t.fd(size/3)
    t.rt(90)
    t.fd(size/2)
    t.lt(180)
    t.fd(size)
    t.penup()

def endpoints(size,center):
    endpoint1 = (center[0] + size / 3, center[1] + size / 2)
    endpoint2 = (center[0] + size / 3, center[1] - size / 2)
    endpoint3 = (center[0] - size / 3, center[1] + size / 2)
    endpoint4 = (center[0] - size / 3, center[1] - size / 2)
    endpoint = [endpoint1, endpoint2, endpoint3, endpoint4]
    return endpoint

def recur(generation,size,center):
    if generation == 0:
        pass
    else:
        drawH(size, center)
        for i in range(4):
            recur(generation-1,size/2,endpoints(size,center)[i])

recur(3,100,(0,0))
t.mainloop()