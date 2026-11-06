from PIL import Image
import numpy as np

# Note that my approach was to count the number of white pixels within
# a radius of five from each pixel, and if there are fewer than 3 of them,
# call the pixel 'fossil'. The value of '3' is chosen arbitrarily, and exists
# to allow for a little bit of noise in the image

# Custom functions - one to do distance between two points, and one to answer
# the 'is this pixel fossil' question


# calculate  distance between points (x1,y1) and (x2,y2) using Pythagoras
def distance(x1, y1, x2, y2):
    return np.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))


# returns True if point x,y has fewer than 3 white pixels within
# a distance of radius. im_array is the image array.
def is_fossil(x, y, im_array, radius):
    white_count = 0  # will count white pixels, start at 0

    # loop over all pixels in 11x11 pixel square containing the target pixel
    # as all pixels within 5 radius must be inside this square. This saves
    # wasting a lot of time looking at pixels that can't possible be close
    # enough for us to care about
    for x_index in range(x-radius, x+radius+1):
        for y_index in range(y-radius, y+radius+1):
            # check actual distance against radius
            if (distance(x_index, y_index, x, y)) <= radius \
                    and im_array[y_index, x_index] == 255:
                white_count += 1  # if pixel was white - add one to count
    if white_count < 3:  # allow a couple of whites, but not three
        return True
    else:
        return False


# main code starts here
image = np.array(Image.open("rockscancut.png"))  # read the image into array

centers_found = []  # will hold centers - as tuples (x,y)

# loops to loop over every pixel - we are skipping the ones within 5
# pixels of the edge (so look at indexes 5-250)
for x in range(5, 251):
    print(f"Working on column {x}")  # show user something is happening
    for y in range(5, 251):
        if is_fossil(x, y, image, 5):    # is this pixel at centre of a fossil?
            # if it is, add it to my list as a tuple of (x, y)
            centers_found.append((x, y))

# ugly print to confirm it's working
print("List of centres found:")
print(centers_found)  # print out the list

# and more visually useful - make an image to show positions

# take a copy of the existing image and zero it - this is simplest way to
# make a new image array that's definitely in the right format
center_image = image.copy()
center_image *= 0  # and zero it - multiply everything by 0 - so all black

for position in centers_found:                # for each detected centre
    center_image[position[1], position[0]] = 255  # set the pixel white

# and write it out
img_out = Image.fromarray(center_image)
img_out.save("centres.png")
