import hashlib
import xlrd
import numpy as np
from passlib.hash import scrypt
import scrypt as sc

h1 = sc.hash('password',"r")
print("h1",h1)
print("int",int.from_bytes(h1, byteorder='little', signed=True))

m = hashlib.sha256()
m.update("password".encode('utf-8'))
print(int(m.hexdigest(), 16))

m = hashlib.sha3_256()
m.update("password".encode('utf-8'))
print(int(m.hexdigest(), 16))