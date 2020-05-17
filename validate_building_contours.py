import numpy as np
from sklearn.cluster import AgglomerativeClustering
import PARAMETERS as PM


def lines_to_points(lines):

    points = []
    for line in lines:
        for x1, y1, x2, y2 in line:
            points.append(np.array([x1, y1]))
            points.append(np.array([x2, y2]))

    return points


def get_building_corners(image: np.ndarray, lines: np.ndarray) -> np.ndarray:

    result = np.copy(image)
    vertical_lines = []
    # Check if vertical
    for line in lines:
        #print(line)
        # Check if lines are vertical
        for x1, y1, x2, y2 in line:
            # Check if lines are within i a defined horizontal range
            if x1-PM.HOUGH_LINES_VERTICAL_THRESHOLD < x2 < x1+PM.HOUGH_LINES_VERTICAL_THRESHOLD :
                # Check if lines are within the image - ignore Lines at the image borders
                if x1 != 0 and x1 != image.shape[0] and x1 != 0 and x1 != image.shape[0]:
                    vertical_lines.append(line)

    return vertical_lines, lines_to_points(vertical_lines)


def cluster_points_to_buildings(points):

    # Make horizontal axis less relevant
    for point in points:
        point[0] = point[0] * PM.CLUSTER_HARRIS_HORIZONTAL_RELEVANCE

    # Cluster points by distance threshold
    cluster = AgglomerativeClustering(n_clusters=None, linkage='single',
                                      distance_threshold=PM.CLUSTER_DISTANCE_THRESHOLD)
    cluster.fit(points)

    # Print Clusters
    custom_clusters = []
    colors = ['g.', 'r.', 'b.', 'y.', 'c.']
    for tmp_class, color in zip(range(0, 5), colors):
        x = points[cluster.labels_ == tmp_class]
        # Just continue with clusters that contain at least MIN_POINTS_PER_CLUSTER points
        if x.shape[0] >= PM.MIN_POINTS_PER_CLUSTER:
            custom_clusters.append(x)

    custom_clusters = np.array(custom_clusters)

    return custom_clusters


def get_corresponding_harris_line(hough_line, corner_lines):

    th = PM.HOUGH_HARRIS_LINES_DIST_THRESHOLD
    for harris_line in corner_lines:
        harris_calculated_y = hough_line[0] * harris_line[0] + harris_line[1]
        print(harris_calculated_y, '?=', hough_line[0])
        if hough_line[1] - th <= harris_calculated_y <= hough_line[1]:
            harris_calculated_y = hough_line[2] * harris_line[0] + harris_line[1]
            if hough_line[3] - th <= harris_calculated_y <= hough_line[3]:
                return True

    return False


def create_cluster_outer_line(corner, sorted_cluster):

    th = PM.BUILDING_CORNERS_HARRIS_THRESHOLD
    corner_points_x = [corner[0]]
    corner_points_y = [corner[1]]

    for value in sorted_cluster:
        if (corner[0] - th) <= value[0] <= (corner[0] + th):
            corner_points_x.append(value[0])
            corner_points_y.append(value[1])

    # print('lcp', corner_points_x, corner_points_y)

    if len(corner_points_x) < 3:
        return False, ()
    else:
        corner_line = np.polyfit(corner_points_x, corner_points_y, deg=1)
        # print(corner_line)
        return True, corner_line


def find_external_contours(clusters, vertical_hough_lines):

    corner_lines = []
    # find hotizontal outer lines for each cluster
    for cluster in clusters:

        # Sort cluster from min to max horizontal value
        # print(cluster)
        sorted_cluster = np.sort(cluster, 0)

        # Get lines from points that belong to left cluster corner
        success = False
        fail_counter = 0
        # print(sorted_cluster)
        while not success and fail_counter < len(sorted_cluster):
            left_corner = sorted_cluster[fail_counter]
            # print(left_corner, '=', np.amin(sorted_cluster, 0))
            success, left_corner_line = (create_cluster_outer_line(left_corner, sorted_cluster))
            if success:
                corner_lines.append(left_corner_line)
                break
            else:
                fail_counter = fail_counter+1

        # Get lines from points that belong to right cluster corner
        success = False
        fail_counter = 0
        sorted_cluster = sorted_cluster[::-1]
        # print(sorted_cluster)
        while not success and fail_counter < len(sorted_cluster):
            right_corner = sorted_cluster[fail_counter]
            # print(left_corner, '=', np.amin(sorted_cluster, 0))
            success, right_corner_line = (create_cluster_outer_line(right_corner, sorted_cluster))
            if success:
                corner_lines.append(right_corner_line)
                break
            else:
                fail_counter = fail_counter+1

    # print('corner_lines', corner_lines)

    # Check if hough lines are in a threshold around the corner lines
    external_contour_lines = []
    success = False
    for hough_line in vertical_hough_lines:
        success = get_corresponding_harris_line(hough_line[0], corner_lines)
        if success:
            external_contour_lines.append(hough_line[0])

    # print(external_contour_lines)

    external_contour_lines = vertical_hough_lines
    return external_contour_lines

