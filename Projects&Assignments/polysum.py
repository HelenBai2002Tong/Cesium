import math
def polysum(n,s):
    '''

    :param n: the number of sides of the polygon
    :param s: the length of each side
    :return:  the sum of the area and square of the perimeter of the regular polygon
    '''
    a=0.25*n*s**2/(math.tan(math.pi/n))
    b=(n*s)**2
    return round((a + b), 4)