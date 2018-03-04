###Slice.py
# Use to slice an image into vectors
# swag

#############CONSTANTS
IMAGE_SIZE=(256,256)

##################

import numpy as np
from PIL import Image
import matplotlib
#%matplotlib qt5
import matplotlib.pyplot as plt
import scipy.signal
from skimage import morphology as mp
from skimage import exposure
import slice_lib as slib
from mpl_toolkits.mplot3d import axes3d

IMAGE_FACTOR = (IMAGE_SIZE[0]*IMAGE_SIZE[1]) ** (1. / 4) / 4

gaussian = slib.gaussian_2d(IMAGE_FACTOR)

image_names = ["eiffel.jpg", "lisa.jpg", "fish.jpg"]

def vectorize(segment):
    vector_list = []
    going_left = False
    for i in range(segment.shape[1]):
        row = segment[:,i]
        rsum = np.sum(row)
        if rsum>0:
            xor = np.argwhere(np.logical_xor(np.insert(row[:-1],0,False),row))
            if going_left:
                xor = np.flip(xor,0)
            for j in range(int(len(xor)/2)):
                vector_list.append(((int(xor[2*j]),i),(int(xor[2*j+1]),i)))
            going_left = !going_left
    return vector_list


for imgname in image_names[1:2]:
    picture = Image.open(imgname).convert("L")
    picture = picture.resize(IMAGE_SIZE, Image.BICUBIC)
    pic_array = np.array(picture)

    np.mean(pic_array)
    np.median(pic_array)

    # Equalization
    img_eq = exposure.equalize_hist(pic_array)

    display_image, display_layered,\
     seg_bot, seg_mid, seg_top = slib.segment_image(pic_array, gaussian)

    plt.imshow(display_image, cmap="YlOrBr_r")
    plt.show()
    plt.imshow(display_layered ** .2 + 1000, cmap="gist_ncar")
    plt.show()

    # fig=plt.figure()
    # ax=fig.add_subplot(111,projection='3d')
    # x,y = np.meshgrid(np.arange(IMAGE_SIZE[0]),np.arange(IMAGE_SIZE[1]))
    # ax.contourf3D(x, y, display_layered, cmap="gist_ncar")
    # plt.draw()
    # plt.show()

seg_mid[0][:,50].shape
np.insert(seg_mid[0][:,50][:-1],0,True).shape
np.flip(np.argwhere(np.logical_xor(np.insert(seg_mid[0][:,50][:-1],0,False),seg_mid[0][:,50])),0)

vectors = []
for img in (seg_bot+seg_mid+seg_top):
    plt.imshow(img, cmap="YlOrBr_r")
    plt.show()
    vectors.append(vectorize(img))

len(vectors)
