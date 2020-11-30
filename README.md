# Building Corner Localization
Localization of EGO vehicle by detection of building corners. Note that the project does not give the exact distances as no camera calibration was available.
The task of localization is usually divided into two steps. First, the more coarse GNSS localization, which can lack in accuracy due to multipath effects or for example in tunnels were no signal is avalaible. Hereby, other approaches are considered maninly based on the remaining sensors of a autonomously driving vehicle, namely cameras, lidars and radars. The detection of landmarks, in our case in the form of building corners is one approach for refining the coarse GNSS localization. The key idea behind using building corners is the comparably to other objects such as signs or special buildings low complexity to detect them. More in-depth approaches use Deep Convolutional Networks to detect the landmarks, an overview gives https://www.mdpi.com/2075-1702/7/2/25/pdf. 

## Table of contents
* [Overview](#Overview)
* [Requirements](#Requirements)
* [Installation](#Installation)
* [Usage](#Usage)
* [Contributors](#Contributors)


## Overview
The idead behind this work was to evaluate one algorithm of advanced driver assistance systems in a closed or open loop respectively. 

Due to difficulties in creating a closed loop with CarMaker, the main Simulation environment for the lecture, there is only an open loop available. 
For a demo see simulation_kempten.avi for results with the CarMaker environment.

[![Demonstration Video on a CarMaker model of the City of Kempten, Germany](https://github.com/adlanto/building_corner_localization/blob/master/images/sample_image.PNG)](https://github.com/adlanto/building_corner_localization/blob/master/simulation_kempten.avi)

The closed loop was realized with the integration of Carla Simulator - see https://carla.org/
However, the detection on Carla is not very good yet as the parameters were optimized for CarMaker.

![Sample image in the Carla environment.](https://github.com/adlanto/building_corner_localization/blob/master/images/sample_image_carla.jpg)


## Requirements
The complete system was running with
- Windows 10
- Python 3.7
- Anaconda 1.9.12
- OpenCV 4.1.0.25
- Carla 0.9.9 with Unreal Engine 4.24.3
- IPG CarMaker 8.1.1


## Installation
You can either run the system on a closed loop with Carla or on two Videos recorded for example in CarMaker or in a real environment. Consider to adapt the parameters.py if a different environment is used. 

Create a new conda environment based on the environment file:
```
$ conda env create -f environment.yml
```

If you want to use Carla, install following the documentation at https://carla.readthedocs.io/en/latest/ or follow the video https://www.youtube.com/watch?v=J1F32aVSYaU&ab_channel=sentdex


## Usage

Run in your Anaconda environment:
```
$ main.py
```

There are different settings that you may want to adapt to your simulation environment:
- USE_CARLA: Use the Carla simulation environment if installed (Please adapt the path of your installation in carla_inferface.py!)
- DURATION_PER_FRAME_MAIN_MS: Time for each frame to process
- MONO_CAMERA_MODE: For just detecting the building corners in a single frame
- CAMERA_FOCAL: Camera focal length (Currently an estimation, does strongly influence the distances)
- DISTANCE_BETWEEN_STEREO_CAMERAS: Distance between the stereo cameras
- CAMERA_FOV: Field of View of the cameras

Furthermore, there are different debugging options available:
- VISUALIZE_BUILDING_CORNERS: Output of the result during runtime
- DEBUG_VISUALIZATION: Show some important interim results
- VISUALIZE_HARRIS: Show the results of the Harris corner detection (This uses matplotlib, you have to manually jump to the next image)
- VISUALIZE_HARRIS_CLUSTERS: Show the clustering results (This uses matplotlib, you have to manually jump to the next image)
- VISUALIZE_HOUGH: Show the steps of the hough line detection


## Contributors
This was a project in the lecture modelling and simulation of advanced driver assistance systems @Kempten University of Applied Sciences.
It was developed by Tobias Langes (https://github.com/adlanto) and Volker Manz (https://github.com/maenzinger11).
