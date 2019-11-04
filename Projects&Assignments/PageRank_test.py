import xlrd
import copy
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation

def getindex(j,matrix):
    fromindex=[]
    toindex=[]
    for i in range(len(matrix)):
        if matrix[j][i] != 0:
            fromindex.append(i)
    for k in range(len(matrix)):
        if matrix[k][j] != 0:
            toindex.append(k)
    return fromindex,toindex
def self(index,PRlist):
    self=0
    for i in index:
        self=self+(PRlist[i]/len(PRlist))
    return 0.85*self

def getPR(j,index,PR,matrix,const):
    more=0
    for i in index:
        more=more+PR[i]*matrix[j][i]
    newPR=0.85*more+const
    return newPR
def difference(list1,list2):
    sum=0
    for i in range(len(list1)):
        sum=sum+abs(list1[i]-list2[i])
    return sum
def add_arrow(x,y,x1,y1):
    ax.arrow(x,y,x1-x,y1-y, length_includes_head=True,head_width=0.05, head_length=0.1, fc='b', ec='b')
data = xlrd.open_workbook("pagerank.xlsx")
table = data.sheets()[0]
thematrix=[]
head=[]
nrows=table.nrows
for i in range(1,nrows):
    mylist1=table.row_values(i, start_colx=1, end_colx=None)
    thematrix.append(mylist1)

head=table.row_values(0,start_colx=1,end_colx=None)

for i in range(0,nrows-1):
    preindex=getindex(i,thematrix)
    index=preindex[1]
    for j in index:
        thematrix[j][i]=thematrix[j][i]/len(index)

initial=[]
WholePR=[]
for i in range(nrows-1):
    initial.append(1/(nrows-1))
WholePR.append(initial)

wholefromindex=[]
wholetoindex=[]
for i in range(nrows-1):
    k=getindex(i,thematrix)
    wholefromindex.append(k[0])
    wholetoindex.append(k[1])
selfish=[]
for i in range(len(wholetoindex)):
    if len(wholetoindex[i])==0:
        selfish.append(i)
const=0.15/(nrows-1)
PRlist=copy.deepcopy(initial)
for i in range(nrows-1):
    a=getPR(i,wholefromindex[i],PRlist,thematrix,const)
    a=a+self(selfish,initial)
    PRlist[i]=a
WholePR.append(PRlist)
iter=1

while difference(WholePR[-1],WholePR[-2])>0.000001:
    PRlist1=copy.deepcopy(PRlist)
    for i in range(nrows - 1):
        a = getPR(i, wholefromindex[i], PRlist1, thematrix,const)
        a = a + self(selfish,PRlist)
        PRlist1[i] = a
    WholePR.append(PRlist1)
    PRlist=PRlist1
    iter=iter+1
print(iter)

numofiter=len(WholePR)
fig=plt.figure()
ax = fig.gca()
ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
ratio = math.pi/180
x = [math.sin(i*ratio) for i in range(0,360,round(360//(nrows-1)))]
x=x[:-1]
y = [math.cos(i*ratio) for i in range(0,360,round(360//(nrows-1)))]
y=y[:-1]
xt = [1.5*math.sin(i*ratio) for i in range(0,360,round(360//(nrows-1)))]
yt = [1.5*math.cos(i*ratio) for i in range(0,360,round(360//(nrows-1)))]
points = ax.scatter(x,y,c = 'r')
text = [ax.text(xt[i]-0.2,yt[i],head[i]+":"+str(round(WholePR[0][i]*100))+"%", fontsize = 20) for i in range((nrows-1))]
text.append(ax.text(0,0,str(0)))
for i in range((nrows-1)):
    for j in (wholefromindex[i]):
        add_arrow(x[j],y[j],x[i],y[i])
def init():
    points.set_sizes([5000*i for i in WholePR[0]])#,s = ranks[0])
    text[(nrows-1)].set_text('iteration')
def update(a):
    points.set_sizes([5000*i for i in WholePR[a]])#,s = ranks[a])
    for i in range((nrows-1)):
        text[i].set_text(head[i]+",PR:"+str(round(WholePR[a][i]*100))+"%")
    text[(nrows-1)].set_text(str(a+1))

ani = animation.FuncAnimation(fig,update,(len(WholePR)),init_func=init,interval=1000,repeat = 0)
ani.save('PR_animation.gif',writer = "pillow")
for i in WholePR:
    print(i)
plt.show()
