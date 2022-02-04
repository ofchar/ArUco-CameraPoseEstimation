# Camera position estimation based on ArUco markers
###### Mateusz Owczarek, 2021
-------
### General information
Project was designed to run on Windows and Linux machines, that have Python and OpenCV library installed. Moreover camera with it’s calibration files and dictionary of ArUco markers ids and their in-world position and orientation is required to correctly operate the application.

Please note that every marker must be orientated at 0°, 90°, 180° or 270° in regard to assumed world’s coordinate system axes. Moreover, it is worth noting that every measurement, both in input and in output is to be given in meters.

Project was tested on Windows 10 with Python 3.8.5.

-----
## Installation and use
### Installation
- Install Python3, together with Pip
- Download project files, and place in some directory
- Install required packages: `pip install imutils numpy opencv-contrib-python glob3`
- Prepare calibration and positions.txt files
- Run PositionEstimator.py

### Optional arguments
- `--type {type}` type of ArUco tags, defaults to "DICT_4x4_50"
- `--calibration {file}` path to camera calibration file, defaults to "calibration"
- `--size {size}` size - length of one side - of printed marker, defaults to 0.1
- `--positions {file}` path to file with markers poses, defaults to "positions.txt"
- `--cameraSource {int}` to provide camera source (if more then one are connected to the computer, defaults to 0.
# Camera position estimation based on ArUco markers

### General information
Simple application which allows to estimate position of the camera in some 3D space based on known position and orientation of the ArUco marker(s). 

Project was designed to run on Windows and Linux machines, that have Python and OpenCV library installed. Moreover camera with it’s calibration files and dictionary of ArUco markers ids and their in-world position and orientation is required to correctly operate the application.

Please note that every marker must be orientated at 0°, 90°, 180° or 270° in regard to assumed world’s coordinate system axes. Moreover, it is worth noting that every measurement, both in input and in output is to be given in meters.

Project was tested on Windows 10 with Python 3.8.5.

## Installation and use
### Installation
- Install Python3, together with Pip
- Download project files, and place in some directory
- Install required packages: `pip install imutils numpy opencv-contrib-python glob3`
- Prepare calibration and positions.txt files
- Run *PositionEstimator.py*, press `q` to exit.

### Camera calibration
Together with *PositionEstimator.py* the *calibration.py* is provided. It is simple script that from provided photos calculates camera matrix and distortion coefficients and save them to file, that can be later loaded in actual program. 

Before starting simple chessboard should be printed (default one is 6x9) and glued on to some rigid material. Then several photos of the board in different positions, rotations etc needs to be taken, and put into some directory. Then one can start the script, that can be customized with the following arguments:
- `image_dir {dir}` path to directory with images, defaults to "calibration_images”
- `image_format {format}` extension of the provided images, defaults to “jpg”
- `square_size {size}` size of chessboard square, in meters, defaults to 0.026
- `-width {width}` chessboard width, defaults to 9
- `height {height}` chessboard height, defaults to 6
- `save_file {path}` path to file to which calibration data should be saved, defaults to “calibration”

Main calibration logic is taken from [OpenCV docs](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html).

### Optional arguments
- `--type {type}` type of ArUco tags, defaults to "DICT_4x4_50"
- `--calibration {file}` path to camera calibration file, defaults to "calibration"
- `--size {size}` size - length of one side - of printed marker, defaults to 0.1
- `--positions {file}` path to file with markers poses, defaults to "positions.txt"
- `--cameraSource {int}` to provide camera source (if more then one are connected to the computer, defaults to 0.

<br>

###### Mateusz Owczarek, 2021
