import Slicer.slice_run as slicer
from PIL import Image

imgname = "images/thalia.png"
picture = Image.open(imgname).convert("L")
slicer.Slice_Image(picture, SQRSIZE=400, BLURRED=True, EQUALIZED=False,\
 CWHITE=False, INVERTED=False, RETURN_IMG=False, SINGLE=False,\
  BOT=True, MID=True, TOP=True)
#
# import matplotlib.pyplot as plt
# # #
# imgname = "images/eiffeltower.png"
# picture = Image.open(imgname).convert("L")
# #
# plt.imshow(Image.open(imgname))
# plt.show()
# #
# slicer.Slice_Image(picture, SQRSIZE=500, BLURRED=True, EQUALIZED=False,\
#  CWHITE=False, INVERTED=False, RETURN_IMG=False, SINGLE=True,\
#   BOT=False, MID=True, TOP=False)
#
# imgname = "images/rtilted.jpg"
# picture = Image.open(imgname).convert("L")
# slicer.Slice_Image(picture, SQRSIZE=500, BLURRED=True, EQUALIZED=False,\
#  CWHITE=True, INVERTED=False, RETURN_IMG=False, SINGLE=True,\
#   BOT=True, MID=False, TOP=False)

# imgname = "images/rcenter.jpg"
# picture = Image.open(imgname).convert("L")
# slicer.Slice_Image(picture, SQRSIZE=500, BLURRED=True, EQUALIZED=False,\
#  CWHITE=False, INVERTED=False, RETURN_IMG=False, SINGLE=True,\
#   BOT=True, MID=False, TOP=False)
#
# imgname = "images/derpyheart_2.png"
# picture = Image.open(imgname).convert("L")
# slicer.Slice_Image(picture, SQRSIZE=500, BLURRED=False, EQUALIZED=False, CWHITE=True, INVERTED=False, RETURN_IMG=False, SINGLE=True, BOT=True, MID=False, TOP=False)

#
# imgname = "images/radboud.png"
# picture = Image.open(imgname).convert("L")
# slicer.Slice_Image(picture, SQRSIZE=110, BLURRED=False, EQUALIZED=False, CWHITE=False, INVERTED=False, RETURN_IMG=False, SINGLE=True)
