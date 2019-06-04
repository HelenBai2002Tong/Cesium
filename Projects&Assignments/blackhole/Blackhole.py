import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

points = np.arange(-5,5,0.01)

xs,ys = np.meshgrid(points,points)

z = np.sqrt(xs**2 + ys**2)
#z = np.sqrt(abs(xs) + abs(ys))
#创建新的figure
# fig = plt.figure()
# plt.imshow(z,cmap=plt.cm.jet)
# plt.colorbar()
#
# plt.show()
# fig = plt.figure()
# plt.imshow(z,cmap=plt.cm.hot)
# plt.colorbar()
# plt.show()
#
# fig = plt.figure()
# plt.imshow(z,cmap=plt.cm.cool)
# plt.colorbar()
# plt.show()
#
# fig = plt.figure()
# plt.imshow(z,cmap=plt.cm.gray)
# plt.colorbar()
#
# plt.show()
im=plt.imread('lena.jpg')
fig = plt.figure()
plt.imshow(im,cmap=plt.cm.gray)
plt.colorbar()
plt.title("Black hole gray image")
plt.imsave('lena_gray.jpg')

fig = plt.figure()
plt.imshow(im,cmap=plt.cm.rainbow) # cmap could be plt.cm.hot, plt.cm.jet, plt.cm.rainbow, ...
#plt.imshow(im,cmap=plt.cm.cool)
plt.colorbar()
plt.title("Black hole color coded image")
plt.imsave('lena_colorcoded.jpg')
