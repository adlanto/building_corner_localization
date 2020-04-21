import cv2
import numpy as np
from preprocessing import process_frame
from postprocessing import view_frame
from cornerDetection import detect_corners


cap = cv2.VideoCapture('buildingsshort.avi')
#test
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if np.shape(frame) != ():
        gray = process_frame(frame)
        result = detect_corners(gray)
        view_frame(result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()