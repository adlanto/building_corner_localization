import numpy as np
import PARAMETERS as PM


def estimate_distances(building_corners_left, building_corners_right):

    distances = {}

    # Parameter
    f = 5 * 10 ^ -3  # Brennweite
    x = 1  # Abstand der beiden Kameras
    p = 3.75 * 10 ^ -6  # Pixelgröße

    # Calculation of the distance
    xl =  0# Pixelanzahl der linken Kamera
    xr =  0# Pixelanzahl der rechten Kamera
    xr =  0# Pixelanzahl der rechten Kamera

    for i in range(1, np.array + 1):
        d = (f * x) / (xl - xr)
        print(d)

    return distances