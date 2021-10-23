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