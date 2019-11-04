import random as rd
def generateindividual():
    mystring=''
    for i in range(11):
        a=rd.randint(0,127)
        a=bin(a)
        b=a[2:]
        b=b.zfill(7)
        mystring=mystring+b+" "
    return mystring[:-1]

def fitness(a):
    wanted="1011001 1101111 1110101 0100000 1100111 1100101 1110100 0100000 1101001 1110100 0100001"
    wantlist=wanted.split(" ")
    alist=a.split(" ")
    fit=0
    for i in range(11):
        if wantlist[i]==alist[i]:
            fit=fit+1
    return fit

def selection(population,fitlist):
    popwithfit=[]
    for i in range(len(population)):
        popwithfit.append((fitlist[i],population[i]))
    popwithfit.sort()
    sortpop=popwithfit
    weight=[]
    for i in range(len(population)):
        rand=rd.random()
        weight.append(rand)
    weight.sort()
    newpop=[]
    while len(newpop)<(len(population)):
        for i in range(len(population)):
            if weight[i]>rd.random():
                newpop.append(sortpop[i][1])
    return newpop

def crossover(pop,pc):
    pop_len = len(pop)
    for i in range(pop_len - 1):
        if (rd.random() < pc):
            cpoint = rd.randint(0, len(pop[0]))
            temp1 = []
            temp2 = []
            temp1.extend(pop[i][0:cpoint])
            temp1.extend(pop[i + 1][cpoint:len(pop[i])])
            temp2.extend(pop[i + 1][0:cpoint])
            temp2.extend(pop[i][cpoint:len(pop[i])])
            pop[i] = temp1
            pop[i + 1] = temp2
    for i in range(len(pop)):
        pop[i]="".join(pop[i])
    return pop

def mutation(pop, pm):
    px = len(pop)
    for i in range(px):
        if (rd.random() < pm):
            rdlist=[0,1,2,3,4,5,6,8,9,10,11,12,13,14,16,17,18,19,20,21,22,24,25,26,27,28,29,30,32,33,34,35,36,37,38,40,
                    41,42,43,44,45,46,48,49,50,51,52,53,54,56,57,58,59,60,61,62,64,65,66,67,68,69,70,72,73,74,75,76,77,
                    78,80,81,82,83,84,85,86]
            mpoint = rd.sample(rdlist,1)[0]
            if pop[i][mpoint]==0:
                pop[i] = pop[i][0:mpoint] + '1' + pop[i][mpoint + 1:]
            else:
                pop[i]=pop[i][0:mpoint]+"0"+pop[i][mpoint+1:]
    return pop

population=[]
posforcross=0.7
posformut=0.01
for i in range(1000):
    population.append(generateindividual())
fit=[]
for i in range(len(population)):
    fit.append(fitness(population[i]))

def actole(a):
    a=a.split(" ")
    b=[]
    for i in a:
        d=int(i,2)
        b.append(d)
    p=''
    for i in b:
        p+=chr(i)
    return p
num=0
while max(fit)!=11:
    fit = []
    for i in range(len(population)):
        fit.append(fitness(population[i]))
    newpop=selection(population,fit)
    nextgeneration=crossover(newpop,posforcross)
    population=mutation(nextgeneration,posformut)
    k=actole(newpop[-1])
    num=num+1
    print('letter')
    print(k)
    print("iter",num)



