import hashlib
import xlrd
import numpy as np
from passlib.hash import scrypt
import scrypt as sc

def sha256_txt(data):
    result=[]
    i=0
    while True:
        text = data.readline()
        if not text:
            break
        m = hashlib.sha256()
        m.update(text.encode('utf-8'))
        result.append(int(m.hexdigest(),16)*10**(-75))
        i+=1
    return result

def sha256_excel(data):
    result=[]
    nrows = data.nrows
    ncolumns = data.ncols
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
    for i in range(1, nrows):
        m = hashlib.sha3_256()
        for j in range(0, ncolumns):
            text = str(data.cell(i, j).value)
            m.update(text.encode('utf-8'))
        result.append(int(m.hexdigest(),16)*10**(-75))
    return result


def Script_txt(data):
    result=[]
    i=0
    while i<200000:
        text = data.readline()
        if not text:
            break
        m = sc.hash(text.encode("utf-8"),"")
        i+=1
        m = int.from_bytes(m, byteorder='little', signed=True)
        result.append(m * 10 ** (-152))
    data.close()
    return result

def Scrypt_excel(data):
    result=[]
    nrows=data.nrows
    ncolumns=data.ncols
    for i in range(1,20000):
        text=''
        for j in range(0,ncolumns):
            text+=str(data.cell(i,j).value)
            m = sc.hash(text.encode("utf-8"),"")
            m=int.from_bytes(m, byteorder='little', signed=True)
            result.append(m*10**(-152))
    return result

def cal_variance(data):
    return round(np.var(data),4)

words=open("allenglishword.txt")
zipcodes= xlrd.open_workbook('uszips.xlsx')
zipcodes= zipcodes.sheet_by_name('Sheet1')

k=sha256_txt(words)
print(cal_variance(k))
k=sha256_excel(zipcodes)
print(cal_variance(k))
words = open("allenglishword.txt")
k=keccak_txt(words)
print(cal_variance(k))
k=keccak_excel(zipcodes)
print(cal_variance(k))
words = open("allenglishword.txt")
k=Script_txt(words)
print(cal_variance(k))
k=Scrypt_excel(zipcodes)
print(cal_variance(k))

