# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 16:06:31 2019

@author: Administrator
"""

"""
cv2.morphologyEx(src,      # 输入图片
                 op,       # 需要处理类型的函数：(cv2.MORPH_OPEN,cv2.MORPH_CLOSE,cv2.MORPH_GRADIENT)
                 kernel,   # 卷积核大小
                 dst=None, 
                 anchor=None, 
                 iterations=None,     #迭代次数，默认1次
                 borderType=None, 
                 borderValue=None)
"""
import cv2
import numpy as np
from skimage import data, io, segmentation, color

img  =  cv2.imread('D:/liuzhikangxiaolunwen/daima/tupian/1047/1047_slic_rag_signal_80_rotate_imag.png')
imgB=cv2.imread('D:/liuzhikangxiaolunwen/daima/tupian/1047/1047_slic_rag_signal_80_rotate_imag.png',0)
ret , imgB = cv2.threshold(imgB,127,1,cv2.THRESH_BINARY)#二值化为01像素

# B, G, img = cv2.split(res)
# _,RedThresh = cv2.threshold(img,160,255,cv2.THRESH_BINARY)     #设定红色通道阈值160（阈值影响开闭运算效果）
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(50,1))         #定义矩形结构元素
opened1 = cv2.morphologyEx(imgB, cv2.MORPH_OPEN, kernel,iterations=1)     #开运算1

lines = cv2.HoughLines(opened1,1,np.pi/180,50) #这里对最后一个参数使用了经验型的值

result = img.copy()

for line in lines[3]:
	rho = line[0] #第一个元素是距离rho
	theta= line[1] #第二个元素是角度theta
    
numberLine=len(lines)
ynum=[]
for i in range(numberLine):
    for line in lines[i]:
        if line[1]==theta:
            ynum.append(line[0])

    
            
            
for i in range(len(ynum)):
    rho=int(ynum[i])
    col=imgB.shape[1]
    for i in range(col):
        pixel=int(imgB[rho,i])+int(imgB[rho+1,i])+int(imgB[rho+6,i])+int(imgB[rho+2,i])+int(imgB[rho+3,i])+int(imgB[rho+4,i])+int(imgB[rho+5,i])+int(imgB[rho+7,i])+int(imgB[rho+8,i])+int(imgB[rho+9,i])+int(imgB[rho+10,i])\
            +int(imgB[rho-1,i])+int(imgB[rho-6,i])+int(imgB[rho-2,i])+int(imgB[rho-3,i])+int(imgB[rho-4,i])+int(imgB[rho-5,i])+int(imgB[rho-7,i])+int(imgB[rho-8,i])+int(imgB[rho-9,i])+int(imgB[rho-10,i])
        if pixel < 6:
        
            imgB[rho,i]=0
            imgB[rho+1,i]=0
            imgB[rho+2,i]=0        
            imgB[rho+3,i]=0
            imgB[rho+4,i]=0        
            imgB[rho+5,i]=0
            imgB[rho+6,i]=0
            imgB[rho+7,i]=0
            
            
            
            imgB[rho-1,i]=0
            imgB[rho-2,i]=0        
            imgB[rho-3,i]=0              
            imgB[rho-4,i]=0        
            imgB[rho-5,i]=0
            imgB[rho-6,i]=0
            imgB[rho-7,i]=0
            
            
            

            
        

out = color.label2rgb(imgB,colors=( 'black', 'white'))


io.imshow(out)
io.show()
io.imsave('D:/liuzhikangxiaolunwen/daima/tupian/1047/1047_slic_rag_signal_80_rotate_imag_remove.png', out)
