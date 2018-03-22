###Slice.py
# Use to slice an image into vectors
# swag

#############CONSTANTS
IMAGE_SIZE=(256,256)

##################
import os
import sys

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
#print(sys.path)
#sys.path.append("Slicer\\")
import slice_lib as slib
import numpy as np
from PIL import Image
#import matplotlib
#%matplotlib qt5
#import matplotlib.pyplot as plt
import scipy.signal
from skimage import morphology as mp
from skimage import exposure

from mpl_toolkits.mplot3d import axes3d

IMAGE_FACTOR = (IMAGE_SIZE[0]*IMAGE_SIZE[1]) ** (1. / 4) / 4

gaussian = slib.gaussian_2d(IMAGE_FACTOR)

image_names = ["eiffel.jpg", "lisa.jpg", "fish.jpg"]
#image_names = ["Slicer\\eiffel.jpg", "Slicer\\lisa.jpg", "Slicer\\fish.jpg"]

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

    # plt.imshow(display_image, cmap="YlOrBr_r")
    # plt.show()
    # plt.imshow(display_layered ** .2 + 1000, cmap="gist_ncar")
    # plt.show()

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
# for img in (seg_bot+seg_mid+seg_top):
#     plt.imshow(img, cmap="YlOrBr_r")
#     plt.show()
#     #vectors.append(vectorize(img))


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
            going_left = not going_left
    return vector_list


def MultiContourSegment(segment):
    vector_list = []

#
# plt.imshow(seg_bot[0], cmap="YlOrBr_r")
# plt.show()


from skimage import measure
contours = measure.find_contours(seg_bot[0],.1)

contour = contours[1]
#print(contour)
#plt.plot(contour[:, 1], 256-contour[:, 0], linewidth=5)

import driver as drv
drv.print_vector(contour)

# for n, contour in enumerate(contours):
#     plt.plot(contour[:, 1], 256-contour[:, 0], linewidth=5)
#     print(n)
#     #print(n, contour)
# plt.show()
# plt.xlim([0,256])
# plt.ylim([0,256])
# plt.show()
#
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
# from matplotlib.figure import Figure
#
#
# #fig = Figure(figsize=(1.3+256.0/72.0,1.3+256.0/72.0))
# fig = Figure(figsize=(256.0/72.0,256.0/72.0), frameon=False)
# canvas = FigureCanvas(fig)
# ax = fig.gca() #fig.add_axes([0, 0, 256, 256])
# ax.axes.set_xlim(0,256)
# ax.axes.set_ylim(0,256)
#
# #ax.text(0.0,0.0,"Test", fontsize=45)
# #ax.plot()
# for n, contour in enumerate(contours):
#     ax.plot(contour[:, 1], 256-contour[:, 0], linewidth=5)
#
# #fig.patch.set_visible(False)
# ax.patch.set_visible(False)
# ax.axis('off')
# ax.spines['top'].set_visible(False)
# ax.spines['right'].set_visible(False)
# ax.spines['bottom'].set_visible(False)
# ax.spines['left'].set_visible(False)
# canvas.draw()       # draw the canvas, cache the renderer
#
#
#
# width, height = fig.get_size_inches() * fig.get_dpi()
#
# image = np.fromstring(canvas.tostring_rgb(), dtype='uint8').reshape(int(height), int(width), 3)
#
#
# #image = np.fromstring(canvas.tostring_rgb(), dtype='uint8').reshape(height, width, 3)
#
# # (373248/3)**.5
# # 373248/610
# # 610*610
# offset = int((image.shape[0]-256)/2)
#
#
# # image = image[:372100].reshape((610,610))
# plt.imshow(seg_bot[0])
# #plt.imshow(image[offset:-offset,offset:-offset], alpha=0.6)
# plt.imshow(image, alpha=0.6)
# plt.show()
