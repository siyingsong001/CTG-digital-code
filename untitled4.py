# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 16:06:31 2019

@author: Administrator
"""



from scipy.io import loadmat
import matplotlib.pyplot as plt
import  cv2
import  numpy  as  np
from math import ceil
import numpy as np
import pylab as pl
from scipy import interpolate 
import matplotlib.pyplot as plt




data= loadmat("data1002test.mat")
RealityData = data['data1002test']##提取信号实际的波形参数（即matlab中的数据）
RealityData=np.transpose(RealityData).tolist()
ExtractionData = np.load('ExtractionData.npy')##导入图像信号提取的波形参数（即手机拍照数据）

BackgridRfirst=751  #背景网格行的起始像素行
BackgridRlast=3431  #背景网格行的终止像素行
BackgridCfirst=471  #背景虚线的起始列像素列
BackgridClast=4930  #背景虚线的终止列像素列


ActualColumnToPixel=(BackgridClast-BackgridCfirst)/620#求取实际网格列数值1对应多少像素，时间点数对应多少像素，即采样的比例
DataInterception=ExtractionData[BackgridCfirst:BackgridClast]
y=DataInterception
x=np.linspace(0, BackgridClast-BackgridCfirst,BackgridClast-BackgridCfirst)

x_new = np.linspace(0, BackgridClast-BackgridCfirst,620)


tck = interpolate.splrep(x, y)
y_bspline = interpolate.splev(x_new, tck)



plt.plot(x, y, "o",  label=u"原始数据")

plt.plot(x_new, y_bspline, label=u"B-spline插值")

pl.legend()
pl.show()