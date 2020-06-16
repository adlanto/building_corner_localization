import numpy as np
import PARAMETERS as PM
import cv2
import statistics

matched_arrays_x_z = []
matched_array = []
matched_array_x_z = []


def median(x_array, z_array):

    matched_arrays_x_z.append([x_array, z_array])
    print('matched', matched_arrays_x_z)

    if x_array is not []:
        print('x_array= ', x_array)
        #print('z_array', z_array)
    #     # Match x values from current array to points of arrays before
    #     # Iterate over all array x values


        for i, x_new in enumerate(x_array):
            #print('x_new= ', x_new)

            for matched_points_array in matched_arrays_x_z:
                if matched_points_array is not []:
                    x_old = matched_points_array[0][0]
                    # print('x_old= ', x_old)
                    if x_old - 1 <= x_new <= x_old + 1:
                        point = [x_new, z_array[i]]
                        #print('1 point', point)
                        matched_array.append(point)
                        #print('1 matched_points_array', matched_array)
        # matched_array_x_z.append(matched_array)
        #print('2 matched_array_x_z', matched_array_x_z)


        median_z_array = []
        median_x_array = []
        x_value = []
        z_value = []
        for points_matched_array in matched_array_x_z:
            #print('points_matched_array', points_matched_array)
            if len(points_matched_array) >= 5:
                for j, x_values in enumerate(points_matched_array):
                    x_value.append(x_values[0])
                    #print('x_value', x_value)
                    median_x = statistics.median_grouped(x_value)
                #print('median_x', median_x)
                median_x_array.append(median_x)
                #print('median_x_array', median_x_array)

                # x_values = points_matched_array[0][:]
                # print('x_values', x_values)
                # x_median = cv2.medianBlur(x_values, 3)

                for k, z_values in enumerate(points_matched_array[1]):
                    z_value.append(z_values)
                    median_z = statistics.median_grouped(z_value)
                median_z_array.append(median_z)
                #print('median_z_array', median_z_array)

                # z_values = points_matched_array[:, 1]
                # z_median = cv2.medianBlur(z_values, 3)
                # median_z_array.append(z_median)

    return median_x_array, median_z_array


def estimate_distances(frame_left, frame_right, building_corners_left, building_corners_right):

    gray_left_frame = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
    gray_right_frame = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

    # Assertion of lines in left to lines in right Camera
    map_lines = {}
    for i, l_lines in enumerate(building_corners_left):
        euclidean_distances = []
        for r_lines in building_corners_right:
            euclidean_distances.append(np.sqrt((l_lines[0, 0] - r_lines[0, 0])**2 + (l_lines[0, 2] - r_lines[0, 2])**2))
        if np.amin(euclidean_distances) < PM.MAXIMAL_DISTANCE_CORRESPONDING_LINES:
            map_lines[i] = np.argmin(euclidean_distances)
        #print(euclidean_distances)
    # print(map_lines)

    # # Calculate disparity between images
    # window_size = 3
    # min_disp = 16
    # num_disp = 112-min_disp
    # stereo = cv2.StereoSGBM_create(minDisparity=min_disp, numDisparities=num_disp, blockSize=16, P1=8*3*window_size**2,
    #                                P2=32*3*window_size**2, disp12MaxDiff=1, uniquenessRatio=10, speckleWindowSize=100,
    #                                speckleRange=32)
    # disp = stereo.compute(gray_left_frame, gray_right_frame).astype(np.float32) / 16.0
    #
    # h, w = gray_left_frame.shape[:2]
    # PM.CAMERA_FOCAL = 0.8 * w  # guess for focal length
    # Q = np.float32([[1, 0, 0, -0.5 * w],
    #                 [0, -1, 0, 0.5 * h],  # turn points 180 deg around x-axis,
    #                 [0, 0, 0, -PM.CAMERA_FOCAL],  # so that y-axis looks up
    #                 [0, 0, 1, 0]])
    # points = cv2.reprojectImageTo3D(disp, Q)
    # colors = cv2.cvtColor(gray_left_frame, cv2.COLOR_BGR2RGB)
    # mask = disp > disp.min()
    # out_points = points[mask]
    # print(out_points)
    #
    # cv2.imshow("disparity", (disp-min_disp)/num_disp)

    # Crate empty lists for x and y values
    x_array = []
    z_array = []

    # Iterate over all building corners and find correspondencies
    for left_line_index, right_line_index in zip(map_lines.keys(), map_lines.values()):
        left_line = building_corners_left[left_line_index][0]
        right_line = building_corners_right[right_line_index][0]
        # Calculate horizontal average of lines
        left_line_x = (left_line[0] + left_line[2]) / 2
        right_line_x = (right_line[0] + right_line[2]) / 2
        if left_line_x - right_line_x != 0:
            # Calculate the depth at the specific position
            #print("B:", PM.DISTANCE_BETWEEN_STEREO_CAMERAS, 'f:', PM.CAMERA_FOCAL)
            z = (PM.DISTANCE_BETWEEN_STEREO_CAMERAS * PM.CAMERA_FOCAL) / (left_line_x - right_line_x)
            z_array.append(z)
            # Calculate the corresponding x values
            x_mean = (left_line_x + right_line_x) / 2
            #print('left_line_x:', left_line_x, 'right_line_x:', right_line_x, 'f:', PM.CAMERA_FOCAL, 'z:', z, 'x_mean', x_mean)
            x = ((x_mean - PM.RESIZED_FRAME_SIZE[0] / 2) / PM.CAMERA_FOCAL) * z
            #print('x', x)
            x_array.append(x)


    return x_array, z_array

