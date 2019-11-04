import pandas as pd
import matplotlib.pyplot as plt
import math
import matplotlib.animation as animation
def precentage(a):#算比例
    a = a*1000
    a = int(a)/10
    return str(a)+"%"
def  uniformization(a):#归一化
    s = sum(a)
    for i in range(node_num):
        a[i] = a[i]/s
    return a
def add_arrow(x,y,x1,y1):#增加ARROW
    ax.arrow(x,y,x1-x,y1-y, length_includes_head=True,head_width=0.05, head_length=0.1, fc='b', ec='b')
ipt = pd.read_csv(r"Matrix.csv") #读入 图（graph）信息
head = ipt.columns
node_num = 5# 节点数目
rank1 = [1 for i in range(node_num)]
rank0 = [0 for i in range(node_num)]
ranks = [[1/node_num for i in range(node_num)]]
linkto = [[] for i in range(node_num)]#二维数组 [[],[],...,[]]记录链接到这个点的点的index
linkfrom = [0 for i in range(node_num)]
for i in range(node_num):#将二维表格信息导入程序
    for j in range(node_num):
        if((ipt[head[i+1]][j])==1 and i!=j):#总结CSV
            linkto[j].append(i)#到j的链接的出发节点号
            linkfrom[i] +=1#从j出发的连接数量
    if linkfrom[j] == 0:
        linkfrom[j] = node_num
while(sum([abs(rank1[i]-rank0[i]) for i in range(node_num)])>0.0001):#rank0 上一次的rank1本次的rank
    rank0 = [rank1[i] for i in range(node_num)]
    for i in range(node_num):
        rank1[i] = 0.15/node_num
        for j in linkto[i]:
            rank1[i] += 0.85*rank0[j]/linkfrom[j]
    temp = uniformization(rank1)
    ranks.append([i for i in temp])#每一轮迭代的rank保存下来，用于绘图，由于python的挂钩储存方式必须这样写

#动画部分
fig = plt.figure()
ax = fig.gca()
ax.set_xlim(-2,2)
ax.set_ylim(-2,2)
ratio = math.pi/180
x = [math.sin(i*ratio) for i in range(0,360,360//node_num)]
y = [math.cos(i*ratio) for i in range(0,360,360//node_num)]
xt = [1.5*math.sin(i*ratio) for i in range(0,360,360//node_num)]
yt = [1.5*math.cos(i*ratio) for i in range(0,360,360//node_num)]
points = ax.scatter(x,y,c = 'r')
text = [ax.text(xt[i]-0.2,yt[i],head[i+1]+":"+str(precentage(ranks[0][i])), fontsize = 20) for i in range(node_num)]
text.append(ax.text(0,0,str(0)))
for i in range(node_num):
    for j in (linkto[i]):
        add_arrow(x[j],y[j],x[i],y[i])#添加路径
def init():
    points.set_sizes([10000*i for i in ranks[0]])#,s = ranks[0])
    text[node_num].set_text('iteration')
def update(a):
    points.set_sizes([10000*i for i in ranks[a]])#,s = ranks[a])
    for i in range(node_num):
        text[i].set_text(head[i+1]+",PR:"+str(precentage(ranks[a][i])))
    text[node_num].set_text(str(a+1))
ani = animation.FuncAnimation(fig,update,range(len(ranks)),init_func=init,interval=1000,repeat = 0)
ani.save('PR_animation.gif',writer = "pillow")
plt.show()
