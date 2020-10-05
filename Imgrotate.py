# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 11:12:07 2019

@author: Administrator
"""
#图像旋转校正
#先通过hough transform检测图片中的图片，计算直线的倾斜角度并实现对图片的旋转
import os
import cv2
import math
import random
import numpy as np
from scipy import misc, ndimage
from skimage import data, io, segmentation, color



img = cv2.imread('D:/liuzhikangxiaolunwen/daima/tupian/1031/1031_slic_rag_signal_65.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
	
#霍夫变换
lines = cv2.HoughLines(edges,1,np.pi/180,0)
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))


t = float(y2-y1)/(x2-x1)
rotate_angle = math.degrees(math.atan(t))
if rotate_angle > 45:
    rotate_angle = -90 + rotate_angle
elif rotate_angle < -45:
    rotate_angle = 90 + rotate_angle
rotate_img = ndimage.rotate(img, rotate_angle)
#cv2.namedWindow('rotate_angle',cv2.WINDOW_NORMAL)
#cv2.imshow('rotate_angle', rotate_img)
#cv2.imwrite('xunzhuanheipre',rotate_img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()

io.imshow(rotate_img)
io.show()
io.imsave('D:/liuzhikangxiaolunwen/daima/tupian/1031/1031_slic_rag_signal_65_rotate_imag.png', rotate_img)
