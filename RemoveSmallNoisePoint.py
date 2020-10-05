import cv2
import numpy as np
from skimage import data, io, segmentation, color





img  =  cv2.imread('slic_rag_rotate_signal_linearremoval1.png')
imgB=cv2.imread('slic_rag_rotate_signal_linearremoval1.png',0)
ret , imgB = cv2.threshold(imgB,127,1,cv2.THRESH_BINARY)#二值化为01像素

binary , contours, hierarchy = cv2.findContours(imgB ,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)    # 输出为三个参数  
cv2.drawContours(img,contours,-1,(0,0,255),3)


for i in range(len(contours)):
    area = cv2.contourArea(contours[i])
    if area < 300:
        cv2.drawContours(imgB,[contours[i]],0,0,-1)


out = color.label2rgb(imgB,colors=( 'black', 'white'))
io.imshow(out)
io.show()
#io.imsave('slic_rag_rotate_signal_linearremoval_SmallNoisePoint.png', out)

img  =  cv2.imread('slic_rag_rotate_signal_linearremoval_SmallNoisePoint.png')
io.imshow(img)
io.show()