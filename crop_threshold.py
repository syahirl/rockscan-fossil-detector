import numpy as np      # import numpy
from PIL import Image   # and PIL image module

img = Image.open("rockscan.png")  # open the image
img_array = np.array(img)         # and convert it to a numpy array

cropped_array = img_array[128:128+256, 128:128+256]   # slice it to crop it

median = np.median(cropped_array)              # find the median
cropped_array[cropped_array >= median] = 255   # set values >= median to white
cropped_array[cropped_array < median] = 0      # set values < median to black

# write the file back out... done!
img2 = Image.fromarray(cropped_array)
img2.save("rockscancut2.png")
