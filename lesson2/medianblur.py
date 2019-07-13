# -*- coding: utf-8 -*-
# @Time     : 2019/7/13 9:10
# @Author   : Li Wenyi
# @File     : medianblur.py

import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import random

def medianBlur(img,kernel,padding_way,padding_size):
    kernel = np.array(kernel)
    k_h,k_w = kernel.shape
    img = np.array(img)
    h,w = img.shape
    if padding_way.lower() == 'zero':
        new_img = np.zeros((h + 2*padding_size, w + 2*padding_size))
        new_img[padding_size:h + padding_size, padding_size:w + padding_size] = img

    if padding_way.lower() == 'replica':
        new_img = np.zeros((h + 2 * padding_size, w + 2 * padding_size))
        new_img[padding_size:h + padding_size, padding_size:w + padding_size] = img
        #up
        new_img[0:padding_size,padding_size:w+padding_size] = img[0,0:w]
        #left
        new_img[padding_size:h+padding_size,0:padding_size] = np.tile(img[0:h,0][:, np.newaxis],(padding_size,))
        #down
        new_img[h+padding_size:h+padding_size*2,padding_size:w+padding_size] = img[h-1,0:w]
        #right
        new_img[padding_size:h+padding_size,w+padding_size:w+padding_size*2] = np.tile(img[0:h,w-1][:, np.newaxis],(padding_size,))
        #leftup
        new_img[0:padding_size,0:padding_size] = img[0,0]
        #rightup
        new_img[0:padding_size,w+padding_size:w+padding_size*2] = img[0,w-1]
        #leftdown
        new_img[h+padding_size:h+padding_size*2,0:padding_size] = img[h-1,0]
        #rightdown
        new_img[h+padding_size:h+padding_size*2,w+padding_size:w+padding_size*2] = img[h-1,w-1]
    new_h = (h+2-k_h) + 1
    new_w = (w+2-k_w) + 1
    median_img = np.zeros((new_h,new_w))
    for i in range(new_h):
        for j in range(new_w):
            median_img[i,j] = int(np.median(new_img[i+padding_size-int(k_h / 2): i+padding_size+int(k_h/2),j+padding_size-int(k_w/2):j+padding_size+int(k_w/2)]))
    print("Median_img is: ")
    print(median_img)
    return  median_img
def sp_noise(image,prob):
    '''
    添加椒盐噪声
    prob:噪声比例
    '''
    output = np.zeros(image.shape,np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    return output

#使用自定义list做测试
a = [[1,2,3],[3,4,4],[7,8,9]]
b = np.array(a)
print("midian kernel shape is: ",b.shape)
medianBlur(a,b,'replica',1)


#使用灰度图去除椒盐噪声
path = "lena.jpg"
lena = cv2.imread(path,0)
lena_noise = sp_noise(lena,0.01)
#显示椒盐噪声图
plt.imshow(Image.fromarray(lena_noise))
plt.show()
lena_blur = medianBlur(lena_noise,b,'replica',1)
lena_blur = Image.fromarray(lena_blur)
#显示经过中值滤波后的效果
plt.imshow(lena_blur)
plt.show()
