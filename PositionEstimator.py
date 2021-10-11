# import the necessary packages
from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import sys
import numpy as np
import math


# Loads camera matrix and distortion coefficients.
# FILE_STORAGE_READ
cv_file = cv2.FileStorage("C:\\Users\\mat28\\Desktop\\calibration", cv2.FILE_STORAGE_READ)

# note we also have to specify the type to retrieve other wise we only get a
# FileNode object back instead of a matrix
mtx = cv_file.getNode("K").mat()
dist = cv_file.getNode("D").mat()

cv_file.release()


# define names of each possible ArUco tag OpenCV supports
ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

# adjust dictionary parameters for better marker detection
parameters = cv2.aruco.DetectorParameters_create()
parameters.cornerRefinementMethod = 3
parameters.errorCorrectionRate = 0.2

arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_4X4_50"])
arucoParams = cv2.aruco.DetectorParameters_create()



markerDict = {	1: [2.10,1.85,0.4],
				2: [4,5,6]
			}





# initialize the video stream and allow the camera sensor to warm up
vs = VideoStream(src=0).start()
time.sleep(2.0)



# loop over the frames from the video stream
while True:
	frame = vs.read()
	frame = imutils.resize(frame, width=1920)

	# detect ArUco markers in the input frame
	(corners, ids, rejected) = cv2.aruco.detectMarkers(frame,
		arucoDict, parameters=arucoParams)

	# verify *at least* one ArUco marker was detected
	if len(corners) > 0:
		# flatten the ArUco IDs list
		ids = ids.flatten()

		for (markerCorner, markerID) in zip(corners, ids):
			rotation_vectors, translation_vectors, _objPoints = cv2.aruco.estimatePoseSingleMarkers(markerCorner, 0.1, mtx, dist)

			frame = cv2.aruco.drawAxis(frame, mtx, dist, rotation_vectors, translation_vectors, 0.1)

			(rotation_vectors - translation_vectors).any()

			# print(translation_vectors[0][0])
			# print(markerDict[markerID])



			dst, jacobian = cv2.Rodrigues(rotation_vectors[0][0])

			dst = cv2.transpose(dst)

			cameraRotationVector = cv2.Rodrigues(dst)

			cameraTranslationVector = cv2.transpose(-dst) @ translation_vectors[0][0]

			# print(cameraTranslationVector)

			x = markerDict[markerID][0] + cameraTranslationVector[0]
			y = markerDict[markerID][1] + cameraTranslationVector[1]
			z = markerDict[markerID][2] + cameraTranslationVector[2]
			print(x, y, z, sep=" ")

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	time.sleep(0.1)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()