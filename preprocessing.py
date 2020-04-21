import cv2
import numpy as np


def process_frame(frame: np.ndarray) -> np.ndarray:

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray
