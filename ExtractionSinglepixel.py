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


img  =  cv2.imread('slic_rag_rotate_signal_linearremoval_SmallNoisePoint.png',0)##导入去噪完全的图像信号
ret , imgB = cv2.threshold(img,127,1,cv2.THRESH_BINARY)#二值化为01像素
linearlabel=[2168, 1736, 2054, 1838, 1946, 2276]#上一个程序霍夫变换去直线，得到的各条直线的Y坐标值
row=imgB.shape[0]#行
col=imgB.shape[1]#列
colzeros=[]
resultList = []#用于存储从图像信号采样下来的每一个点值
for i in range(col):
    K=np.sum(imgB[:,i])  #K为i列的白色点的个数
    c=imgB[:,i].tolist()#将i列变成列表
    newList = list(reversed(c))#翻转列表，便于计算Rlast
    Rfirst=c.index(max(c))#计算i列最大值位置，即I列白色区域的起始点
    Rlast=row-newList.index(max(newList))-1#i列白色区域的终止点
    H=Rlast-Rfirst+1  #H为第一个白点和倒数第一个白点中间的点数个数
    if K != 0:#即信号区域
        if K<H:#即该列含有多个白色区域
            area=[]#用于存放i列含有白点的行值
            for j in range(row):
                if imgB[j,i]==1:
                    area.append(j)

            distancearea=[]
            zuida=[]
            zuixiao=[]
            fun = lambda x: x[1]-x[0]
            for k, g in groupby(enumerate(area), fun):
                l1 = [j for i, j in g]    # 连续数字的列表
                Previous=max(l1)-min(l1)#midPrevious为噪声段上一列白色点段的中心坐标值。
                distancearea.append(Previous)
                zuida.append(max(l1))
                zuixiao.append(min(l1))
                    
                maxdistance=distancearea.index(max(distancearea))
                Rfirst=zuixiao[maxdistance]
                Rlast=zuida[maxdistance]
            samplinglabel=row-(ceil((Rlast-Rfirst)/2)+Rfirst)#计算i列的中间点
            resultList.append(samplinglabel)#计i列的中间点存入
        else:
            samplinglabel=row-(ceil((Rlast-Rfirst)/2)+Rfirst)#计算i列的中间点
            resultList.append(samplinglabel)#计i列的中间点存入
        colzeros.append(i)
    else:
        resultList.append(0) #无信号区域，取值为0

resultListCopy=resultList.copy()
        
Block= []  #存入没有信号点，即断点的i列值
for i in range(col):
    if resultList[i]==0:
        Block.append(i)
    else:
        print("have value")
        
for i in range(col):
    K=np.sum(imgB[:,i])  #K为该列的白色点的个数
    c=imgB[:,i].tolist()
    newList = list(reversed(c))
    Rfirst=c.index(max(c))
    Rlast=row-newList.index(max(newList))-1
    H=Rlast-Rfirst+1  #H为第一个白点第二个白点中间的个数
    if K<H:#即该列含有多个白色区域
        area=[]#用于存放i列含有白点的行值
        for j in range(row):
            if imgB[j,i]==1:
               area.append(j)

        distancearea=[]
        zuida=[]
        zuixiao=[]
        fun = lambda x: x[1]-x[0]
        for k, g in groupby(enumerate(area), fun):
            l1 = [j for i, j in g]    # 连续数字的列表
            Previous=max(l1)-min(l1)#midPrevious为噪声段上一列白色点段的中心坐标值。
            distancearea.append(Previous)
            zuida.append(max(l1))
            zuixiao.append(min(l1))
            maxdistance=distancearea.index(max(distancearea))
            Rfirst=zuixiao[maxdistance]
            Rlast=zuida[maxdistance]
        if abs(int(resultList[i])-int(resultList[i-1]))>15:#计算绝对值，不知道正负，将斜率大于15的，归为快速变换列
            if int(resultList[i])>int(resultList[i-1]):#斜率为正值
                resultListCopy[i]=row-((Rlast-Rfirst)*0.1+Rfirst)#快速变换列不取中间点，取白色区域90
            else:#斜率为负值
                resultListCopy[i]=row-((Rlast-Rfirst)*0.9+Rfirst)
        else:
            print("Not fast change")
    else:
        if abs(int(resultList[i])-int(resultList[i-1]))>15:#计算绝对值，不知道正负，将斜率大于15的，归为快速变换列
            if int(resultList[i])>int(resultList[i-1]):#斜率为正值
                resultListCopy[i]=row-((Rlast-Rfirst)*0.1+Rfirst)#快速变换列不取中间点，取白色区域90
            else:#斜率为负值
                resultListCopy[i]=row-((Rlast-Rfirst)*0.9+Rfirst)
            
        
Block=Block[1:len(Block)-1] #下面会存在加1减1，故先处理下，避免报错

#将断点区域用直线连接起来        
fun = lambda x: x[1]-x[0]
for k, g in groupby(enumerate(Block), fun):
    l1 = [j for i, j in g]    # 连续数字的列表
    scop = str(min(l1)) + '-' + str(max(l1))  # 将连续数字范围用"-"连接
    print("连续数字范围：{}".format(scop))
    for l in range((min(l1)),(max(l1)+1)):
        resultListCopy[l]=int((l-(min(l1)-1))*(resultListCopy[(max(l1)+1)]-resultListCopy[(min(l1)-1)])/((max(l1)+1)-(min(l1)-1)))+resultListCopy[(min(l1)-1)]


#采样步骤，可以设置采样多少倍       
sampling=[]
multiple=4
qu4=ceil(col/multiple)-multiple 
for x in range(qu4):
    sampling.append(resultListCopy[x*multiple])
        
    
#画出图样       
fig = plt.figure()  
ax = fig.add_subplot(1,1,1)
minc=min(colzeros)
maxc=max(colzeros)
ax.plot(resultListCopy[minc:maxc],color='blue')

    