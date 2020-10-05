#超像素的划分
from skimage.segmentation import slic,mark_boundaries
import cv2
import matplotlib.pyplot as plt
# import numpy as np
#
# np.set_printoptions(threshold=np.inf)

img =cv2.imread('data1002.png')




segments2 = slic(img, n_segments=90000, compactness=10)
out2=mark_boundaries(img,segments2)
plt.subplot(111)
plt.title("n_segments=900")
plt.imshow(out2)

plt.show()
