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




data= loadmat("data1002test.mat")
RealityData = data['data1002test']##提取信号实际的波形参数（即matlab中的数据）
RealityData=np.transpose(RealityData).tolist()
ExtractionData = np.load('ExtractionData.npy')##导入图像信号提取的波形参数（即手机拍照数据）

firstCha=abs(ExtractionData[0]-RealityData[0])

ExtractionData=ExtractionData-firstCha


#采样步骤，可以设置采样多少倍       
sampling=[]
multiple=7

qu4=ceil(len(ExtractionData)/multiple)-multiple 
for x in range(qu4):
    sampling.append(ExtractionData[x*multiple])


#画出图样       
fig = plt.figure()  
ax = fig.add_subplot(1,1,1)
ax.plot(RealityData,color='blue')
ax.plot(sampling,color='red')






