import xlrd
def getthemin(number,mylist):
    array=mylist[number]
    for i in range(len(array)-1):
        for j in range(len(array)-1):
            if array[j][0]>array[j+1][0]:
                temp=array[j]
                array[j]=array[j+1]
                array[j+1]=temp
    return array
def getremoved(index,mylist,alist):
    index2=index[:]
    mylist2=[]
    for i in mylist:
        mylist2.append(alist[i])
    for i in index2:
         if i[1] in mylist2:
            index.remove(i)
    return index
def getzeroout(mylist):
    mylist1=mylist[:]
    for i in mylist1:
        if i[0]==0:
            mylist.remove(i)
    return mylist

data = xlrd.open_workbook("Dijkstra.xlsx")
table = data.sheets()[0]
thematrix=[]
head=[]
nrows=table.nrows
for i in range(1,nrows):
    mylist1=table.row_values(i, start_colx=1, end_colx=None)
    thematrix.append(mylist1)

head=table.row_values(0,start_colx=1,end_colx=None)
for i in range(len(thematrix)):
    for j in range(len(thematrix)):
        thematrix[i][j]=[thematrix[i][j],head[j]]

numberindex=int(input("pick a number:"))
getto=[]
getto.append(numberindex)
while len(getto)<=len(thematrix):
    a=getthemin(getto[-1],thematrix)
    b=getremoved(a,getto,head)
    c=getzeroout(b)
    try:
        d=c[0]
        e = head.index(d[1])
        getto.append(e)
        print("result")
        print(getto)
    except:
        print(getto)
        print("No result")
        break






