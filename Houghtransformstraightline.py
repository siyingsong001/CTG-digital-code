#使用霍夫变换检测直线的Y坐标值，将Y这一行遍历每一列，通过每列的上下10个值的总和是否小于12判定像素是否在信号线上
#小于则认定为直线将该列上下10个像素归为0，即变黑。
#然后遍历每一条直线，直到直线全部去除
# -*- coding: utf-8 -*-

"""
Created on Sun Jun 23 14:51:28 2019
@author: Administrator
"""
import  cv2
import  numpy  as  np
from skimage import data, io, segmentation, color

#img  =  cv2.imread('slic_rag_rotate_signal_linearremoval2.png')
img  =  cv2.imread('D:/liuzhikangxiaolunwen/daima/tupian/1030/1030_slic_rag_signal_70_rotate_imag.png')
imgB=cv2.imread('D:/liuzhikangxiaolunwen/daima/tupian/1030/1030_slic_rag_signal_70_rotate_imag.png',0)
ret , imgB = cv2.threshold(imgB,127,1,cv2.THRESH_BINARY)#二值化为01像素
gray  =  cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)


#edges = cv2.Canny(img, 50, 150, apertureSize = 3)
lines = cv2.HoughLines(gray,1,np.pi/180,10) #这里对最后一个参数使用了经验型的值
result = img.copy()

rho=3253
col=imgB.shape[1]
for i in range(col):
    pixel=int(imgB[rho,i])+int(imgB[rho+1,i])+int(imgB[rho+6,i])+int(imgB[rho+2,i])+int(imgB[rho+7,i])+int(imgB[rho+3,i])+int(imgB[rho+4,i])+int(imgB[rho+5,i])+int(imgB[rho+10,i])\
    +int(imgB[rho-1,i])+int(imgB[rho-6,i])+int(imgB[rho-2,i])+int(imgB[rho-3,i])+int(imgB[rho-4,i])+int(imgB[rho-5,i])+imgB[rho-7,i]+imgB[rho-8,i]+imgB[rho-9,i]+imgB[rho-10,i]
  #  pixel = int(imgB[rho, i]) + int(imgB[rho + 1, i]) + int(imgB[rho + 2, i]) + int(imgB[rho + 3, i]) + int(imgB[rho + 4, i]) + int(imgB[rho + 5, i]) +int(imgB[rho-1,i])+int(imgB[rho-2,i])+int(imgB[rho-3,i])+int(imgB[rho-4,i])
    if pixel < 9:
        imgB[rho,i]=0
        imgB[rho+1,i]=0
        imgB[rho+6,i]=0
        imgB[rho+2,i]=0
        imgB[rho+7,i]=0
        imgB[rho+3,i]=0
     #   imgB[rho + 8, i] = 0
      #  imgB[rho + 9, i] = 0
      #  imgB[rho + 10, i] = 0
       
        imgB[rho+4,i]=0

        imgB[rho+5,i]=0

        imgB[rho-1,i]=0
        imgB[rho-6,i]=0
        imgB[rho-2,i]=0
        imgB[rho-7,i]=0
        imgB[rho-3,i]=0
      
        imgB[rho-4,i]=0

        imgB[rho-5,i]=0
      #  imgB[rho - 8, i] = 0
      #  imgB[rho - 9, i] = 0
      #  imgB[rho - 10, i] = 0


out = color.label2rgb(imgB,colors=( 'black', 'white'))


io.imshow(out)
io.show()
#io.imsave('slic_rag_rotate_signal_linearremoval_SmallNoisePoint.png', out)
        
