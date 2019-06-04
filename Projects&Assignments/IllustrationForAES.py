import time as t
PrivateKey1=eval(input("Choose one:"))
PrivateKey2=eval(input("Choose another:"))
ClockNumber=eval(input("The size of the clock:"))
BaseNumber=eval(input("Base:"))

def getPPN(P1,P2,CN,BN):
    PPN1=((BN)**(P1))%CN
    PPN2=((BN)**(P2))%CN
    return PPN1,PPN2

def getShared(PPN,PK,CN):
    Remain=PPN%CN
    i=1
    while i < PK:
        Remain=(PPN*Remain)%CN
        i+=1
    return Remain
start=t.clock()
PPN1,PPN2=getPPN(PrivateKey1,PrivateKey2,ClockNumber,BaseNumber)
timeneed=t.clock()-start
print("PPN1,PPN2:",PPN1,PPN2)
print("timeneed:",round(timeneed,4))
print(getShared(PPN1,PrivateKey2,ClockNumber))
print(getShared(PPN2,PrivateKey1,ClockNumber))

