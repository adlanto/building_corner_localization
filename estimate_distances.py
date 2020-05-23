import numpy as np
import PARAMETERS as PM


def estimate_distances(building_corners_left, building_corners_right):
    #print('l =', building_corners_left)
    #print('r =', building_corners_right)

    # 5. Zuordnung Kante zu Kamera 1 und Kamera 2


    map_lines = {}
    for l, l_lines in enumerate(building_corners_left):
        euclidean_distances = []
        for r_lines in building_corners_right:
            euclidean_distances.append(np.sqrt((l_lines[0, 0] - r_lines[0, 0])**2 + (l_lines[0, 2] - r_lines[0, 2])**2))
        map_lines[l] = np.argmin(euclidean_distances)
        #print(euclidean_distances)
    #print(map_lines)

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
    x_imagesize = PM.RESIZED_FRAME_SIZE[0]
    y_imagesize = PM.RESIZED_FRAME_SIZE[1]


    alpha_epipolline = (np.arctan(((y_imagesize / 2)) / ((x_imagesize / 3)))) * (360 / (2 * np.pi))
    #print(alpha_epipolline)
    # y = m * x + b

    # Epipolargerade für links
    # Steigung Epipolgerade links
    m1l = (3 / 2) * (y_imagesize / x_imagesize)
    b1l = - (y_imagesize - m1l * x_imagesize)
    # Epipolgerade links
    yel = m1l * x_imagesize + b1l

# 2.
    # Punktgerade mit Rückgabe des Schnittpunktes
    # l = len(building_corners_left)
    #print(l)

    left_intersections = []
    for left_cornerline in building_corners_left:

        #
        x1l = left_cornerline[0, 0]
        y1l = left_cornerline[0, 1]
        x2l = left_cornerline[0, 2]
        y2l = left_cornerline[0, 3]


        # Steigung Punktepaar
        if (x2l - x1l) == 0:
            mpl = 1e5
        else:
            mpl = (y2l - y1l) / (x2l - x1l)


        # y-Achsenabschnitt
        # y= mx+b
        bpl = y1l - mpl * x1l

        xpl = (bpl - b1l) / (m1l - mpl)
        ypl = mpl * xpl + bpl


        #print()
        #print('xpl =', xpl) #, '; ypl =', ypl)
        #print()

        left_intersections.append([xpl])
        print('l= ', left_intersections)

    #print('left_intersections', left_intersections)

# 3. RECHTE SEITE
    # Epipolgerade für rechts
    # Steigung Epipolgerade rechts
    m2r = (y_imagesize / 2) / (((2 / 3) * 640) - 640)
    b2r = -(y_imagesize - m2r * x_imagesize)
    # Epipolgerade rechts
    yer = m2r * x_imagesize + b2r

# 4.
            # Punktgerade mit Rückgabe des Schnittpunktes

    right_intersections = []
    for right_cornerline in building_corners_right:

        x1r = right_cornerline[0, 0]
        x2r = right_cornerline[0, 2]
        y1r = right_cornerline[0, 1]
        y2r = right_cornerline[0, 3]

        # Steigung Punktepaar
        if (x2r - x1r) == 0:
            mpr = 1e5
        else:
            mpr = (y2r - y1r) / (x2r - x1r)


        # y-Achsenabschnitt
        bpr = y1r - mpr * x1r

        xpr = (bpr - b2r) / (m2r - mpr)
        ypr = mpr * xpr + bpr

        #print()
        #print('xpr =', xpr) # , '; ypr =', ypr)
        #print()

        right_intersections.append([xpr])
        print('r= ', right_intersections)

    #print('right_intersections', right_intersections)

# 5. Calculation with the correspndance points
    distances_and_xintersections = []
    for i, left_intersection in enumerate(left_intersections):
        right_intersection = right_intersections[map_lines[i]]

        # 5. Calculation of the distance
        d = (PM.f * PM.x) / (abs(left_intersection[0] - right_intersection[0]) * PM.p)

        distances_and_xintersections.append([round(d, 3), left_intersection[0], right_intersection[0]])


    print('d = ', distances_and_xintersections)

# 6. Relative Distanzen x,y
    x_array = []
    y_array = []

    for distance, xpl, xpr in distances_and_xintersections:
        x_rel = abs(xpl - xpr)
        x_array.append(x_rel)
        y_array.append(np.sqrt(distance ** 2 + x_rel ** 2)) #### x_rel ist in pixel angegeben --> umrechnung pixel in meter
        # --> mit winkel rechnen!
    print()
    #print('x_array = ', x_array)
    #print('y_array', y_array)
    print()


    return x_array, y_array
