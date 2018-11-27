def able(a,b,c):
    if a+b>c and a+c>b and b+c>a:
        return True
def check(answer,i,j,k):
    if [i,j,k] in answer or [i,k,j] in answer or [j,i,k] in answer or [j,k,i] in answer or [k,i,j] in answer or [k,j,i] in answer:
        return False
    else:
        return True
n=eval(input("number"))
count=0
answer=[]
for i in range(n):
    for j in range(n):
        for m in range(n):
            if (i+j+m)==n and able(i,j,m) and check(answer,i,j,m):
                count=count+1
                answer.append([i,j,m])

print(count)
