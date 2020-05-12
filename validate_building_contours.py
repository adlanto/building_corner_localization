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
