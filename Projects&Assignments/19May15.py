VALUES=[20,6,38,50,40]
LIMIT = 4
FLAG = True
while FLAG == True:
    FLAG = False
    for COUNTER in range(LIMIT):
        if VALUES[COUNTER] > VALUES[COUNTER + 1]:
            TEMPORARY = VALUES[COUNTER]
            VALUES[COUNTER] = VALUES[COUNTER + 1]
            VALUES[COUNTER + 1] = TEMPORARY
            FLAG=True
print(VALUES)
