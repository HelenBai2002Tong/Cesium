import time as t
import hashlib
import xlrd
from passlib.hash import scrypt
import base64
import uuid

words=open("allenglishword.txt")
zipcodes= xlrd.open_workbook('uszips.xlsx')
zipcodes= zipcodes.sheet_by_name('Sheet1')

def cal_time(f,data):
    start=t.time()
    f(data)
    end=t.time()-start
    print(end)


def sha256_txt(data):
    while True:
        text = data.readline()
        if not text:
            break
        m = hashlib.sha256()
        m.update(text.encode('utf-8'))


def sha256_excel(data):
    nrows=data.nrows
    ncolumns=data.ncols
    for i in range(1,nrows):
        m = hashlib.sha256()
        for j in range(0,ncolumns):
            text=str(data.cell(i,j).value)
            m.update(text.encode('utf-8'))
    print(nrows,ncolumns)

def keccak_txt(data):
    while True:
        text = data.readline()
        if not text:
            break
        m = hashlib.sha3_256()
        m.update(text.encode('utf-8'))
    data.close()

def keccak_excel(data):
    nrows=data.nrows
    ncolumns=data.ncols
    for i in range(1,nrows):
        m = hashlib.sha3_256()
        for j in range(0,ncolumns):
            text=str(data.cell(i,j).value)
            m.update(text.encode('utf-8'))

def Script_txt(data):
    i=0
    while i<200:
        text = data.readline()
        if not text:
            break
        m = scrypt.hash(text.encode("utf-8"))
        i+=1
    data.close()

def Scrypt_excel(data):
    nrows=data.nrows
    ncolumns=data.ncols
    for i in range(1,20):
        text=''
        for j in range(0,ncolumns):
            text+=str(data.cell(i,j).value)
            m = scrypt.hash(text.encode("utf-8"))

'''
cal_time(sha256_txt,words)

words.close()

cal_time(sha256_excel,zipcodes)

words=open("allenglishword.txt")
cal_time(keccak_txt,words)
words.close()

cal_time(keccak_excel,zipcodes)'''


words=open("allenglishword.txt")
cal_time(Script_txt,words)
words.close()
cal_time(Scrypt_excel,zipcodes)


