import cv2
import numpy as np
from src import PARAMETERS as PM


def detect_keypoints(preprocessed_image: np.ndarray) -> np.ndarray:

    # detect Harris corners / keypoints
    dst = cv2.cornerHarris(preprocessed_image, PM.HARRIS_NEIGHBOURHOOD_SIZE, PM.HARRIS_SOBEL_KERNEL_SIZE, PM.HARRIS_RELEVANCE_PARAM)

    # result is dilated for marking the corners
    dst = cv2.dilate(dst, None)

    # get data in plottable shape
    ret, dst = cv2.threshold(dst, 0.01*dst.max(), 255, 0)
    dst = np.uint8(dst)

    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

    # define the criteria to stop and refine the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(preprocessed_image, np.float32(centroids), (5, 5), (-1, -1), criteria)

    return np.vstack(corners)


def detect_hough_lines(preprocessed_image: np.ndarray) -> np.ndarray:

    uint8_image = preprocessed_image.astype(np.uint8)
    canny_image = cv2.Canny(uint8_image, PM.CANNY_FIRST_THRESHOLD, PM.CANNY_SECOND_THRESHOLD, PM.CANNY_SOBEL_KERNEL_SIZE)
    kernel = np.ones((PM.MORPHOLOGY_KERNEL_VERTICAL, PM.MORPHOLOGY_KERNEL_HORIZONTAL), np.uint8)
    canny_image = cv2.morphologyEx(canny_image, cv2.MORPH_CLOSE, kernel)

    contours, hierarchy = cv2.findContours(canny_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:100]

    contours_poly = [None]*len(contours)
    bound_rect = [None]*len(contours)
    centers = [None]*len(contours)
    radius = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv2.approxPolyDP(c, PM.POLYGON_APPROXIMATION_ACCURACY, True)
        bound_rect[i] = cv2.boundingRect(contours_poly[i])
        centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])

    drawing = np.zeros(preprocessed_image.shape, np.uint8)

    for i in range(len(contours)):
        cv2.drawContours(drawing, contours_poly, i, (255,255,255))

    lines = cv2.HoughLinesP(drawing, PM.HOUGH_RHO, PM.HOUGH_THETA, PM.HOUGH_THRESHOLD, PM.HOUGH_MIN_LINE_LENGTH, PM.HOUGH_MAX_LINE_GAP)

    return lines, contours, contours_poly
