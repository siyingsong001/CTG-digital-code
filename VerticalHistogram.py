# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 16:06:31 2019

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

thresh3=imgB#250  输出[0,0]这个点的像素值  				#返回值ret为阈值
# print(ret)#130
(h,w)=thresh3.shape #返回高和宽
# print(h,w)#s输出高和宽
a = [0 for z in range(0, w)] 
print(a) #a = [0,0,0,0,0,0,0,0,0,0,...,0,0]初始化一个长度为w的数组，用于记录每一列的黑点个数  
 
#记录每一列的波峰
for j in range(0,w): #遍历一列 
    for i in range(0,h):  #遍历一行
        if  thresh3[i,j]==0:  #如果改点为黑点
            a[j]+=1  		#该列的计数器加一计数
            thresh3[i,j]=255  #记录完后将其变为白色 
    # print (j)           
 
#            
for j  in range(0,w):  #遍历每一列
    for i in range((h-a[j]),h):  #从该列应该变黑的最顶部的点开始向最底部涂黑
        thresh3[i,j]=0   #涂黑
 
#此时的thresh1便是一张图像向垂直方向上投影的直方图
#如果要分割字符的话，其实并不需要把这张图给画出来，只需要的到a=[]即可得到想要的信息
 
 
# img2 =Image.open('0002.jpg')
# img2.convert('L')
# img_1 = np.array(img2)
plt.imshow(thresh3,cmap=plt.gray())
plt.show()

cv2.waitKey(0)  
cv2.destroyAllWindows() 