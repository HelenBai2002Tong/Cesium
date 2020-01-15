a=['c','cbe','caf',"caf",'d']
result=[]
while True:
    difference=[]
    notused=[]
    for i in range(len(a)-1):
        thelength=min(len(a[i]),len(a[i+1]))
        for j in range(thelength):
            if a[i][j]!=a[i+1][j]:
                difference.append((a[i][j],a[i+1][j]))
                try:
                    notused.append(a[i][j+1:])
                    notused.append(a[i][:j])
                except:
                    pass
                break
    b=difference+notused

    b.sort()
    result.append(b[0])





print(difference)
print(notused)





