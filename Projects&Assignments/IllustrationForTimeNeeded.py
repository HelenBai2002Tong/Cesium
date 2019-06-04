import matplotlib.pyplot as ply
import numpy as np
import time as t

def crack(CN,BN,PPN1,PPN2):
    PK1=0
    PK2=0
    for i in range(1,CN):
        if (PPN1-0.1) < ((BN)**(i)) % CN < (PPN1+0.1):
            PK1=i
            break
    for i in range(1, CN):
        if (PPN2-0.1) < ((BN)**(i)) % CN < (PPN2+0.1):
            PK2=i
            break
    return PK1,PK2

start=t.clock()
print(crack(10000019,171123,808008,397038))
timeneed=t.clock()-start
print(round(timeneed,4))



