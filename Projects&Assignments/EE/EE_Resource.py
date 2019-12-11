import hashlib
import xlrd
from memory_profiler import profile

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
if __name__ == "__main__":
    words=open("allenglishword.txt")
    zipcodes = xlrd.open_workbook('uszips.xlsx')
    zipcodes = zipcodes.sheet_by_name('Sheet1')
    sha256_txt(words)
    sha256_excel(zipcodes)
    keccak_txt(words)
    keccak_excel(zipcodes)

