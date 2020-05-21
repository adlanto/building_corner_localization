import numpy as np
import PARAMETERS as PM


def estimate_distances(building_corners_left, building_corners_right):
    print('l =', building_corners_left)
    print('r =', building_corners_right)

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

    # Epipolargerade für links
    # Steigung Epipolgerade links
    m1l = (3/2)*(y/x)
    b1l = -(y-m1l*x)
    # Epipolgerade links
    yel = m1l * x + b1l

# 2.
    # Punktgerade mit Rückgabe des Schnittpunktes
    l = len(building_corners_left)
    #print(l)


    for n in range(0, l):
        # print(building_corners_left)
        m = building_corners_left[n]
        # print('m=', building_corners_left[n])

        # m = building_corners_left[n]
        # print('m =', m)
        # print('m1 =', m[0])

        if len(m) == 0:
            xpl = -1


        else:
            x1l = m[0, 0]
            x2l = m[0, 1]
            y1l = m[0, 2]
            y2l = m[0, 3]


            # Steigung Punktepaar
            if (x2l - x1l) == 0:
                mpl = 0
            else:
                mpl = (y2l - y1l) / (x2l - x1l)


            # y-Achsenabschnitt
            bpl = y1l - mpl * x1l

            xpl = (bpl - b1l) / (m1l - mpl)
            ypl = mpl * xpl + bpl


            #print()
            print('xpl =', xpl) #, '; ypl =', ypl)
            #print()

# 3. RECHTE SEITE
            # Epipolgerade für rechts
            # Steigung Epipolgerade rechts
            m2r = (y / 2) / (((2 / 3) * 640) - 640)
            b2r = -(y - m2r * x)
            # Epipolgerade rechts
            yer = m2r * x + b2r

# 4.
            # Punktgerade mit Rückgabe des Schnittpunktes
            r = len(building_corners_right)
            # print(r)

            for k in range(0, r):
                # print(building_corners_right)
                n = building_corners_right[k]


                if len(n) == 0:
                    xpr = -1


                else:
                    x1r = n[0, 0]
                    x2r = n[0, 2]
                    y1r = n[0, 1]
                    y2r = n[0, 3]

                    # Steigung Punktepaar
                    if (x2r - x1r) == 0:
                        mpr = 0
                    else:
                        mpr = (y2r - y1r) / (x2r - x1r)


                    # y-Achsenabschnitt
                    bpr = y1r - mpr * x1r

                    xpr = (bpr - b2r) / (m2r - mpr)
                    ypr = mpr * xpr + bpr

                    #print()
                    print('xpr =', xpr) # , '; ypr =', ypr)
                    #print()





# 5. Calculation of the distance


                    if (xpl != -1) & (xpr != -1):
                        d = (PM.f * PM.x) / (abs(xpl- abs(xpr)) * PM.p)
                        distances = round(d, 3)


                    else:
                        distances = 'no distance'

                    #print('d = ', distances)

# 6. Relative Distanzen x,y

                    x_rel = abs(xpl-xpr)
                    y_rel = np.sqrt(distances**2 - x_rel**2)

                    print()
                    print('x_real = ', x_rel)
                    print('y_rel', y_rel)
                    print()


    return xpr, ypr
