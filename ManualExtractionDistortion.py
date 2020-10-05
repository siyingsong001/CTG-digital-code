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
BackgridCfirst=512  #背景虚线的起始列像素列
BackgridClast=4915  #背景虚线的终止列像素列

RealityData1=[]
for i in range(len(RealityData)):
    RealityData1.append(RealityData[i][0])

##直接采样数据

DataInterception=ExtractionData[BackgridCfirst:BackgridClast]
fig = plt.figure()  
ax = fig.add_subplot(1,1,1)
ax.plot(DataInterception)

y=DataInterception
  
xuanqudedian=[0,433,1179,1919,2665,3398,4124,4402]
###################第1#######################
y1=DataInterception[xuanqudedian[0]:xuanqudedian[1]]
x1=np.linspace(0, xuanqudedian[1]-xuanqudedian[0],xuanqudedian[1]-xuanqudedian[0])
x_new1 = np.linspace(0, xuanqudedian[1]-xuanqudedian[0],60)
tck1 = interpolate.splrep(x1, y1)#需要先使用splrep函数计算出B-Spline曲线的参数
y_bspline1 = interpolate.splev(x_new1, tck1)##y_bspline为手机拍照信号采样后的数据
y_bspline=y_bspline1

#######################################
bl=len(xuanqudedian)
for i in range(2,bl-1):
    y=DataInterception[xuanqudedian[i-1]:xuanqudedian[i]]
    x=np.linspace(0, xuanqudedian[i]-xuanqudedian[i-1],xuanqudedian[i]-xuanqudedian[i-1])
    x_new = np.linspace(0, xuanqudedian[i]-xuanqudedian[i-1],100)
    tck= interpolate.splrep(x, y)#需要先使用splrep函数计算出B-Spline曲线的参数
    y_bspline2 = interpolate.splev(x_new, tck)##y_bspline为手机拍照信号采样后的数据
    y_bspline=np.append(y_bspline,y_bspline2)
    
#######################################
    ###################第7#######################
y7=DataInterception[xuanqudedian[6]:xuanqudedian[7]]
x7=np.linspace(0, xuanqudedian[7]-xuanqudedian[6],xuanqudedian[7]-xuanqudedian[6])
x_new7= np.linspace(0, xuanqudedian[7]-xuanqudedian[6],40)
tck7 = interpolate.splrep(x7, y7)#需要先使用splrep函数计算出B-Spline曲线的参数
y_bspline7 = interpolate.splev(x_new7, tck7)##y_bspline为手机拍照信号采样后的数据
y_bspline=np.append(y_bspline,y_bspline7)



Sampledata=y_bspline

ActualRowToPixel=(BackgridRlast-BackgridRfirst)/(250-50) #求取实际网格行数值1对应多少像素

ExtractionDataToActual=(Sampledata-BackgridRfirst)/ActualRowToPixel

cha=np.mat(ExtractionDataToActual).mean()-np.mat(RealityData).mean()

ExtractionDataToActual=ExtractionDataToActual-cha

#画出图样       
fig = plt.figure()  
ax = fig.add_subplot(1,1,1)
ax.plot(RealityData1,color='blue')
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

CorrelationCoefficient=calc_corr(list(RealityData1),list(ExtractionDataToActual))
Rmse=rmse(ExtractionDataToActual,RealityData1)