###Slice.py
# Use to slice an image into vectors
# swag

#############CONSTANTS
IMAGE_SIZE=(128,128)
##################


import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
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

gaussian = gaussian_2d(3)

picture = Image.open("eiffel.jpg").convert("L")
#picture = Image.open("fish.png").convert("L")
#picture = Image.open("lisa.jpg").convert("L")
#picture = Image.open("niek.jpg").convert("L")
#picture = Image.open("applelogo.jpg").convert("L")

picture = picture.resize(IMAGE_SIZE, Image.BICUBIC)

pic_array = np.array(picture)

#plt.plot(pic_array[:,:,0])
plt.imshow(pic_array, cmap="gray")
plt.show()

pic_convolved = scipy.signal.fftconvolve(pic_array, gaussian[0], mode='same')


mean = np.mean(pic_convolved)


pic_layer1 = mp.dilation(pic_convolved>mean, mp.square(4))

mean = np.mean(pic_convolved[pic_layer1==0])

pic_layer2 = np.invert(mp.erosion(pic_convolved<mean, mp.square(4)))

# plt.imshow(pic_layer1)
# plt.show()
# plt.imshow(pic_layer2)
# plt.show()

final_picture = pic_layer1*2+pic_layer2
plt.imshow(final_picture, cmap='gray')
plt.show()

conn_comps_layer0 = mp.label(final_picture<1, connectivity=1)
conn_comps_layer1 = mp.label(final_picture==1, connectivity=1)
conn_comps_layer2 = mp.label(final_picture>1, connectivity=1)

layered_output_image = conn_comps_layer0\
                     + conn_comps_layer1\
                     + conn_comps_layer2\
                     + (conn_comps_layer1>0)*10\
                     + (conn_comps_layer2>0)*20

plt.imshow(layered_output_image, cmap='gist_ncar')
plt.show()
#plt.imshow(conn_comps_layer0, cmap='gray')
# plt.imshow(conn_comps_layer0)
# plt.show()
# plt.imshow(conn_comps_layer1)
# plt.show()
# plt.imshow(conn_comps_layer2)
# plt.show()

bottom_imgs = []
middle_imgs = []
top_imgs = []

for i in range(np.max(conn_comps_layer0)):
    bottom_imgs.append(conn_comps_layer0==i)
for i in range(np.max(conn_comps_layer1)):
    middle_imgs.append(conn_comps_layer1==i)
for i in range(np.max(conn_comps_layer2)):
    top_imgs.append(conn_comps_layer2==i)

# for img in top_imgs[1:]:
#     print(np.sum(img))
#     if(np.sum(img)>IMAGE_SIZE[0]):
#         plt.imshow(img)
#         plt.show()
