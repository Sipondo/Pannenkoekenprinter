import Slicer.slice_run as slicer
from PIL import Image

imgname = "images/beer.jpg"
picture = Image.open(imgname).convert("L")
slicer.Slice_Image(picture, SQRSIZE=750, BLURRED=False, EQUALIZED=False, CWHITE=True, INVERTED=True, RETURN_IMG=False)
