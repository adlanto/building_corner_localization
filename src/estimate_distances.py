import numpy as np
from src import PARAMETERS as PM
import statistics


class Median:

    def __init__(self):

        self.tracked_points = []
        self.timestamp = 0
        self.frame_counter_for_deletion = {}
        self.previous_point_length = {}

    def update(self, x_array, z_array):

        median_x_array = []
        median_z_array = []

        # If no points are tracked yet - add all points detected in current frame to be tracked
        if len(self.tracked_points) == 0:
            for x, z in zip(x_array, z_array):
                tracked_point = [[x, z], ]
                self.tracked_points.append(tracked_point)
        # Else: Points were detected in a previous frame
        else:
            # Iterate over new points
            for x_new, z_new in zip(x_array, z_array):
                for i, tracked_point in enumerate(self.tracked_points):
                    x_old = tracked_point[0][0]
                    # Try to find corresponding points
                    if x_old - 1 <= x_new <= x_old + 1:
                        # If found add to tracked_point and continue with next new point
                        tracked_point.append([x_new, z_new])
                        break
                    if i == len(self.tracked_points) - 1:
                        # If point was not found before loop completed, add new tracked point
                        tracked_point = [[x_new, z_new], ]
                        self.tracked_points.append(tracked_point)
                        break

        # Create median of all points that were tracked more than FRAMES_FOR_MEDIAN times
        for tracked_point in self.tracked_points:
            if len(tracked_point) >= PM.FRAMES_FOR_MEDIAN:
                median_x_array.append(statistics.median_grouped(list(zip(*tracked_point))[0]))
                median_z_array.append(statistics.median_grouped(list(zip(*tracked_point))[1]))
                # Remove first point from the tracked point list
                tracked_point.pop(0)

        self.timestamp = self.timestamp + 1
        deletion_marker = []
        for i, tracked_point in enumerate(self.tracked_points):
            self.previous_point_length[i] = len(tracked_point)
            if len(tracked_point) == self.previous_point_length[i]:
                if i in self.frame_counter_for_deletion.keys():
                    self.frame_counter_for_deletion[i] = self.frame_counter_for_deletion[i] + 1
                else:
                    self.frame_counter_for_deletion[i] = 1
                if self.frame_counter_for_deletion[i] >= PM.NUMBER_FRAMES_AFTER_WHICH_DELETE_MEDIAN_POINT:
                    deletion_marker.append(i)
            else:
                self.frame_counter_for_deletion[i] = 0

        for delete_index in deletion_marker[::-1]:
            self.previous_point_length.pop(delete_index)
            self.frame_counter_for_deletion.pop(delete_index)
            self.tracked_points.pop(delete_index)

        return median_x_array, median_z_array


def estimate_distances(frame_left, frame_right, building_corners_left, building_corners_right):

    # Assertion of lines in left to lines in right Camera
    map_lines = {}
    for i, l_lines in enumerate(building_corners_left):
        euclidean_distances = []
        for r_lines in building_corners_right:
            euclidean_distances.append(np.sqrt((l_lines[0, 0] - r_lines[0, 0])**2 + (l_lines[0, 2] - r_lines[0, 2])**2))
        if np.amin(euclidean_distances) < PM.MAXIMAL_DISTANCE_CORRESPONDING_LINES:
            map_lines[i] = np.argmin(euclidean_distances)
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
            z = (PM.DISTANCE_BETWEEN_STEREO_CAMERAS * PM.CAMERA_FOCAL) / (left_line_x - right_line_x)
            z_array.append(z)
            # Calculate the corresponding x values
            x_mean = (left_line_x + right_line_x) / 2
            x = ((x_mean - PM.RESIZED_FRAME_SIZE[0] / 2) / PM.CAMERA_FOCAL) * z
            x_array.append(x)

    return x_array, z_array

