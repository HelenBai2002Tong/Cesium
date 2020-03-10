def swap(A,B):
    TEMP = A
    A = B
    B = TEMP
    return A,B


def swapRows(MAT, a, b):
    if isinstance(MAT[0], list)!=True:
        temp = MAT[a]
        MAT[a] = MAT[b]
        MAT[b] = temp
    else:
        for i in range(len(MAT[0])):
            temp= MAT[a][i]
            MAT[a][i] = MAT[b][i]
            MAT[b][i] = temp
    return MAT

Players=["A","B","H","P","R","T"]
ROUNDS=[[70,10,23,3],[40,0,50,90],[60,38,42,90],[45,0,0,60],[55,0,15,10],[51,60,20,90]]
TOTALS=[106,180,230,105,80,221]

for i in range(6):
    for j in range(5):
        if TOTALS[j]<TOTALS[j+1]:
            temp=TOTALS[j+1]
            TOTALS[j+1]=TOTALS[j]
            TOTALS[j]=temp
            swapRows(ROUNDS,j,j+1)
            swapRows(Players,j,j+1)
print(Players)
print(ROUNDS)
print(TOTALS)