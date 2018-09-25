global k
k=0
def hanoi(n,fr,space,to):
    global k
    if n ==1:
        k+=1
        if k % 1000000==0:
            print(k)
        #print(fr,"--",to)
    else:
        hanoi(n-1,fr,to,space)
        hanoi(1,fr,space,to)
        hanoi(n-1,space,fr,to)
    return k
print(hanoi(64,"B","C","A"))