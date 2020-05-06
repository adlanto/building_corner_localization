import cv2
import numpy as np
from preprocessing import preprocess_frame
from postprocessing import view_frame
from cornerDetection import detect_corners, detect_corners2, get_building_corners
from cornerTracker import track_corners


cap = cv2.VideoCapture('videos/buildings1.avi')

corners = []
counter = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if np.shape(frame) != ():
        frame = cv2.resize(frame, (640, 480))
        gray = preprocess_frame(frame)
        result = detect_corners(gray, frame)
        result, lines = detect_corners2(gray, frame)
        corners.append(get_building_corners(counter, frame, lines))
        view_frame(frame)
        #cv2.waitKey(500)
        counter += 1
    else:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

track_corners(corners)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()