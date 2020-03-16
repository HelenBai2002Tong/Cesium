COUNT = 0
K = 0
ROWC=[]
VALUES=[]
MAT=[]
COL=[]
for I in range(0,6):
    for J in range(0,6):
        if MAT[I][J]!= 0:
             VALUES[K] = MAT[I][J]
             COL[K] = J
             K = K + 1
    ROWC[I] = K
