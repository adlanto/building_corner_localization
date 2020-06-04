import numpy as np
import PARAMETERS as PM
import cv2


def estimate_distances(building_corners_left, building_corners_right):
    #print('l =', building_corners_left)
    #print('r =', building_corners_right)

    # Zuordnung Kante zu Kamera 1 und Kamera 2
    map_lines = {}
    for l, l_lines in enumerate(building_corners_left):
        euclidean_distances = []
        for r_lines in building_corners_right:
            euclidean_distances.append(np.sqrt((l_lines[0, 0] - r_lines[0, 0])**2 + (l_lines[0, 2] - r_lines[0, 2])**2))
        map_lines[l] = np.argmin(euclidean_distances)
        #print(euclidean_distances)
    print(map_lines)

    distances = {}

    #Stereo-Kamera Distanzberechnung
    dis = []
    for ls in map_lines:
        stereo = cv2.StereoSGBM(numDisparities=16, blockSize=15)
        # stereo = cv2.StereoSGBM_create(minDisparity=0,
        #                                numDisparities=64,
        #                                blockSize=11)
        disparity = stereo.compute(l_lines, r_lines)
        dis.append(disparity)
    print(dis)


    return dis
