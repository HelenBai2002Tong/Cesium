import matplotlib.pyplot as mtp
import numpy as np
# x=[]
# y=[]
# for i in range(6):
#     x.append(i)
#     z=3*i+5
#     y.append(z)
# mtp.plot(x,y,'bo')
# mtp.xlabel("x")
# mtp.ylabel("y")
# mtp.axis([0,5,0,30])
# mtp.show()
#print(np.linspace(0,5,50))
# mtp.plot([1,1.5,3,4],[4,4,2,2],label='1')
# mtp.plot([1.5,2,3,4],[1,4,3,1],label="2")
# mtp.legend()
# mtp.show()
#
# mtp.scatter([1,1.5,3,4],[4,4,2,2])
# mtp.scatter([1.5,2,3,4],[1,4,3,1])
# mtp.title("Rick's")
# mtp.show()

a=np.arange(0,400,8)
b=np.random.randint(10,300,50)
c=np.random.ranf(50)
d=a*c*2
colors=['deeppink','pink','lightpink','hotpink','plum','thistle']
e=np.random.randint(0,6,50)
mtp.scatter(a,d,c=[colors[i] for i in e],s=b)
mtp.show()

# a=np.random.randint(1,5,10)
# print(a)
# b=np.random.ranf(5)
# print(b)
# c=np.random.randn(10)
# print(c)
# d=c*5+10 # u=10, sd = 5
# print(d)

# a=np.random.random(size=1000)
# #a=a*10
# mtp.hist(a,bins=100)
# mtp.show()
#
#
# mu, sigma = 100, 15
# x = mu + sigma * np.random.randn(100000)
# # the histogram of the data
# mtp.hist(x,bins='auto')
# mtp.grid(True)
# mtp.text(60,2000,r'$\mu=100,\sigma=15$')
# mtp.show()
#
# a=30
# b=30
# c=45
# a=np.radians(a)
# b=np.radians(b)
# c=np.radians(c)
# a=np.sin(a)
# b=np.cos(b)
# c=np.tan(c)
# print(a,b,c)

def f(t):
    return np.sin(2*t)

t1 = np.arange(0.0, 10.0, 0.1)
t2 = np.arange(0.0, 10.0, 0.02)

mtp.figure(1)
mtp.subplot(2,1,1)
mtp.plot(t1, f(t1), 'bo', t2, f(t2), 'k')

mtp.subplot(2,1,2)
mtp.plot(t2, np.cos(2*t2), 'r--')
mtp.axis([0,10,-1,1])
mtp.annotate("local max",xy=(6.28,1),xytext=(4,0.5)
             ,arrowprops=dict(facecolor='black',
                              headwidth=5, width=0.5))
mtp.show()


