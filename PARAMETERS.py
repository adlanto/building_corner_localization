# This file includes all Parameters to be changed for the project #
import numpy as np

# General Parameters
USE_CARLA = False
DURATION_PER_FRAME_MAIN_MS = 50
MONO_CAMERA_MODE = False

# Parameters for visualization
VISUALIZE_BUILDING_CORNERS = True
DEBUG_VISUALIZATION = False
VISUALIZE_HARRIS = False
VISUALIZE_HARRIS_CLUSTERS = False
VISUALIZE_HOUGH = False

# Camera Parameters
None

# Parameters for image preprocessing
RESIZED_FRAME_SIZE = (640, 480)
CROP_VALUE_FROM_TOP = 260 # 230 for CM
BLUR_FILTER_KERNEL_SIZE = 5
THRESHOLD_FILTER_VALUE = 90

# Parameters for finding building contours
HARRIS_NEIGHBOURHOOD_SIZE = 2
HARRIS_SOBEL_KERNEL_SIZE = 5
HARRIS_RELEVANCE_PARAM = 0.005
CANNY_FIRST_THRESHOLD = 50
CANNY_SECOND_THRESHOLD = 200
CANNY_SOBEL_KERNEL_SIZE = 3
MORPHOLOGY_KERNEL_VERTICAL = 30
MORPHOLOGY_KERNEL_HORIZONTAL = 30
POLYGON_APPROXIMATION_ACCURACY = 2
HOUGH_RHO = 1
HOUGH_THETA = np.pi/180
HOUGH_THRESHOLD = 40
HOUGH_MIN_LINE_LENGTH = 5
HOUGH_MAX_LINE_GAP = 20

# Parameters for validation of building corners
HOUGH_LINES_VERTICAL_THRESHOLD = 5
CLUSTER_HARRIS_HORIZONTAL_RELEVANCE = 1.5
CLUSTER_DISTANCE_THRESHOLD = 80
MIN_POINTS_PER_CLUSTER = 3
BUILDING_CORNERS_HARRIS_THRESHOLD = 10
HOUGH_HARRIS_LINES_DIST_THRESHOLD = 100

# Parameters for Stereocameras
f = 5 * 10 ** -3  # Brennweite
x = 1  # Abstand der beiden Kameras
p = 3.75 * 10 ** -5  # Pixelgröße

