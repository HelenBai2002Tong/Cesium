class magic_array(object):
    def __init__(self):
        pass
    def makeup(self,n):
        temp=[]
        for i in range(n):
            temp.append([])
            for j in range(n):
                temp[i].append(0)
        Z=1
        x = 0
        y = n//2
        while Z <= n*n:
            temp[x][y]=Z
            Z=Z+1
            if x == 0 and y == n-1:
                x= x+1
            else:
                x=x-1
                y=y+1
                if x < 0 :
                    x = n-1
                if y > n-1:
                    y= 0
                if temp[x][y] != 0:
                    x = x + 2
                    y = y - 1
        for i in range(len(temp)):
            print(temp[i])
        return temp
    def check(self,list):
        l=len(list)
        sum1=0
        for i in range(l):
            sum1+=list[0][i]
        check1=0
        check2=0
        check3=0
        check4=0
        for i in range(l):
            for j in range(l):
                check1 = check1 + list[i][j]
                check2=check2+list[j][i]
                if i == j:
                    check3 = check3 + list[i][j]
                if i + j == l - 1:
                    check4 = check4 + list[i][j]
            if check2==check1==sum1:
                check1=0
                check2=0
            else:
                return False
        if check3==check4==sum1:
            return True
        else:
            return False

a=magic_array()
b=a.makeup(5)
print(a.check(b))
