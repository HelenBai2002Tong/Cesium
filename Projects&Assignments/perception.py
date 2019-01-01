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

# randomly generate 50 points
X1, y1 = np.random.uniform(-11,-7,100).reshape((50, 2)), np.zeros(50)
X2, y2 = np.random.uniform(7,11,100).reshape((50, 2)), np.ones(50)

X_train=np.concatenate([X1[0:40],X2[0:40]])
y_train=np.concatenate([y1[0:40],y2[0:40]])
X_test=np.concatenate([X1[40:],X2[40:]])
y_test=np.concatenate([y1[40:],y2[40:]])
p=perceptron(2,f)
p.train(X_train,y_train,100,0.1) # train the perceptron
results=[]
for i in range(20):
    results.append(p.predict(X_test[i])) # to predict the result, the result should be 0 * 10 and 1 * 10
print("result", results)
print("Is the prediction right?", results==y_test)
k1=[]
k2=[]
n1=[]
n2=[]

for i in range(50):
    k1=k1+[X1[i][0]]
    k2=k2+[X1[i][1]]
    n1=n1+[X2[i][0]]
    n2=n2+[X2[i][1]]

# draw the resulted graph
plt.scatter(k1,k2,marker="x") # plot the points marked with 0
plt.scatter(n1,n2,marker="+") # plot the points marked with 1
slope=-p.getWeight()[0]/p.getWeight()[1] # calculate the slope of the line
intercept=-p.getBias()/p.getWeight()[1] # calculate the interception with the y-axis
x=np.linspace(-10,10,20)
y=slope*x+intercept # the equation of the graph
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
    k1=[0,1,0]
    k2=[0,0,1]
    n1=1
    n2=1
    plt.scatter(k1, k2, marker="x")  # plot the points marked with 0
    plt.scatter(n1, n2, marker="+")  # plot the points marked with 1
    slope = -a.getWeight()[0] / a.getWeight()[1]  # calculate the slope of the line
    intercept = -a.getBias() / a.getWeight()[1]  # calculate the interception with the y-axis
    x = np.linspace(-1, 2, 5)
    y = slope * x + intercept  # the equation of the graph
    plt.plot(x, y)
    plt.title("and gate")
    plt.show()


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
    def train_or():
        p=perceptron(2,f)
        x,y=getordata()
        p.train(x,y,10,0.1)
        return p
    a=train_or()
    x,y=getordata()
    for i in x:
        print("or gate",i,a.predict(i))
    k1=0
    k2=0
    n1=[1,0,1]
    n2=[1,1,0]
    plt.scatter(k1, k2, marker="x")  # plot the points marked with 0
    plt.scatter(n1, n2, marker="+")  # plot the points marked with 1
    slope = -a.getWeight()[0] / a.getWeight()[1]  # calculate the slope of the line
    intercept = -a.getBias() / a.getWeight()[1]  # calculate the interception with the y-axis
    x = np.linspace(-1, 2, 5)
    y = slope * x + intercept  # the equation of the graph
    plt.plot(x, y)
    plt.title("or gate")
    plt.show()


and_perceptron()
or_perceptron()
