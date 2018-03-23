import Slicer.slice_run as slicer
from PIL import Image

imgname = "images/eiffel.jpg"
picture = Image.open(imgname).convert("L")
slicer.Slice_Image(picture)
