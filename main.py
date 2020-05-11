import cv2
import numpy as np
from preprocess_frame import preprocess_frame
import PARAMETERS as PM
from find_building_contours import detect_keypoints, detect_hough_lines
from validate_building_contours import get_building_corners, cluster_points_to_buildings
from visualization import debug_visualization

cap = cv2.VideoCapture('videos/buildings1.avi')

corners = []
counter = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if np.shape(frame) != ():
        # Resize Frame to predefined size
        frame = cv2.resize(frame, PM.RESIZED_FRAME_SIZE)
        preprocessed_frame = preprocess_frame(frame)
        keypoints = detect_keypoints(preprocessed_frame)
        hough_lines, hough_contours, hough_contours_poly = detect_hough_lines(preprocessed_frame)
        vertical_lines, hough_lines_as_points = get_building_corners(frame, hough_lines)
        keypoint_clusters = cluster_points_to_buildings(keypoints)

        if (PM.DEBUG_VISUALIZATION):
            errors = debug_visualization(frame, preprocessed_frame, keypoints, hough_lines,
                                         hough_contours, hough_contours_poly, vertical_lines, keypoint_clusters)
        cv2.waitKey(PM.DURATION_PER_FRAME_MAIN_MS)
    else:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()