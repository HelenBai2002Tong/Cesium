def Sum_list(L):
    """
    :param L: a list of number
    :return: sum of the numbers
    """
    total=0
    for i in range(len(L)):
        total+=L[i]
        print(i)
    print(total)


def Sum_list_ele(L):
    """
    :param L: a list of number
    :return: sum of the numbers
    """
    total=0
    for i in L:
        total+=i
        print(i)
    print(total)

Sum_list([1,2,3,4])
Sum_list_ele([1,2,3,4])