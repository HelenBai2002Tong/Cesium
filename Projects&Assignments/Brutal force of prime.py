# A school method based Python3
# program to check if a number
# is prime
import time as t
def isPrime(n):
    # Corner case
    if n <= 1:
        return False

    # Check from 2 to n-1
    for i in range(2, n):
        if n % i == 0:
            return False;

    return True
start=t.time()
for i in range(10000000, 10001000):
    if isPrime(i):
        print(i)

end=t.time()-start
print(end)
