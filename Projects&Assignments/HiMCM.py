import numpy as np
import xlrd


def weight(a,n):
    RI_list=[0,0,0.58,0.9,1.12,1.24,1.32,1.41,1.45]
    a = np.mat(a)
    w, v = np.linalg.eig(a)
    q = w.max()
    l = list(w)
    index = l.index(q)
    sum = np.sum(v, axis=0)
    sum = np.array(sum)
    summax = sum[0][index]
    CI=summax-n/(n-1)
    CI=np.round(CI,2)
    RI=RI_list[n-1]
    CR=round(CI/RI,2)
    v = np.array(v)
    v = v[:, index]
    output = v / summax
    output=np.round(output,2)
    return output,CR


