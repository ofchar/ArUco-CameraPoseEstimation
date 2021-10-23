from imutils.video import VideoStream
import imutils
import time
import cv2
import numpy as np
import os
import argparse
import sys

frameWidth=1280

# define names of ArUco tags supported by OpenCV.
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

# define all known tags, together with their x, y, z positions.
markerDict = {}



def checkFileExistence(path):
	exists = os.path.exists(path)

	if not exists:
		sys.exit("File at path: " + path + " does not exist :(")

def scaleCameraMatrix(mtx, newWidth, calibWidth=1920):
	scale = newWidth / calibWidth

	return mtx * scale

# Load camera matrix and distortion coefficients from file specified in path.
def loadCalibrationData(path):
	calibrationFile = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

	mtx = calibrationFile.getNode("mtx").mat()
	dist = calibrationFile.getNode("dist").mat()

	calibrationFile.release()

	mtx = scaleCameraMatrix(mtx, frameWidth)

	return mtx, dist

def checkArucoDictionaryExistence(type):
	if not type in ARUCO_DICT:
		sys.exit("Type " + type + " is not supported. Sorry :(")

def getArguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--type", type = str, default = "DICT_4X4_50", help = "(optional) Type of ArUco tags")
	parser.add_argument('-c', "--calibration", type = str, default = "calibration", help='(optional) Path to camera calibration file')
	parser.add_argument('-s', "--size", type = float, default = 0.1, help='(optional) Size of the markers in meters')
	parser.add_argument('-p', "--positions", type = str, default = "positions.txt", help='(optional) Path to file with markers positions')

	return parser.parse_args()

def loadMarkersPositions(path):
	with open(path) as f:
		for line in f:
			(key, val) = line.split()
			a_list = val.split(',')
			map_object = map(float, a_list)

			list_of_integers = list(map_object)
			markerDict[int(key)] = list_of_integers



def doMagic(mtx, dist, dictionary, params, markerSize):
	# Initialize videoStream
	videoStream = VideoStream(src=0).start()
	time.sleep(1.0)

	while True:
		frame = videoStream.read()
		frame = imutils.resize(frame, width=frameWidth)

		corners, ids, _ = cv2.aruco.detectMarkers(frame, dictionary, parameters=params)

		x = 0
		y = 0
		z = 0
		count = 0

		# if any markers have been detected
		if len(corners) > 0:
			ids = ids.flatten()

			for (corner, id) in zip(corners, ids):
				rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corner, markerSize, mtx, dist)

				frame = cv2.aruco.drawAxis(frame, mtx, dist, rvec, tvec, markerSize)

				(rvec - tvec).any()


				dst, _ = cv2.Rodrigues(rvec[0][0])

				cameraTranslationVector = cv2.transpose(-dst) @ tvec[0][0]

				try:
					x = x + markerDict[id][0] + cameraTranslationVector[2]
					y = y + markerDict[id][1] + cameraTranslationVector[0]
					z = z + markerDict[id][2] + cameraTranslationVector[1]

					print(id, markerDict[id][0] + cameraTranslationVector[0], markerDict[id][1] + cameraTranslationVector[1], markerDict[id][2] + cameraTranslationVector[2], sep = " ")
					count = count + 1
				except KeyError:
					pass

			if count > 0:
				print()
				print(x / count, y / count, z / count, sep = " ")
				print()
				print()


		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		if key == ord("q"):
			break

	cv2.destroyAllWindows()
	videoStream.stop()


def main():
	args = getArguments()
	# Determine path to camera calibration file.
	calibrationPath = args.calibration if args.calibration[0] == '\\' else os.getcwd() + '\\' + args.calibration

    # Load camera calibration.
	checkFileExistence(calibrationPath)
	mtx, dist = loadCalibrationData(calibrationPath)

	# Prepare aruco dictionary
	checkArucoDictionaryExistence(args.type)
	dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[args.type])

	# Prepare detector params
	params = cv2.aruco.DetectorParameters_create()
	params.cornerRefinementMethod = 3
	params.errorCorrectionRate = 0.2

	# Determine path to marker's positions file.
	positionsFile = args.positions if args.positions[0] == '\\' else os.getcwd() + '\\' + args.positions

	# Load marker's positions
	loadMarkersPositions(args.positions)

	doMagic(mtx, dist, dictionary, params, args.size)

if __name__ == "__main__":
	main()