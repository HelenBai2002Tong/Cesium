import time as t
import hashlib
import xlrd
import numpy as np

words=open("allenglishword.txt")
zipcodes= xlrd.open_workbook('uszips.xlsx')
data= zipcodes.sheet_by_name('Sheet1')

def keccak_excel(data):
    result=[]
    nrows = data.nrows
    ncolumns = data.ncols
    print(nrows)
    for i in range(1, nrows):
        m = hashlib.sha3_256()
        for j in range(0, ncolumns):
            text = str(data.cell(i, j).value)
            m.update(text.encode('utf-8'))
        print("m",m)
        k=m.hexdigest()
        print("int",int(k,16))
        result.append(m)

    return result
keccak_excel(data)