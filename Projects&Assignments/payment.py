def cal_balance_12(b,a,m):
    '''
    :param b: balance
    :param a: annualInterestRate
    :param m: monthlyPaymentRate
    :return:balance remained after 12 months
    '''
    for i in range(12):
        b=(b-b*m)+(b-b*m)*a/12
    return round(b,2)
print(cal_balance_12(42,0.2,0.04))
print(cal_balance_12(484,0.2,0.04))

def cal_lowest(b,a):
    '''

    :param b: balance
    :param a: annualInterestRate
    :return: the lowest payment
    '''
    s=b
    l=10
    while True:
        b=s
        for i in range(12):
            b=b-l+(b-l)*a/12
        if b > 0:
            l+=10
        else:
            return l
print(cal_lowest(3329,0.2))
print(cal_lowest(4773,0.2))

def cal_lowest_bi(b,a):
    '''

    :param b: balance
    :param a: annualInterestRate
    :return: the lowest payment
    '''
    lower=b/12
    m=a/12
    upper=b*((1+m)**12)/12
    guess = round((lower + upper) / 2, 2)
    s=b
    while -10**(-6)>b or b>10**(-6):
        guess = (lower + upper)/ 2
        b=s
        for i in range(12):
            b=(b-guess)+((b-guess)*m)
        if b > 0:
            lower=guess
        else:
            upper=guess

    return round(guess,2)

print(cal_lowest_bi(320000,0.2))
print(cal_lowest_bi(999999,0.18))