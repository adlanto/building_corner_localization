import cv2
import numpy as np


def process_frame(frame: np.ndarray) -> np.ndarray:

    # Volker Anfang: Beliebige Filter einsetzen
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret, thresh = cv2.threshold(blur, 180, 255, cv2.THRESH_TOZERO_INV)
    cv2.imshow('blurred', thresh)
    return_image = thresh
    # Volker Manz Ende
    # Ziel: möglichst viele Punkte am Rande von den Gebäuden / auch braunes rechts

    return return_image
