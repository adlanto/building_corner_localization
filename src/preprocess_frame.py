import cv2
import numpy as np
from src import PARAMETERS as PM


def preprocess_frame(frame: np.ndarray) -> np.ndarray:

    # Change image color from RGB to Gray
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    crop = gray[0:PM.CROP_VALUE_FROM_TOP]
    crop = np.float32(crop)

    return crop
