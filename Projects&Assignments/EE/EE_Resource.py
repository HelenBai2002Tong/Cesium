import hashlib
import xlrd
from memory_profiler import profile
from passlib.hash import scrypt
import scrypt as sc
@profile(precision=6)
def sha256_txt(data):
    while True:
        text = data.readline()
        if not text:
            break
        m = hashlib.sha256()
        m.update(text.encode('utf-8'))

@profile(precision=6)
def sha256_excel(data):
    nrows = data.nrows
    ncolumns = data.ncols
    print(nrows)
    for i in range(1, nrows):
        m = hashlib.sha256()
        for j in range(0, ncolumns):
            text = str(data.cell(i, j).value)
            m.update(text.encode('utf-8'))

@profile(precision=6)
def keccak_txt(data):
    while True:
        text = data.readline()
        if not text:
            break
        m = hashlib.sha3_256()
        m.update(text.encode('utf-8'))

@profile(precision=6)
def keccak_excel(data):
    nrows = data.nrows
    ncolumns = data.ncols
    print(nrows)
    for i in range(1, nrows):
        m = hashlib.sha3_256()
        for j in range(0, ncolumns):
            text = str(data.cell(i, j).value)
            m.update(text.encode('utf-8'))
@profile(precision=6)
def Script_txt(data):
    i=0
    while i<200:
        text = data.readline()
        if not text:
            break
        m = sc.hash(text.encode("utf-8"),"")
        i+=1
    data.close()
@profile(precision=10)
def Scrypt_excel(data):
    nrows=data.nrows
    ncolumns=data.ncols
    for i in range(1,20):
        text=''
        for j in range(0,ncolumns):
            text+=str(data.cell(i,j).value)
            m = sc.hash(text.encode("utf-8"),"")

if __name__ == "__main__":
    words=open("allenglishword.txt")
    zipcodes = xlrd.open_workbook('uszips.xlsx')
    zipcodes = zipcodes.sheet_by_name('Sheet1')
   # sha256_txt(words)
    #sha256_excel(zipcodes)
    #words = open("allenglishword.txt")
    #keccak_txt(words)
    #keccak_excel(zipcodes)
    words = open("allenglishword.txt")
    Script_txt(words)
    Scrypt_excel(zipcodes)

