import cv2
import numpy as np
import PARAMETERS as PM


def preprocess_frame(frame: np.ndarray) -> np.ndarray:

    # Change image color from RGB to Gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use threshold filter to remove bright image parts
    ret, thresh_image = cv2.threshold(blur, 90, 255, cv2.THRESH_TOZERO_INV)

    crop = gray[0:PM.CROP_VALUE_FROM_TOP]
    crop = np.float32(crop)

    return crop
