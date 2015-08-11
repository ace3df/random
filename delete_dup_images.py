"""
A super simple script to delete dup images by comparing pixel hash.
"""

from PIL import Image
import time
import os

def dhash(image):
	image = image.convert('L').resize(
		(8 + 1, 8),
		Image.ANTIALIAS,
	)

	pixels = list(image.getdata())
	difference = []
	for row in xrange(8):
		for col in xrange(8):
			pixel_left = image.getpixel(col, row)
			pixel_right = image.getpixel(col + 1, row)
			difference.append(pixel_left > pixel_right)

	decimal_value = 0
	hex_string = []
	for index, value in enumerate(difference):
		if value:
			decimal_value += 2**(index % 8)
		if (index % 8) == 7:
			hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
			decimal_value = 0	
	return ''.join(hex_string)

image_data = {}

while True:
	print "Folder to check:"
	path = raw_input()
	if os.path.isdir(path):
		break
	else:
		print ""
		print "Folder doesn't exsit!"
		print path
		print "---------------------"

removed_int = 0

onlyfiles = [ f for f in os.listdir(path) if os.path.isfile(os.path.join(path,f)) ]
print "Checking: %s files!" % (len(onlyfiles))
time.sleep(5)

for image_file in onlyfiles:
	print image_file
	image_file = os.path.join(path, image_file)
	image_path = Image.open(image_file)
	data_gest = dhash(image_path)
	if data_gest in image_data:
		print "Deleting: " + image_file
		os.remove(image_file)
		removed_int += 1
	else:
		image_data[data_gest] = image_file

print "Deleted: %s file(s)!" % (str(removed_int))
raw_input("Press ENTER to close!")
