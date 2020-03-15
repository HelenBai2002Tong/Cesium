import matplotlib.pyplot as plt
import numpy as np
import time as t
import random
from random import randint
def power(x, y, p):
    # Initialize result
    res = 1;

    # Update x if it is more than or
    # equal to p
    x = x % p;
    while (y > 0):

        # If y is odd, multiply
        # x with result
        if (y & 1):
            res = (res * x) % p;

            # y must be even now
        y = y >> 1;  # y = y/2
        x = (x * x) % p;

    return res;

# This function is called
# for all k trials. It returns
# false if n is composite and
# returns false if n is
# probably prime. d is an odd
# number such that d*2<sup>r</sup> = n-1
# for some r >= 1
def miillerTest(d, n):
    # Pick a random number in [2..n-2]
    # Corner cases make sure that n > 4
    a = 2 + random.randint(1, n - 4);

    # Compute a^d % n
    x = power(a, d, n);

    if (x == 1 or x == n - 1):
        return True;

        # Keep squaring x while one
    # of the following doesn't
    # happen
    # (i) d does not reach n-1
    # (ii) (x^2) % n is not 1
    # (iii) (x^2) % n is not n-1
    while (d != n - 1):
        x = (x * x) % n;
        d *= 2;

        if (x == 1):
            return False;
        if (x == n - 1):
            return True;

            # Return composite
    return False;

# It returns false if n is
# composite and returns true if n
# is probably prime. k is an
# input parameter that determines
# accuracy level. Higher value of
# k indicates more accuracy.

#Without
def isPrimeO(n):
    # Corner case
    if n <= 1:
        return False

    # Check from 2 to n-1
    for i in range(2, n):
        if n % i == 0:
            return False;

    return True
#With
def isPrimeB(n):
    # Corner cases
    if (n <= 1):
        return False
    # This is checked so that we can skip
    # middle five numbers in below loop
    if (n % 2 == 0):
        return False
 # Check from 2 to n^0.5
    for i in range(2, round(n**0.5)):
        if n % i == 0:
            return False;

    return True
#Fermat
def isProbablyPrime(n, k=3):
    if (n < 2):
        return False
    output = True
    for i in range(0, k):
        a = randint(1, n - 1)
        if (pow(a, n - 1, n) != 1):
            return False
    return output
#Miller
def isPrime(n, k=3):
    # Corner cases
    if (n <= 1 or n == 4):
        return False;
    if (n <= 3):
        return True;

        # Find r such that n =
    # 2^d * r + 1 for some r >= 1
    d = n - 1;
    while (d % 2 == 0):
        d //= 2;

        # Iterate given nber of 'k' times
    for i in range(k):
        if (miillerTest(d, n) == False):

            return False;

    return True;

def cal_time(function,length):
    """
    :param function: a primality test function
    :param length: the length of the list input into the function
    :return: the time used to test it
    """
    start = t.clock()
    for i in range(length):
        function(i)
    return (t.clock()-start)

def illustrate(type):
    '''
    :param type: the type of primality test
    :return: draw a picture of this method for time ve length of list
    '''
    fig = plt.figure()
    fig.suptitle('Plot of running time for different sorting algorithm')
    x=[100000,200000,300000,400000,500000]
    y=[]
    for i in x:
        y.append(cal_time(type,i))
    plt.plot(x,y,color="red",label=str(type))
    plt.xlabel("length of step list")
    plt.ylabel("time taken(s)")
    plt.show()

def illustrateall():
    '''
    :return: a figure shows all method of sortings' time vs length
    '''
    fig = plt.figure()
    fig.suptitle('Plot of running time for different sorting algorithm')
    x = [0,10000, 20000, 30000, 40000, 50000]
    y1 = []
    y2 = []
    y3 = []
    y4 = []
    for i in x:
        y1.append(cal_time(isPrimeO, i))
        y2.append(cal_time(isPrimeB, i))
        y3.append(cal_time(isProbablyPrime, i))
        y4.append(cal_time(isPrime, i))
    l1, = plt.plot(x, y1, color="red", label="Brutal force without improvement")
    l2, = plt.plot(x, y2, color="green", label="Brutal force with improvement")
    l3, = plt.plot(x, y3, color='yellow',label="Fermat Test")
    l4, = plt.plot(x, y4,  color="blue",label="Miller Rabin Method")
    plt.xlabel("n")
    plt.ylabel("time taken(s)")
    my_x_ticks = np.arange(0, 50000, 10000)
    my_y_ticks = np.arange(0, 8, 1)
    plt.xticks(my_x_ticks)
    plt.yticks(my_y_ticks)
    plt.legend()
    plt.show()


illustrateall()
