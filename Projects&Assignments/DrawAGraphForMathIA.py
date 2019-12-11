import matplotlib.pyplot as mtp
import numpy as np
import math

x=[]
y1=[]
y2=[]
y3=[]
y4=[]
for i in range(2,30):
    x.append(i)
    z=i**0.5
    y1.append(i)
    y2.append(z)
    y3.append(math.log10(i))
    y4.append(math.log10(i)*math.log10(i))

mtp.plot(x,y1,label='Brutal force without improvement')
mtp.plot(x,y2,label="Brutal force with improvement")
mtp.plot(x,y3,label='Fermat Test')
mtp.plot(x,y4,label='Miller Rabin Method')
mtp.xlabel("n")
mtp.ylabel("time required")
mtp.xticks([])
mtp.yticks([])
mtp.legend()
#mtp.axis([0,90,0,90])
mtp.show()