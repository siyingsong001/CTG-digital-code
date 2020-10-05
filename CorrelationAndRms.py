# -*- coding: utf-8 -*-
"""
Created on Sat Jun 29 13:25:37 2019

@author: Administrator
"""
from scipy.io import loadmat
import matplotlib.pyplot as plt
import  cv2
import  numpy  as  np
from math import ceil
import pylab as pl
from scipy import interpolate 
from numpy import *
from numpy import math

import scipy.stats as stats




data= loadmat("data1002test.mat")
RealityData = data['data1002test']##提取信号实际的波形参数（即matlab中的数据）
RealityData=np.transpose(RealityData).tolist()
ExtractionData = np.load('ExtractionData.npy')##导入图像信号提取的波形参数（即手机拍照数据）

BackgridRfirst=751  #背景网格行的起始像素行
BackgridRlast=3430  #背景网格行的终止像素行
BackgridCfirst=471  #背景虚线的起始列像素列
BackgridClast=4915  #背景虚线的终止列像素列

##直接采样数据
ActualColumnToPixel=(BackgridClast-BackgridCfirst)/620#求取实际网格列数值1对应多少像素，时间点数对应多少像素，即采样的比例
DataInterception=ExtractionData[BackgridCfirst:BackgridClast]
y=DataInterception
x=np.linspace(0, BackgridClast-BackgridCfirst,BackgridClast-BackgridCfirst)
x_new = np.linspace(0, BackgridClast-BackgridCfirst,599)
tck = interpolate.splrep(x, y)
y_bspline = interpolate.splev(x_new, tck)##y_bspline为手机拍照信号采样后的数据
Sampledata=y_bspline




ActualRowToPixel=(BackgridRlast-BackgridRfirst)/(250-50) #求取实际网格行数值1对应多少像素

ExtractionDataToActual=(Sampledata-BackgridRfirst)/ActualRowToPixel

cha=np.mat(ExtractionDataToActual).mean()-np.mat(RealityData).mean()

ExtractionDataToActual=ExtractionDataToActual-cha

#画出图样       
fig = plt.figure()  
ax = fig.add_subplot(1,1,1)
ax.plot(RealityData,color='blue')
ax.plot(ExtractionDataToActual,color='red')


def calc_corr(a, b):
	a_avg = sum(a)/len(a)
	b_avg = sum(b)/len(b)
 
	# 计算分子，协方差————按照协方差公式，本来要除以n的，由于在相关系数中上下同时约去了n，于是可以不除以n
	cov_ab = sum([(x - a_avg)*(y - b_avg) for x,y in zip(a, b)])
 
	# 计算分母，方差乘积————方差本来也要除以n，在相关系数中上下同时约去了n，于是可以不除以n
	sq = math.sqrt(sum([(x - a_avg)**2 for x in a])*sum([(x - b_avg)**2 for x in b]))
 
	corr_factor = cov_ab/sq
 
	return corr_factor

def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

CorrelationCoefficient=calc_corr(list(RealityData),list(ExtractionDataToActual))
Rmse=rmse(RealityData,ExtractionDataToActual)



