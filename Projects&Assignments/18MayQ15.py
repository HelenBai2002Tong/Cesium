def SalesCalculate(ARRAY, A, B, X, Y,FEES):
    #A,B are row & column of first day,
    #X,Y are row & column of last day.
    TOTAL = 0
    for COL in range(B,7):
        if COL < 5:
            TOTAL = TOTAL + ARRAY[A][COL] * FEES[0]
        else:
            TOTAL = TOTAL + ARRAY[A][COL] * FEES[1]
    #calculates total for week A,
    #days are in the range from B to 6
    #weekdays are days 0-4, and weekend 5,6
    for ROW in range(A + 1, X):
        for COL in range(0,7):
            if COL < 5:
                TOTAL = TOTAL + ARRAY[ROW][COL]*FEES[0]
            else:
                TOTAL = TOTAL + ARRAY[ROW][COL]*FEES[1]
    #calculates total for all weeks from A+1 to X-1,
    #days are in the range from 0 to 6
    for COL in range(0,Y+1):
        if COL < 5:
            TOTAL = TOTAL + ARRAY[X][COL]*FEES[0]
        else:
            TOTAL = TOTAL + ARRAY[X][COL]*FEES[1]

    #calculates total for week X,
    #days are in the range from 0 to Y
    return TOTAL
