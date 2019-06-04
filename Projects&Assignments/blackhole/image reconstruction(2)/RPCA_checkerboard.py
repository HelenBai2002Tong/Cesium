import numpy as np
from numpy.linalg import norm, svd

def inexact_augmented_lagrange_multiplier(X, mask, lmbda=.001, tol=1e-10,
                                          maxiter=1000, verbose=True):
    """
    Inexact Augmented Lagrange Multiplier
    """
    Y = X
    norm_two = norm(Y.ravel(), 2)
    norm_inf = norm(Y.ravel(), np.inf) / lmbda
    dual_norm = np.max([norm_two, norm_inf])
    Y = Y / dual_norm
    A = np.zeros(Y.shape)
    E = np.zeros(Y.shape)
    dnorm = norm(X, 'fro')
    mu = 1.25 / norm_two
    rho = 1.5
    sv = 10.
    n = Y.shape[0]
    itr = 0
    while True:
        U, S, V = svd(X - E + (1 / mu) * Y, full_matrices=False)
        svp = (S > 1 / mu).shape[0]
        if svp < sv:
            sv = np.min([svp + 1, n])
        else:
            sv = np.min([svp + round(.05 * n), n])
        Aupdate = np.dot(np.dot(U[:, :svp], np.diag(S[:svp] - 1 / mu)), V[:svp, :])
        Eraw = X - Aupdate + (1 / mu) * Y
        Eupdate = np.maximum(Eraw - lmbda / mu, 0) + np.minimum(Eraw + lmbda / mu, 0)
        Eupdate = Eupdate * mask
        A = Aupdate
        E = Eupdate
        Z = X - A - E
        Y = Y + mu * Z
        mu = np.min([mu * rho, mu * 1e7])
        itr += 1
        if ((norm(Z, 'fro') / dnorm) < tol) or (itr >= maxiter):
            break
    if verbose:
        print("Finished at iteration %d" % (itr))  
    return A, E


#生成图像
imagewidth = 240
imageheight = 240
blocksize = 30
groundtruth = np.zeros((imagewidth,imageheight), dtype=np.uint8)
for i in range(imagewidth):
    for j in range(imageheight):
        if(i//blocksize+j//blocksize)%2 != 0 :
            groundtruth[i][j] = 1
groundtruth = groundtruth * 255

#展示原始图像
from PIL import Image
image = Image.fromarray(groundtruth) 
image.show()
image.save('groundtruth.jpg')

#使图片部分像素不可见/损毁
percentage = 0.85  #不可见比例
rand_array = np.array(range(imagewidth*imageheight))
np.random.shuffle(rand_array)
inputimage = groundtruth
mask = np.zeros((imagewidth,imageheight), dtype=np.uint8)
for i in range(int(imagewidth*imageheight*percentage)):
    x = rand_array[i]//imagewidth
    y = rand_array[i]%imagewidth
    inputimage[x][y] = np.random.randint(0, 255)
    mask[x][y] = 1 #mask用于标记损毁点
    
#展示损毁后的图像
image = Image.fromarray(inputimage) 
image.show()
image.save('inputimage.jpg')
image = Image.fromarray(mask*255) 
image.save('mask.jpg')

#修复图像
A, E = inexact_augmented_lagrange_multiplier(inputimage/255, mask)
result = A * 255
image = Image.fromarray(result.astype(np.uint8)) #转换成整数
image.show()
image.save('result.jpg')

