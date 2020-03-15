import random
import time as t
from random import randint


def isProbablyPrime(n, k=6):
    if (n < 2):
        return False
    output = True
    for i in range(0, k):
        a = randint(1, n - 1)
        if (pow(a, n - 1, n) != 1):
            return False
    return output

start=t.time()
for i in range(10000000,10010000):
    if isProbablyPrime(i,4):
        pass
end=t.time()-start
print(end)
