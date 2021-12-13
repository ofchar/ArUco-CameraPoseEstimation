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

# define marker class, to hold information about marker position
# and orientation in regard to world's coordinate system
class Marker:
	def __init__(self, position_x, position_y, position_z, axis_x, axis_y, axis_z):
		self.position_x = position_x
		self.position_y = position_y
		self.position_z = position_z
		self.axis_x = axis_x
		self.axis_y = axis_y
		self.axis_z = axis_z



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
	parser.add_argument('-c', "--calibration", type = str, default = "calibration", help = '(optional) Path to camera calibration file')
	parser.add_argument('-s', "--size", type = float, default = 0.1, help = '(optional) Size of the markers in meters')
	parser.add_argument('-p', "--positions", type = str, default = "positions.txt", help = '(optional) Path to file with markers positions')
	parser.add_argument('-cs', "--cameraSource", type = int, default = 0, help = '(optional) Integer representating camera source')

	return parser.parse_args()

def loadMarkersPositions(path):
	markerDict = {}

	with open(path) as f:
		for line in f:
			if line[0] == '#':
				continue

			(key, pos, ax) = line.split()
			positions =  list(map(float, pos.split(',')))
			axes = list(map(int, ax.split(',')))

			markerDict[int(key)] = Marker(positions[0], positions[1], positions[2],
											axes[0], axes[1], axes[2])

	return markerDict

def doMagic(mtx, dist, dictionary, params, markerSize, markerDict, camSource):
	videoStream = VideoStream(src = camSource).start()
	time.sleep(1.0)

	while True:
		frame = videoStream.read()
		frame = imutils.resize(frame, width = frameWidth)

		corners, ids, _ = cv2.aruco.detectMarkers(frame, dictionary, parameters = params)

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

				dst, _ = cv2.Rodrigues(rvec[0][0])

				cameraTranslationVector = cv2.transpose(-dst) @ tvec[0][0]

				try:
					if markerDict[id].axis_x > 0:
						shiftX = markerDict[id].position_x + cameraTranslationVector[markerDict[id].axis_x - 1]
					else:
						shiftX = markerDict[id].position_x - cameraTranslationVector[-(markerDict[id].axis_x) - 1]

					if markerDict[id].axis_y > 0:
						shiftY = markerDict[id].position_y + cameraTranslationVector[markerDict[id].axis_y - 1]
					else:
						shiftY = markerDict[id].position_y - cameraTranslationVector[-(markerDict[id].axis_y) - 1]

					if markerDict[id].axis_z > 0:
						shiftZ = markerDict[id].position_z + cameraTranslationVector[markerDict[id].axis_z - 1]
					else:
						shiftZ = markerDict[id].position_z - cameraTranslationVector[-(markerDict[id].axis_z) - 1]

					x = x + shiftX
					y = y + shiftY
					z = z + shiftZ

					count = count + 1
				except KeyError:
					pass

			if count > 0:
				print(x / count, y / count, z / count, sep = " ")
				print()


		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		if key == ord("q"):
			break

	cv2.destroyAllWindows()
	videoStream.stop()


def main():
	args = getArguments()

    # Load camera calibration.
	checkFileExistence(args.calibration)
	mtx, dist = loadCalibrationData(args.calibration)


	# Load marker's positions
	checkFileExistence(args.positions)
	markerDict = loadMarkersPositions(args.positions)


	# Prepare aruco dictionary
	checkArucoDictionaryExistence(args.type)
	dictionary = cv2.aruco.Dictionary_get(ARUCO_DICT[args.type])


	# Prepare detector params
	params = cv2.aruco.DetectorParameters_create()


	doMagic(mtx, dist, dictionary, params, args.size, markerDict, args.cameraSource)

if __name__ == "__main__":
	main()