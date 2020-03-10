def Domain(R):
    #Takes a relation as a set of pairs and returns the domain
    #Domain({(1,2),(2,3)})={1,2}
    answer=set()
    for p in R:
        answer.add(p[0])
    return answer

def Range(R):
    #Take a relation as a set of pairs and returns the range
    #Range({(1,2),(2,3)})={2,3}
    answer=set()
    for p in R:
        answer.add(p[1])
    return answer

def Reflexive(A,R):
    #Take a relation R as a set of pairs and returns the boolean answer to the question is R is reflexive
    #Reflexive({1,2,3},{(1,2),(2,3),(1,1),(2,2)})=False
    for a in A:
        if not ((a,a) in R):
                answer = False
    return answer

def RcircR(R):
    #Take a relation R as a set of pairs and returns R compose R
    #RcircR({(1,2),(2,3),(2,1)})={(1, 3), (1, 1), (2, 2)}
    answer=set()
    for p in R:
        for q in R:
            if p[1]==q[0]:
                answer.add((p[0],q[1]))
    return answer

def Rinverse(R):
    #Takes a relation R as a set of pairs and returns the inverse relation
    #Rinverse({(1,2),(2,3),(2,1)})={(1, 2), (3, 2), (2, 1)}
    answer=set()
    for p in R:
        answer.add((p[1],p[0]))
    return answer

def Symmetric(R):
    #Takes a relation R as a set of pairs and returns the boolean answer to the question is R is symmetric
    #Symmetric({(1,2),(2,1)})=True
    return R==Rinverse(R)

def Transitive(R):
    #Takes a relation R as a set of pairs and returns the boolean answer to the question is R is transitive
    #Transitive({(1,2),(2,1),(1,1)})
    return RcircR(R) <= R

def RcircS(R,S):
    #Takes a relation R and S as a sets of pairs and returns R compose S
    #RcircS({(1,2),(2,3),(3,1)},{(2,4),(2,1),(3,2)})={(1, 1), (1, 4), (2, 2)}
    answer=set()
    for p in R:
        for q in S:
            if p[1]==q[0]:
                answer.add((p[0],q[1]))
    return answer

def Function(R):
    #Takes a relation R as a set of pairs and returns the boolean answer to the question is R a function
    #Function({(1,2),(2,3),(1,1)})=False
    for p in R:
        for q in R:
            if (p[0]==q[0]) and (p[1]!=q[1]):
                return False
    return True

