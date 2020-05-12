import numpy as np
import PARAMETERS as PM


def estimate_distances(building_corners_left, building_corners_right):
    print('l', building_corners_left)
    print('r', building_corners_right)

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

    # Steigung Epipolgerade links
    m1l = (x/3)/(y/2)
    b1l = y/2
    # Epipolgerade links
    yel = m1l * x + b1l

# 2.
    # Punktgerade mit Rückgabe des Schnittpunktes
    for array in building_corners_left:

        x1l = building_corners_left[0]
        x2l = building_corners_left[2]
        y1l = building_corners_left[1]
        y2l = building_corners_left[3]
        # Steigung Punktepaar
        mpl = (y2l - y1l) / (x2l - x1l)
        # y-Achsenabschnitt
        bpl = y1l - mpl * x1l

        xpl = (bpl-b1l)/(m1l-mpl)
        ypl = mpl * xpl + bpl

        array = array + 1

        print('xpl', xpl)
        print('ypl', ypl)

    return xpl, ypl

# 3.
    # Epipolgerade für rechts
    # Steigung Epipolgerade links
    m2r = -(x*(2/3))/(y/2)
    b2r = y/2
    # Epipolgerade rechts
    yer = m2 * x + b2

    # 4.
    # Punktgerade mit Rückgabe des Schnittpunktes
    for array in building_corners_right:
        x1r = building_corners_right[0]
        x2r = building_corners_right[2]
        y1r = building_corners_right[1]
        y2r = building_corners_right[3]
        # Steigung Punktepaar
        mpr = (y2r - y1r) / (x2r - x1r)
        # y-Achsenabschnitt
        bpr = y1r - mp * x1r

        xpr = (bpr - b2r) / (m2r - mpr)
        ypr = mpr * xpr + bpr

        array = array + 1

        print('xpr', xpr)
        print('ypr', ypr)

    return xpr, ypr

# 5.
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