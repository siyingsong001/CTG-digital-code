#基于slic的区域融合
from skimage import data, io, segmentation, color
from skimage.future import graph
import numpy as np
import math



def _weight_mean_color(graph, src, dst, n):
    """Callback to handle merging nodes by recomputing mean color.

    The method expects that the mean color of `dst` is already computed.
    """

    diff = graph.node[dst]['mean color'] - graph.node[n]['mean color']
    diff = np.linalg.norm(diff)
    return {'weight': diff}


def merge_mean_color(graph, src, dst):
    """Callback called before merging two nodes of a mean color distance graph.

    This method computes the mean color of `dst`.
    """
    
    graph.node[dst]['total color'] += graph.node[src]['total color']
    graph.node[dst]['pixel count'] += graph.node[src]['pixel count']
    graph.node[dst]['mean color'] = (graph.node[dst]['total color'] /
                                     graph.node[dst]['pixel count'])

import cv2
img = cv2.imread('D:/liuzhikangxiaolunwen/daima/tupian/1047/data1047.jpg')#导入原始拍照后的信号图像CTG
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # Changes color back to RGB.

w=img.shape[0]
h=img.shape[1]

labels = segmentation.slic(img, compactness=10, n_segments=307200)#进行slic超像素的过分割，网格线边长10像素，网格点边长15像素，故slic预分割边长15个像素


g = graph.rag_mean_color(img, labels)#生成区域邻接图RAG
#合并RAG中区域相似的超像素块，阈值设为70
labels2 = graph.merge_hierarchical(labels, g, thresh=70, rag_copy=False,
                                   in_place_merge=True,
                                   merge_func=merge_mean_color,
                                   weight_func=_weight_mean_color)

countLabel=np.max(labels2)#合并后区域数
area = []#每个区域的面积
for i in range(1, countLabel):
    area.append(np.sum(labels2 == i))
    
    
area1=area.copy()
area1.sort(reverse=True)#将面积从大到小排列

#寻找到信号线的区域，一般最大的为背景部分，所以选取第二或第三大的区域
xuhao1=area.index(area1[1])#记录信号线区域的labels2中的序号
xuhao2=area.index(area1[5])

#将labels3等于labels2，将选取区域标签为1，其余为选取的标签为2
row=labels2.shape[0]
col=labels2.shape[1]
labels3=labels2.copy()
for k in range(0, row):
    for j in range(0, col):
        if labels3[k][j]==xuhao1+1 or labels3[k][j]==xuhao2+1:
           labels3[k][j]=1
        else:
             labels3[k][j]=2

#将labels3中不同的标签依次涂色，为白黑，故信号区域为白色，其他为黑色
out = color.label2rgb(labels3,colors=( 'white', 'black'))
#out = segmentation.mark_boundaries(out, labels3, (0, 0, 0))

io.imshow(out)
print("hello")
io.show()
print("world")
io.imsave('D:/liuzhikangxiaolunwen/daima/tupian/1047/1047_slic_rag_signal_80.png', out)#保存slic结合RAG提取的信号
print("123")
