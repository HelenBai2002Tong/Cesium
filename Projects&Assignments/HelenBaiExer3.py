# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 08:38:38 2018

@author: admin
"""
s = 'azcbobobegghakl'
p=0
for i in s:
    if i in ["a","e","i","o","u"]:
        p=p+1
print("Number of vowels:",p)