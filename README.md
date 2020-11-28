# Building Corner Localization
Localization of EGO vehicle by detection of building corners. Note that the project does not give the exact distances as no camera calibration was available.

[![Demonstration Video on a CarMaker model of the City of Kempten, Germany](https://github.com/adlanto/building_corner_localization/blob/master/images/sample_image.PNG)](https://github.com/adlanto/building_corner_localization/blob/master/simulation_kempten.avi)

This was a project in the lecture modelling and simulation of advanced driver assistance systems. 
The focus was to evaluate one algorithm in a closed or open loop respectively. 

The closed loop was realized with the integration of Carla Simulator - see https://carla.org/

Due to difficulties in creating a closed loop with CarMaker, the main Simulation environment for the lecture, there is only an open loop available. 


# Requirements
The complete system was running with
- Windows 10
- Python 3.7
- Anaconda 1.9.12
- OpenCV 4.1.0.25
- Carla 0.9.9 with Unreal Engine 4.24.3
- IPG CarMaker 8.1.1
