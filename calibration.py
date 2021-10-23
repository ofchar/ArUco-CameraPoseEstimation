import numpy as np
import cv2
import glob
import argparse
import os

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)


def calibrate(dirpath, image_format, square_size, width, height):
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(8,6,0)
    objp = np.zeros((height*width, 3), np.float32)
    objp[:, :2] = np.mgrid[0:width, 0:height].T.reshape(-1, 2)

    objp = objp * square_size

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.

    images = glob.glob(dirpath + '/*.' + image_format)

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, (width, height), None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

            # Draw and display the corners
            img = cv2.drawChessboardCorners(img, (width, height), corners2, ret)

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    return [ret, mtx, dist, rvecs, tvecs]

def save_coefficients(mtx, dist, path):
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_WRITE)

    cv_file.write("mtx", mtx)
    cv_file.write("dist", dist)

    cv_file.release()

def getArguments():
    parser = argparse.ArgumentParser(description='Camera calibration')
    parser.add_argument('--image_dir', type=str, default = "calibration_images", help='(optional) Path to directory with images')
    parser.add_argument('--image_format', type=str, default = "jpg",  help='(optional) Extension of images files')
    parser.add_argument('--square_size', type=float, default = 0.026, help='(optional) Chessboard square size, in meters')
    parser.add_argument('--width', type=int, default = 9, help='(optional) Chessboard width size')
    parser.add_argument('--height', type=int, default = 6, help='(optional) Chessboard height size')
    parser.add_argument('--save_file', type=str, default = "calibration", help='(optional) Path to file to save calibration matrices')

    return parser.parse_args()



def main():
    args = getArguments()

    ret, mtx, dist, rvecs, tvecs = calibrate(args.image_dir, args.image_format, args.square_size, args.width, args.height)
    save_coefficients(mtx, dist, args.save_file)


if __name__ == '__main__':
    main()