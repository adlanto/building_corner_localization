import cv2
import numpy as np


def detect_corners(gray: np.ndarray, image: np.ndarray) -> np.ndarray:

    result = gray

    # # surf = cv2.HARRIS_create(1000)
    # # Find keypoints and descriptors directly
    # kp, des = surf.detectAndCompute(gray, None)

    # result = cv2.drawKeypoints(gray, kp, None, (255, 0, 0), 4)
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)

    # result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)

    # Threshold for an optimal value, it may vary depending on the image.
    image[dst > 0.01 * dst.max()] = [0, 0, 255]

    cv2.imshow('dst', image)

    result = gray
    return result
