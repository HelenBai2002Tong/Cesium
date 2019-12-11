import random
operators=["+","-","*","/"]
stop="no"
score = 0
while stop !=" ":
    a=random.randint(1,10)
    b=random.randint(1,10)
    c=random.choice(operators)
    check=str(a)+c+str(b)
    k=input("the result of " + check + " is: ")
    if round(eval(k),2) == round(eval(check),2):
        score+=1
    else:
        pass
    stop=input("the score now is " + str(score) + ". If you want to stop, enter space, else, enter other things")


