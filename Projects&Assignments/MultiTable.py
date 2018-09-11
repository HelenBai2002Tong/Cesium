a=int(input("input a number:"))
for i in range(1,a+1):
    for j in range(1,a+1):
        if i >=j:
            print(j,"*",i,"=",i*j,end=' ')
    print("\n")

i = 1

while i < a+1:
    j = 1
    while j < a+1:
        if j<=i:
            print(j,"*",i,"=",i*j,end=" ")
        j += 1
    print("\n")
    i += 1
