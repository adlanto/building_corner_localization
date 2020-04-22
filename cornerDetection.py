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


def detect_corners2(gray: np.ndarray, image: np.ndarray) -> np.ndarray:
    crop_image = image[0:230]
    canny_image = cv2.Canny(crop_image, 50, 200, 3)
    cv2.imshow('canny', canny_image)
    result = np.copy(image)

    lines = cv2.HoughLinesP(canny_image,1,np.pi/180,100,minLineLength=20,maxLineGap=10)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(result, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return result


def validate_corners(corners: np.ndarray) -> np.ndarray:



    return corners