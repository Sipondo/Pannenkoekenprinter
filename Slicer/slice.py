###Slice.py
# Use to slice an image into vectors
# swag

#############CONSTANTS
IMAGE_SIZE=(64,64)
##################


import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import scipy.signal
from skimage import morphology as mp

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

gaussian = gaussian_2d(3)

picture = Image.open("lisa.jpg").convert("L")
#picture = Image.open("fish.PNG").convert("L")
#picture = Image.open("eiffel.jpg").convert("L")
#picture = Image.open("applelogo.jpg").convert("L")

picture = picture.resize(IMAGE_SIZE, Image.BICUBIC)

pic_array = np.array(picture)

#plt.plot(pic_array[:,:,0])
plt.imshow(pic_array, cmap="gray")
plt.show()

pic_convolved = scipy.signal.fftconvolve(pic_array, gaussian[0], mode='same')

mean = np.mean(pic_convolved)
std = np.std(pic_convolved)

pic_layer1 = mp.dilation(pic_convolved>mean, mp.square(4))

mean = np.mean(pic_convolved[pic_layer1==0])
std = np.std(pic_convolved[pic_layer1==0])

pic_layer2 = np.invert(mp.erosion(pic_convolved<mean, mp.square(4)))

plt.imshow(pic_layer1)
plt.show()
plt.imshow(pic_layer2)
plt.show()

plt.imshow(pic_layer1*2+pic_layer2, cmap='gray')
plt.show()
