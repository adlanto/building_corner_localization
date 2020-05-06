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
Pk1 = [xw1, np.ceil(y1)]
Pk2 = [xw2, np.ceil(y2)]

# Ausgabe des Punktepaars
print(Pk1)
print(Pk2)

# Prüfung ob Kamera 1 den selbenPunkt wie Kamera 2 als Kantenpunkt entdeckt hat
if Pk1 == Pk2:
    print('Point match')

else:
    print('error')

