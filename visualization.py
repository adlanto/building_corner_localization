import cv2
import numpy as np
import matplotlib.pyplot as plt
import PARAMETERS as PM

def building_corner_visualization(frame, building_corners, name):

    for building_corner in building_corners:
        for x1, y1, x2, y2 in building_corner:
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow('Building Corners '+name, frame)

    return


def debug_visualization(frame, preprocessed_frame, keypoints, hough_lines,
                                         hough_contours, hough_contours_poly, vertical_lines, keypoint_clusters) -> int:

    errors = 0
    # Show the image after the preprocess step
    cv2.imshow('Preprocessed Image', np.int8(preprocessed_frame))

    # Hough visualization
    if (PM.VISUALIZE_HOUGH):
        errors = errors + hough_lines_visualization(frame.copy(), hough_contours, hough_contours_poly, hough_lines, vertical_lines)

    # Harris visualization
    if (PM.VISUALIZE_HARRIS):
        errors = errors + harris_visualization(frame.copy(), keypoints)
        if (PM.VISUALIZE_HARRIS_CLUSTERS):
            errors = errors + cluster_visualization(keypoint_clusters)

    return errors


def cluster_visualization(clusters: np.ndarray) -> bool:

    colors = ['g.', 'r.', 'b.', 'y.', 'c.']
    for cluster, color in zip(clusters, colors):
        plt.plot(cluster[:, 0], cluster[:, 1], color, alpha=0.5)
    plt.show()

    #plt.plot(points[cluster.labels_ == -1, 0], points[cluster.labels_ == -1, 1], 'k+', alpha=0.1)

    return 0


def harris_visualization(image: np.ndarray, corners: np.ndarray) -> int:

    errors = 0
    for point in corners:
        point = np.int0(point)
        try:
            image = cv2.circle(image, (point[0], point[1]), radius=3, color=(0, 0, 255), thickness=-1)
            #image[res[:, 1], res[:, 0]] = [0, 0, 255]
            #image[res[:, 3], res[:, 2]] = [0, 255, 0]
        except:
            errors = errors + 1
            # print("A detected keypoint was not part of the image - ignoring point.")
    cv2.imshow('Harris', image)

    return errors


def hough_lines_visualization(image: np.ndarray, contours, contours_poly, lines, vertical_lines) -> bool:

    empty_image = np.zeros(image.shape, np.uint8)
    hough_image = np.copy(image)
    vertical_hough_image = np.copy(image)
    for i in range(len(contours)):
        cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
        cv2.drawContours(image, contours_poly, i, (255, 255, 255))
        cv2.drawContours(empty_image, contours, -1, (0, 255, 0), 3)
        cv2.drawContours(empty_image, contours_poly, i, (255, 255, 255))

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(hough_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    for line in vertical_lines:
        for x1, y1, x2, y2 in line:
            cv2.line(vertical_hough_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow('Hough_Lines', hough_image)
    cv2.imshow('Vertical_Hough_Lines', vertical_hough_image)
    cv2.imshow('Contours_Only', empty_image)
    cv2.imshow('Contours', image)

    return 0



