import numpy as np
import random as rd


def gennewreq(therange):
    k = rd.randint(1, 100)
    if k <= 30:
        n = 0
    elif k <= 85:
        n = 1
    elif k <= 97:
        n = 2
    else:
        n = 3
    require = []
    while n > 0:
        start = rd.randint(1, therange)
        direction = rd.choice([-1, 1])  # -1 down, 1 up
        if (direction == -1 and start != 1) or (start == therange):
            end = rd.randint(1, (start - 1))
            direction = -1
        else:
            end = rd.randint((start + 1), therange)
            direction = 1
        require.append([start, end, direction])
        n = n - 1
    return require


indexarray = []

rangeforloop = eval(input("the times to generate new requisition: "))
rangeforelevator = eval(input("the range for the elevator(the highest number): "))

start = rd.randint(1, rangeforelevator)
direction = rd.choice([-1, 1])  # -1 down, 1 up
if (direction == -1 and start != 1) or (start == rangeforelevator):
    end = rd.randint(1, (start - 1))
    direction = -1
else:
    end = rd.randint((start + 1), rangeforelevator)
    direction = 1
indexarray.append([start, end, direction])
while indexarray != []:
    newreq = gennewreq(rangeforelevator)
    indexarray = indexarray + newreq


