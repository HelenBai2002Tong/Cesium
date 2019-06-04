# -*- coding: utf-8 -*-
import matplotlib
import matplotlib.pyplot as plt

#im=plt.imread('blackholeGray.jpg')
im=plt.imread('1.jpg')
fig = plt.figure()
plt.imshow(im,cmap=plt.cm.gray)
plt.colorbar()
plt.title("Black hole gray image")
plt.show()
#plt.imsave('lena_gray.jpg')

fig = plt.figure()
plt.imshow(im,cmap=plt.cm.jet) # cmap could be plt.cm.hot, plt.cm.jet, plt.cm.rainbow, ...
#plt.imshow(im,cmap=plt.cm.cool)
plt.colorbar()
#plt.title("Black hole color coded image")
plt.show()
#plt.imsave('lena_colorcoded.jpg')
