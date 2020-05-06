import cv2
import numpy as np


def preprocess_frame(frame: np.ndarray) -> np.ndarray:

    # Volker Anfang: Beliebige Filter einsetzen
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Variante 1:
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret, thresh = cv2.threshold(blur, 90, 255, cv2.THRESH_TOZERO_INV)
    #ret, thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,15,12)
    cv2.imshow('blurred + threshed', thresh)

    return_image = thresh
    # Volker Manz Ende
    # Ziel: möglichst viele Punkte am Rande von den Gebäuden / auch braunes rechts

    return return_image

