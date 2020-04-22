import cv2
import numpy as np


def process_frame(frame: np.ndarray) -> np.ndarray:

    # Volker Anfang: Beliebige Filter einsetzen
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Variante 1:
    #blur = cv2.GaussianBlur(gray,(5,5),0)
    #ret, thresh = cv2.threshold(blur, 180, 255, cv2.THRESH_TOZERO_INV)
    #cv2.imshow('blurred', blur)

    # Variante 2:
    F1 = np.array([[1, 1, 1],
                   [0, 0, 0],
                   [-1, -1, -1]])

    F2 = np.array([[1, 0, -1],
                   [1, 0, -1],
                   [1, 0, -1]])
    X1 = cv2.filter2D(gray, -1, F1)
    X2 = cv2.filter2D(gray, -1, F2)
    x_mag = np.sqrt(X1 ** 2 + X2 ** 2)
    X_mag = np.abs(x_mag) / (3 * 255.0)
    print(X_mag.shape)
    cv2.imshow('X_mag', X_mag)


    return_image = x_mag
    # Volker Manz Ende
    # Ziel: möglichst viele Punkte am Rande von den Gebäuden / auch braunes rechts

    return return_image
