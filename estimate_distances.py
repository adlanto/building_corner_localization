import numpy as np
import PARAMETERS as PM


def estimate_distances(building_corners_left, building_corners_right):
    print(building_corners_left)

    # buildings_corners = list(lines)
    # lines = list((x1, y1, x2, y2))

    # Volker:
    # 1. Berechnung der Fluchtgeraden -> Richtung Bildmittelpunkt ins Unendliche
    # 2. Schnittpunkt zwischen Building Corners Left (Linien) und Fluchtgeraden
    # 3. Epipolargerade für zweite Kamera aufstellen
    # 4. Schnittpunkt zwischen Building Corners Right (Linien) und Epipolargeraden
    # 5. Mit Hilfe des Abstandes der beiden Schnittpunkte auf Distanz schließen

    distances = {}
    # 1.
    # Bildgrößen
    x = PM.RESIZED_FRAME_SIZE[0]
    y = PM.RESIZED_FRAME_SIZE[1]
    # y = m * x + b

    # Steigung Epipolgerade
    m = (x/2)/(y/3)
    b = y/2
    # Epipolgerade
    ye = m * x + b

    # 2.
    # Punktgerade mit Rückgabe des Schnittpunktes
    for array in building_corners_left:

        x1 = building_corners_left[0]
        x2 = building_corners_left[2]
        y1 = building_corners_left[1]
        y2 = building_corners_left[3]
        # Steigung Punktepaar
        mp =(y2 - y1) / (x2 - x1)
        # y-Achsenabschnitt
        bp = y1 - mp * x1

        xp = (bp-b)/(m-mp)
        yp = mp * xp + bp

        array = array + 1

        print('xp', xp)
        print('yp', yp)

    return xp, yp


    # Parameter
    f = 5 * 10**-3  # Brennweite
    x = 1  # Abstand der beiden Kameras
    p = 3.75 * 10**-6  # Pixelgröße

    # Calculation of the distance
    xl = PM.RESIZED_FRAME_SIZE  # Pixelanzahl der linken Kamera         PM.RESIZED_FRAME_SIZE = (640, 480)
    xr = 0  # Pixelanzahl der rechten Kamera

    # for i in range(1, 1):
    #     d = (f * x) / (xl - xr)
    #     print(d)

    return distances