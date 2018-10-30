from matplotlib import pyplot as plt
import numpy as np

class perceptron(object):
    def __init__(self,nums,activator):
        '''
        :param nums: the parameter in vector
        :param activator: the function used to calculate
        '''
        self.activitor=activator
        self.weight=[0 for i in range(nums)]
        self.bias=0

    def getWeight(self):
        '''
        :return: weight
        '''
        return self.weight

    def getBias(self):
        '''
        :return: bias
        '''
        return self.bias

    def predict(self,vector):
        '''
        :param vector: a single vector
        :return: the value after calculating by perceptron
        '''
        sum=0
        for i in range(len(vector)):
            sum=sum+vector[i]*self.weight[i]
        return self.activitor(sum+self.bias)

    def train(self,vectors,labels,iteration,rate):
        '''
        :param vectors: the vector list
        :param labels: the label list with corresponding to vectors and is the expect value
        :param iteration: the numbers you want to iterate
        :param rate: the learning rate
        :return: perform oneiteration for iteration times
        '''
        for i in range(iteration):
            self.oneiteration(vectors,labels,rate)

    def oneiteration(self,vectors,labels,rate):
        '''
        :param vectors: the vector list
        :param labels: the label list with corresponding to vectors and is the expect value
        :param rate:the learning rate
        :return: update the weight and bias
        '''
        for i in range(len(vectors)):
            y=self.predict(vectors[i])
            self.update(y,vectors[i],labels[i],rate)

    def update(self,y,vector,label,rate):
        '''
        :param y: the value of vector calculate by the perceptron
        :param vector: one vector from vectors
        :param label: the expect value of the vector
        :param rate: the learning rate
        :return: update the weight and bias
        '''
        delta=label-y
        for i in range(len(self.weight)):
            self.weight[i]+=rate*(delta*vector[i])
        self.bias+=delta*rate

def f(x):
    '''
    :param x: a number
    :return: 1 or 0
    '''
    return 1 if x > 0 else 0

X1, y1 = np.random.uniform(-11,-7,200).reshape((100, 2)), np.zeros(100)
X2, y2 = np.random.uniform(7,11,200).reshape((100, 2)), np.ones(100)
X=X1+X2
y=y1+y2
p=perceptron(2,f)
p.train(X,y,100,0.1)
k1=[]
k2=[]
n1=[]
n2=[]

for i in range(100):
    k1=k1+[X1[i][0]]
    k2=k2+[X1[i][1]]
    n1=n1+[X2[i][0]]
    n2=n2+[X2[i][1]]

plt.scatter(k1,k2,marker="x")
plt.scatter(n1,n2,marker="+")
slope=-p.getWeight()[0]/p.getWeight()[1]
intercept=-p.getBias()/p.getWeight()[1]
x=np.linspace(-10,12,100)
y=slope*x+intercept
plt.plot(x,y)
plt.show()

def and_perceptron():
    def f(x):
        '''
        :param x: a number
        :return: 1 or 0
        '''
        return 1 if x > 0 else 0
    def getanddata():
        x=[[1,1],[0,0],[1,0],[0,1]]
        y=[1,0,0,0]
        return x,y
    def train_and():
        p=perceptron(2,f)
        x,y=getanddata()
        p.train(x,y,10,0.1)
        return p
    a=train_and()
    x,y=getanddata()
    for i in x:
        print("and gate",i,a.predict(i))



def or_perceptron():
    def f(x):
        '''
        :param x: a number
        :return: 1 or 0
        '''
        return 1 if x > 0 else 0
    def getordata():
        x=[[1,1],[0,1],[1,0],[0,0]]
        y=[1,1,1,0]
        return x,y
    def train_and():
        p=perceptron(2,f)
        x,y=getordata()
        p.train(x,y,10,0.1)
        return p
    a=train_and()
    x,y=getordata()
    for i in x:
        print("or gate",i,a.predict(i))


and_perceptron()
or_perceptron()