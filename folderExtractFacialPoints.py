# This file contains the implementation to extract facial features from an image
#
# Author: Michael L. Smith
# 
# Many methods and implementation taken from:
# https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/ 

from imutils import face_utils
import numpy as np
import argparse
import imutils
import cv2
import dlib
import os
import pandas as pd 
import re

def rect_to_bb(rect):
	# take a bounding predicted by dlib and convert it
	# to the format (x, y, w, h) as we would normally do
	# with OpenCV
	x = rect.left()
	y = rect.top()
	w = rect.right() - x
	h = rect.bottom() - y
 
	# return a tuple of (x, y, w, h)
	return (x, y, w, h)

def shape_to_np(shape, dtype="int"):
	# initialize the list of (x, y)-coordinates
	coords = np.zeros((68, 2), dtype=dtype)
 
	# loop over the 68 facial landmarks and convert them
	# to a 2-tuple of (x, y)-coordinates
	for i in range(0, 68):
		coords[i] = (shape.part(i).x, shape.part(i).y)
 
	# return the list of (x, y)-coordinates
	return coords


def draw_bounding_box_and_points(image, rect, face_num, shape):

		# convert dlib's rectangle to a OpenCV-style bounding box
		# [i.e., (x, y, w, h)], then draw the face bounding box
		(x, y, w, h) = face_utils.rect_to_bb(rect)
		cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
	 
		# show the face number
		cv2.putText(image, "Face #{}".format(face_num + 1), (x - 10, y - 10),
			cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
	 
		# loop over the (x, y)-coordinates for the facial landmarks
		# and draw them on the image
		for (x, y) in shape:
			cv2.circle(image, (x, y), 1, (0, 0, 255), -1)


def ret_facial_points(detector, predictor, image):

	# load the input image and convert it to grayscale
	image = cv2.imread(image)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
 
	# detect faces in the grayscale image
	rects = detector(gray, 1)

	# there will only ever be one face in the image, etc

	if len(rects) == 0:
		X = np.asarray(['X'] * 68).reshape((68,1))
		Y = np.asarray(['Y'] * 68).reshape((68,1))
		return np.hstack((X, Y))


	for (i, rect) in enumerate(rects):
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		return shape
	 
	 	# uncomment to draw box and points
		#draw_bounding_box_and_points(image, rect, i, shape)

	# uncomment to show image
	# show the output image with the face detections + facial landmarks
	# cv2.imshow("Output", image)
	# cv2.waitKey(0)


def sorted_nicely(l): 
    """ Sort the given iterable in the way that humans expect.""" 
    convert = lambda text: int(text) if text.isdigit() else text 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

def main(args):
	detector = dlib.get_frontal_face_detector()
	predictor = dlib.shape_predictor(args["shape_predictor"])

	facial_matrix = []

	count = 0
	for filename in sorted_nicely(os.listdir(args["folder"])):
		image = os.path.join(args["folder"], filename)
		if image.endswith('.DS_Store'): continue
		frame_facial_pts = ret_facial_points(detector, predictor, image)
		if facial_matrix == []:
			facial_matrix = frame_facial_pts
		else:
			facial_matrix = np.hstack((facial_matrix, frame_facial_pts))
		print "Working on Image #{}".format(count)
		count += 1

	#print facial_matrix.shape

	df = pd.DataFrame(facial_matrix)
	df.to_csv(args["folder"][:-12]+'.csv', index=False, header=False)

	#np.savetxt('np.csv', args["folder"][:-12]+'.csv', facial_matrix, delimiter=',')


if __name__ == "__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-p", "--shape-predictor", required=True,
		help="path to facial landmark predictor")
	ap.add_argument("-f", "--folder", required=True,
		help="path to folder containing images")
	args = vars(ap.parse_args())

	main(args)




