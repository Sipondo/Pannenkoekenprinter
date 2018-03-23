import Slicer.slice_run as slicer
from PIL import Image

imgname = "images/radboud.png"
picture = Image.open(imgname).convert("L")
slicer.Slice_Image(picture, SQRSIZE=200, BLURRED=False, EQUALIZED=False, CWHITE=False, INVERTED=False, RETURN_IMG=False)
