# -*- coding: utf-8 -*-
#主要用于去除去除直线后图像存在的两个问题：
#一、图像上还有多余的噪点
#二、图像上的信号有些由于去直线断裂的。
"""
Created on Tue Jun 25 21:52:47 2019

@author: Administrator
"""

import  cv2
import  numpy  as  np
from skimage import data, io, segmentation, color
from math import ceil
import matplotlib.pyplot as plt
from itertools import groupby


img  =  cv2.imread('rotate_signal.png',0)
ret , imgB = cv2.threshold(img,80,255,cv2.THRESH_BINARY)#二值化为01像素

h,w=imgB.shape #返回高和宽
 

 
a = [0 for z in range(0, h)] 
print(a) 
 
for j in range(0,h):  
    for i in range(0,w):  
        if  imgB[j,i]==0: 
            a[j]+=1 
            imgB[j,i]=255
         
for j  in range(0,h):  
    for i in range(0,a[j]):   
        imgB[j,i]=0    
 
plt.imshow(imgB,cmap=plt.gray())


    