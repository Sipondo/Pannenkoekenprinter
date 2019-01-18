import numpy as np
from PIL import Image
#import matplotlib.pyplot as plt
import scipy.signal
from skimage import morphology as mp
from skimage import exposure

def gaussian_2d(sigma_mm, voxel_size = [1,1]):
    kernel = None
    x = np.linspace(-3*sigma_mm+.5, 3*sigma_mm+.5, (6*sigma_mm+.5)/voxel_size[0])
    y = np.linspace(-3*sigma_mm+.5, 3*sigma_mm+.5, (6*sigma_mm+.5)/voxel_size[1])
    kernel = np.zeros((int((6*sigma_mm+.5)/voxel_size[0]),int((6*sigma_mm+.5)/voxel_size[1])))
    constant = 1.0 / (2.0*np.pi*(sigma_mm*sigma_mm))

    for i in range(0,int(kernel.shape[0])):
        for j in range(0,int(kernel.shape[1])):
            kernel[i,j] = constant * np.exp(-1.0*(x[i]*x[i]+y[j]*y[j])/(2.0*sigma_mm*sigma_mm))
    return kernel, x, y

def segment_image(pic_array, gaussian, blurred, equalized, cwhite):
    ###Blur image with the specified gaussian kernel
    if(cwhite):
        mean = np.mean(pic_array)
        pic_array[pic_array>mean] = pic_array[pic_array>mean] - mean
    if(blurred):
        pic_convolved = scipy.signal.fftconvolve(pic_array, gaussian[0], mode='same')
    else:
        pic_convolved = pic_array
    if(equalized):
        pic_convolved = exposure.equalize_hist(pic_convolved)

    ###Segment middle layer
    mean = np.mean(pic_convolved) + np.std(pic_convolved)
    pic_layer1 = mp.dilation(pic_convolved>mean, mp.square(4))

    ###Segment top layer
    mean = np.mean(pic_convolved[pic_layer1==0]) + np.std(pic_convolved[pic_layer1==0])/2
    pic_layer2 = np.invert(mp.erosion(pic_convolved<mean, mp.square(4)))

    ###Merge layers
    final_picture = pic_layer1*2+pic_layer2

    ###Split layers into connected components
    conn_comps_layer0 = mp.label(final_picture<1, connectivity=1)
    conn_comps_layer1 = mp.label(final_picture==1, connectivity=1)
    conn_comps_layer2 = mp.label(final_picture>1, connectivity=1)

    ###Create labelled output image (print preview)
    layered_output_image = np.zeros(conn_comps_layer0.shape)

    ###Split segments into seperate entities for future slicing
    bottom_imgs = []
    middle_imgs = []
    top_imgs = []

    threshold = -1#conn_comps_layer0.shape[0]*conn_comps_layer0.shape[1]/64
    for i in range(0,np.max(conn_comps_layer0))[:1]:
        new_layer = (conn_comps_layer0==i)
        if np.sum(new_layer)>threshold:
            #new_layer = np.invert(new_layer)
            bottom_imgs.append(new_layer)
            layered_output_image = layered_output_image + new_layer*(1+i)

    #threshold = -1
    for i in range(0,np.max(conn_comps_layer1))[:1]:
        new_layer = (conn_comps_layer1==i)
        if np.sum(new_layer)>threshold:
            #new_layer = np.invert(new_layer)
            middle_imgs.append(new_layer)
            layered_output_image = layered_output_image + new_layer*(11+i)

    for i in range(0,np.max(conn_comps_layer2))[:1]:
        new_layer = (conn_comps_layer2==i)
        if np.sum(new_layer)>threshold:
            #new_layer = np.invert(new_layer)
            top_imgs.append(new_layer)
            layered_output_image = layered_output_image + new_layer*(21+i)

    ###Return all values
    return final_picture, layered_output_image, bottom_imgs, middle_imgs, top_imgs
