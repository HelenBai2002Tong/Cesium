import matplotlib.pyplot as mtp
import numpy as np
import math

x=[]
y1=[]
y2=[]
y3=[]
y4=[]
for i in range(2,3000):
    x.append(i)
    z=i**0.5
    y1.append(i)
    y2.append(z)
    y3.append(math.log(i,10))
    y4.append(math.log(i,10)*math.log(i,10))

mtp.plot(x,y1,label='Brutal force without improvement')
mtp.plot(x,y2,label="Brutal force with improvement")
mtp.plot(x,y3,label='Fermat Test')
mtp.plot(x,y4,label='Miller Rabin Method')
mtp.xlabel("n")
mtp.ylabel("number of calculation required")
my_x_ticks = np.arange(0, 3000, 300)
my_y_ticks = np.arange(0, 4000, 400)

mtp.xticks(my_x_ticks)
mtp.yticks(my_y_ticks)
mtp.legend()
#mtp.axis([0,90,0,90])
mtp.show()