import hashlib
import xlrd
import numpy as np

def sha256_txt(data):
    result=[]
    i=0
    while True:
        text = data.readline()
        if not text:
            break
        m = hashlib.sha256()
        m.update(text.encode('utf-8'))
        result.append(int(m.hexdigest(),16)*10**(-70))
        i+=1
        if i%1000==0:
            print(i%1000)
            print(round(np.var(result),4))
    return result

def sha256_excel(data):
    result=[]
    nrows = data.nrows
    ncolumns = data.ncols
    print(nrows)
    for i in range(1, nrows):
        m = hashlib.sha256()
        for j in range(0, ncolumns):
            text = str(data.cell(i, j).value)
            m.update(text.encode('utf-8'))
        result.append(int(m.hexdigest(),16)*10**(-75))
    return result

def keccak_txt(data):
    result=[]
    while True:
        text = data.readline()
        if not text:
            break
        m = hashlib.sha3_256()
        m.update(text.encode('utf-8'))
        result.append(int(m.hexdigest(),16)*10**(-75))
    return result

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
        result.append(int(m.hexdigest(),16)*10**(-75))
    return result

def cal_variance(data):
    return round(np.var(data),4)

words=open("allenglishword.txt")
zipcodes= xlrd.open_workbook('uszips.xlsx')
zipcodes= zipcodes.sheet_by_name('Sheet1')

k=sha256_txt(words)
print(cal_variance(k))
