###Slice.py
# Use to slice an image into vectors
# swag

import os
import sys

# file_dir = os.path.dirname(__file__)
# sys.path.append(file_dir)
import Slicer.slice_lib as slib
import numpy as np
from PIL import Image
import scipy.signal
from skimage import morphology as mp
from skimage import exposure
from skimage import measure

import os
RUNNING_LOCALLY = os.path.isfile('Slicer/no_print')

def RapidContour(segment, BATTER_SIZE):
    vector_list = [0]
    vector_output = []
    while vector_list:
        vector_list = []
        segment = mp.dilation(segment, mp.disk(BATTER_SIZE))
        vector_list = measure.find_contours(segment,.1)
        vector_output.extend(vector_list)
    return vector_output

def Slice_Image(picture, SQRSIZE=500, BLURRED=True, EQUALIZED=True, CWHITE=False, INVERTED=False, RETURN_IMG=False):
    RUNNING_LOCALLY = os.path.isfile('Slicer/no_print')
    if RETURN_IMG:
        RUNNING_LOCALLY = True
    #############CONSTANTS
    #SQRSIZE = 500
    IMAGE_SIZE=(SQRSIZE,SQRSIZE)
    BATTER_SIZE=SQRSIZE/30
    IMAGE_FACTOR = (IMAGE_SIZE[0]*IMAGE_SIZE[1]) ** (1. / 4) / 4
    #BLURRED = True
    #EQUALIZED = True
    #IMAGE_FACTOR = 1
    ##################

    gaussian = slib.gaussian_2d(IMAGE_FACTOR)

    picture = picture.resize(IMAGE_SIZE, Image.BICUBIC)
    pic_array = np.array(picture)

    if INVERTED:
        display_image, display_layered,\
         seg_top, seg_mid, seg_bot = slib.segment_image(pic_array, gaussian, BLURRED, EQUALIZED, CWHITE)
    else:
        display_image, display_layered,\
         seg_bot, seg_mid, seg_top = slib.segment_image(pic_array, gaussian, BLURRED, EQUALIZED, CWHITE)

    if RUNNING_LOCALLY:
        import matplotlib.pyplot as plt
        plt.axis('equal')
    else:
        import Slicer.driver as drv

    for segment in seg_bot[:1]:
        print("slice_segment_bot")
        for vector in RapidContour(segment, BATTER_SIZE):
            if RUNNING_LOCALLY:
                plt.plot(vector[:, 1], 256-vector[:, 0], linewidth=5, color='saddlebrown')
            else:
                drv.print_vector(vector/(SQRSIZE/450))

    for segment in seg_mid[:1]:
        print("slice_segment_mid")
        for vector in RapidContour(segment, BATTER_SIZE):#measure.find_contours(segment,.1):
            if RUNNING_LOCALLY:
                plt.plot(vector[:, 1], 256-vector[:, 0], linewidth=5, color='goldenrod')
            else:
                drv.print_vector(vector/(SQRSIZE/450))

    for segment in seg_top[:1]:
        print("slice_segment_top")
        for vector in RapidContour(segment, BATTER_SIZE):#measure.find_contours(segment,.1):
            if RUNNING_LOCALLY:
                plt.plot(vector[:, 1], 256-vector[:, 0], linewidth=5, color='moccasin')
            else:
                drv.print_vector(vector/(SQRSIZE/450))
    if RETURN_IMG:
        plt.axis("off")
        plt.savefig('fig.png', bbox_inches='tight', pad_inches = 0)
    else:
        if RUNNING_LOCALLY:
            plt.show()
