import numpy as np


################################# Beispielwerte #######################################
x1 = 3
x2 = 2

# Winkelumrechnung von Grad nach Rad
grad1= 25 / 360 * 2 * np.pi
grad2= 17 / 360 * 2 * np.pi

# Distanz aus Sicht der einzelnen Kameras
dk1 = x1 / np.sin(grad1)
dk2 = x2 / np.sin(grad2)

##########################################################################################

# Distanz berechnen
y1 = x1 / np.tan(grad1)
y2 = x2 / np.tan(grad2)

# Abstand der einzelnen Kameras von dem Weltkoordinatemittelpunkt
xk1 = -0.5
xk2 = 0.5

#
xw1 = x1 + xk1
xw2 = x2 + xk2

# Punkte in WEltkoordinaten
Pk1 = [xw1, (y1)]
Pk2 = [xw2, (y2)]

# Ausgabe des Punktepaars
print()
print('Pk1 =', Pk1)
print('Pk2 =', Pk2)

#Schwellwerte x
# 5% Toleranz
thresh = 0.05
x11 = xw1 -(xw1 * thresh)
x21 = (xw1 * thresh) + xw1

x12 = xw2 - (xw2 * thresh)
x22 = (xw2 * thresh) + xw2

print()
print('x11 =', x11)
print('x21 =', x21)
print()
print('x12 =', x12)
print('x22 =', x22)

#Schwellwerte y
# 5% Toleranz
thresh = 0.05
y11 = y1 - (y1 * thresh)
y21 = (y1 * thresh) + y1

y12 = y2 - (y2 * thresh)
y22 = (y2 * thresh) + y2

print()
print('y12 =', y11)
print('y21 =', y21)
print()
print('y12 =', y12)
print('y22 =', y22)

# Prüfung ob Kamera 1 den selben Punkt wie Kamera 2 als Kantenpunkt entdeckt hat
if ((x11 <= xw1) and (xw1 <= x21)) == ((x12 <= xw2) and (xw2 <= x22)):
    print()
    print('Point in x match')

    if ((y11 <= y1) and (y1 <= y21)) == ((y12 <= y2) and (y2 <= y22)):
        print('Point in y match')
    else:
        print('Error in Point y')

else:
    print('Error in Point x')
