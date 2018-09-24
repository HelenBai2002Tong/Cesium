global a
a=0
def is_palindromes(s):
    '''
    :param s: a string
    :return: whether it is palindromes(ignore non-letter and case)
    '''
    def toChars(s):
        global a
        s=s.lower()
        letters=""
        for c in s:
            a+=1
            if c in "qazxswedcvfrtgbnhyujmkiolp":
                letters=letters+c
        return letters
    def is_pal(s):
        global a
        a=a+1
        print('isPal called with',s)
        if len(s)<=1:
            print(' About to return True from base case')
            return True
        else:
            answer = s[0] == s[-1] and is_pal(s[1:-1])
            print(' About to return', answer, 'for', s)
            return answer
    return(is_pal(toChars(s)),a)


def gcdIter(a, b):
    '''
    a, b: positive integers

    returns: a positive integer, the greatest common divisor of a & b.
    '''
    # Your code here
    s = min(a, b)
    while True:
        if s == 1:
            return s
        else:
            if a%s==0 and b%s==0:
                return s
            else:
                s = s - 1


def isIn(char, aStr):
    '''
    char: a single character
    aStr: an alphabetized string

    returns: True if char is in aStr; False otherwise
    '''
    # Your code here
    if aStr=="":
        return False
    a = int(len(aStr) / 2)
    b = aStr[a]
    if char == b:
        return True
    else:
        if b < char:
            return isIn(char, aStr[a:])
        else:
            return isIn(char, aStr[0:a])
