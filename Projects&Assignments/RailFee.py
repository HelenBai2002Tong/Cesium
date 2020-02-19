import numpy as np
Line1 = {'Pizarra': 4, 'Alora': 3, 'Alamo': 3, "Lomas": 2, 'Torrox': 1, 'Centro': 0}
Line2 = {'Fuengirola': 4, 'Prados': 4, 'Lima': 3, 'PlazaMayor': 3, "David": 2, 'Col': 1, 'Centro': 0}
AllStation = ['Pizarra', 'Alora', 'Alamo', "Lomas", 'Torrox', 'Centro', 'Fuengirola', 'Prados', 'Lima', 'PlazaMayor', "David",
       'Col']
AllStation.sort()
Line_Check = {'Pizarra': 1, 'Alora': 1, 'Alamo': 1, "Lomas": 1, 'Torrox': 1, 'Centro': 1, 'Fuengirola': 2, 'Prados': 2,
              'Lima': 2, 'PlazaMayor': 2, "David": 2, 'Col': 2}
FARES = np.zeros([11,11])

def getLine(station):
    return Line_Check[station]

def getZone(station):
    if getLine(station) == 1:
        return Line1[station]
    if getLine(station) == 2:
        return Line2[station]


for i in range(10):

    station1 = AllStation[i]
    AZ = getZone(station1)
    AL = getLine(station1)

    for j in range(i + 1, 11):

        station2 = AllStation[j]
        BZ = getZone(station2)
        BL = getLine(station2)

        if AL == BL or station1 == 'Centro' or station2 == "Centro":

            x = AZ - BZ
            if x < 0:
                x = -x
            x += 1
        else:
            x = AZ + BZ + 1
        FARES[i][j] = x
        FARES[j][i] = x

    FARES[i][i] = 0

FARES[10][10] = 0

for line in FARES:
    print(line)