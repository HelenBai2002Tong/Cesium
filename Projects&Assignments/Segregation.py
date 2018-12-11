import numpy as np
#empty=0,population1=1,population2=2
size=int(input("size:"))
empty=eval(input("empty:"))
population1=int(input("population1:"))
happy=eval(input("satisfaction:"))

def is_happy(i,j,happy,show,size):
    count=0
    same=-1
    if show[i][j]==0:
        pass
    elif (size-1) > i > 0 and (size-1)>j>0:
        for m in range(i-1,i+2):
            for n in range(j-1,j+2):
                if show[m][n]!=0:
                    count=count+1
                if show[m][n]==show[i][j]:
                    same=same+1
    elif i==0 and (size-1)>j>0:
        for m in range(i,i+2):
            for n in range(j-1,j+2):
                if show[m][n]!=0:
                    count=count+1
                if show[m][n]==show[i][j]:
                    same=same+1
    elif i==size-1 and (size-1)>j>0:
        for m in range(i-1,i+1):
            for n in range(j-1,j+2):
                if show[m][n]!=0:
                    count=count+1
                if show[m][n]==show[i][j]:
                    same=same+1
    elif (size-1) > i > 0 and j==0:
        for m in range(i-1,i+2):
            for n in range(j,j+2):
                if show[m][n]!=0:
                    count=count+1
                if show[m][n]==show[i][j]:
                    same=same+1
    elif j==size-1 and (size-1)>i>0:
        for m in range(i-1,i+2):
            for n in range(j-1,j+1):
                if show[m][n]!=0:
                    count=count+1
                if show[m][n]==show[i][j]:
                    same=same+1
    elif i==0 and j==0:
        for m in range(i,i+2):
            for n in range(j,j+2):
                if show[m][n]!=0:
                    count=count+1
                if show[m][n]==show[i][j]:
                    same=same+1
    elif i==size-1 and j==0:
        for m in range(i-1,i+1):
            for n in range(j,j+2):
                if show[m][n]!=0:
                    count=count+1
                if show[m][n]==show[i][j]:
                    same=same+1
    elif i==0 and j==size-1:
        for m in range(i,i+2):
            for n in range(j-1,j+1):
                if show[m][n]!=0:
                    count=count+1
                if show[m][n]==show[i][j]:
                    same=same+1
    elif i==size-1 and j==size-1:
        for m in range(i-1,i+1):
            for n in range(j-1,j+1):
                if show[m][n]!=0:
                    count=count+1
                if show[m][n]==show[i][j]:
                    same=same+1
    if count==0:
        return True
    else:
        return (same/count)>=happy


number=size**2
population2=number-empty-population1
show=[]
for i in range(empty):
    show.append(0)
for i in range(int(population1)):
    show.append(1)
for i in range(int(population2)):
    show.append(2)
np.random.shuffle(show)
show=np.reshape(show,(size,size))
Tell=False
while not Tell:
    count = 0
    for i in range(size):
        for j in range(size):
            if is_happy(i,j,happy,show,size):
                count=count+1
            if not is_happy(i,j,happy,show,size):
                Tell=False
                print("before","\n",show)
                for m in range(size):
                    for n in range(size):
                        if show[m][n]==0:
                            index1=m
                            index2=n
                show[index1][index2]=show[i][j]
                show[i][j]=0
                print(show)
    if count==size**2:
        Tell=True

print(show)
