from PIL import Image
import numpy as np


# calculate  distance between points (x1,y1) and (x2,y2) using Pythagoras
def distance(x1, y1, x2, y2):
    return np.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))


# returns True if ponit x,y has fewer than 3 white pixels within
# a distance of radius. im_array is the image array.
def is_fossil(x, y, im_array, radius):
    white_count = 0  # will count white pixels, start at 0

    # loop over all pixels in square containing the circle
    # saves a lot of time - no point checking pixels outside that
    for x_index in range(x-radius, x+radius+1):
        for y_index in range(y-radius, y+radius+1):
            # check actual distance against radius
            if (distance(x_index, y_index, x, y)) <= radius \
                    and im_array[y_index, x_index] == 255:
                white_count += 1  # if pixel was white - add one to count
    if white_count < 1:  # allow a couple of whites, but not three
        return True
    else:
        return False


# are two coordinates (tuples) next to each other?
# c1, c2 are the tuples
# diagonal adjacency is allowed
# used in the clustering analysis
def adjacent(c1, c2):
    if abs(c1[0]-c2[0]) > 1:    # check x distance. More than 1?
        return False
    elif abs(c1[1]-c2[1]) > 1:  # check y distance. More than 1?
        return False
    else:                   # x and y distance both 1 or 0 ...
        return True         # ... so adjacent, return True


# clustering function. Runs through the whole list of clusters.
# for each one - compares all coords in it with each of the
# other clusters (i.e. with each coord in that list)
# If it finds any adjacent pairs - they are the same cluster.
#   - remove second cluster from cluster list, add it to the first cluster
#   - return True - to restart the entire process
# If no clusters were matched:
#   - clustering process is done, return False
def recluster():
    global clusterslist  # the global list (elements are lists of coord tuples)
    for this_cluster in range(len(clusterslist)-1):
        # loop over indexes of all clusters except the last one
        # skip last because we are going to compare each to all clusters
        # further on in the list - which makes no sense for last one!
        for compare_cluster in range(this_cluster+1, len(clusterslist)):
            # for each cluster, look at each cluster later in list
            # for each pair (entries in clusterlist)
            for other_coord in clusterslist[compare_cluster]:
                for this_coord in clusterslist[this_cluster]:
                    # two nested loops to look at all coords in both
                    # clusterlist entries
                    if adjacent(this_coord, other_coord):
                        # If ANY 2 entries are adjacent in the two clusters
                        # then clusters are adjacent. At this point we merge
                        # the two clusters and stop.
                        # Have to stop as it's a bad idea to modify a list
                        # while iterating over it

                        # this line removes the list at [j] from the list,
                        #  and adds it's elements to the list at [i]
                        clusterslist[this_cluster] +=\
                            clusterslist.pop(compare_cluster)

                        # and get out of the function, returning True
                        # which means 'carry on'
                        return True
    # if we get here, we've not found ANY cluster adjacency. We are done
    # return false so the program can finish
    return False


# main code starts here

image = np.array(Image.open("rockscancut.png"))  # read the image into array im

circleslist = []    # empty list for centres, will be tuples of (x,y)

# loops to loop over every pixel - we are skipping the ones within 5
# pixels of the edge (so look at indexes 5-250)
for x in range(5, 251):
    print(f"Working on column {x}")      # show user something is happening
    for y in range(5, 251):
        if is_fossil(x, y, image, 5):    # is this pixel at centre of a fossil?
            circleslist.append((x, y))   # if it is, add it to my list

print("List of centres found:")
print(circleslist)                      # print out the list

# and more visually useful - make an image to show positions
newimage_array = image.copy()  # take existing array (it's in correct format)
newimage_array *= 0  # and zero it - multiply everything by 0 - so all black

for position in circleslist:                # for each detected centre
    newimage_array[position[1], position[0]] = 255  # set the pixel white

# ... and write out the image

# and write it out
img_out = Image.fromarray(newimage_array)
img_out.save("centres.png")


# set up a list of clusters. This will be a list where each element
# is a list of coordinate-tuples
clusterslist = []

# initially we want each element as a single element list with one
# coordinate tuple - copied from circleslist
for coords in circleslist:
    clusterslist.append([coords])

# Repeatedly call the recluster function to do a clustering-pass
# on this new list. It will return False when it can't do any more
restart = True
while restart:
    restart = recluster()

# Done - each element in clusterlist should now be a list of coordinates within
# one cluster

# Finally - find centres of these clusters by taking mean position
# mean positions will go into a new list of coordinate tuples
meanslist = []

for cluster in clusterslist:   # for each cluster
    total_x = 0
    total_y = 0
    for coord in cluster:      # for each coordinate in that cluster
        total_x += coord[0]
        total_y += coord[1]     # total up the x and y positions

    # then to work out mean, just divide by number of entries
    # I want integer positions, so round to ints with int() function
    # put these into a tuple, and append it to my list of means
    meanslist.append((int(total_x/len(cluster)),
                      int(total_y/len(cluster))))

print("Final mean cluster position list:")
print(meanslist)    # output it as coordinate list

# Make and write image - same code as before!
newimage_array = image.copy()
newimage_array *= 0

for position in meanslist:
    newimage_array[position[1], position[0]] = 255

img_out = Image.fromarray(newimage_array)
img_out.save("centres_declustered.png")
