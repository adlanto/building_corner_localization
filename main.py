import cv2
import numpy as np
from preprocess_frame import preprocess_frame
import PARAMETERS as PM
from find_building_contours import detect_keypoints, detect_hough_lines
from validate_building_contours import get_building_corners, cluster_points_to_buildings
from visualization import debug_visualization, building_corner_visualization

cap = cv2.VideoCapture('videos/buildings1.avi')

corners = []
counter = 0
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if np.shape(frame) != ():
        # Resize Frame to predefined size
        frame = cv2.resize(frame, PM.RESIZED_FRAME_SIZE)
        preprocessed_frame = preprocess_frame(frame.copy())
        keypoints = detect_keypoints(preprocessed_frame.copy())
        hough_lines, hough_contours, hough_contours_poly = detect_hough_lines(preprocessed_frame.copy())
        vertical_lines, hough_lines_as_points = get_building_corners(frame.copy(), hough_lines.copy())
        keypoint_clusters = cluster_points_to_buildings(keypoints.copy())
        building_corners = vertical_lines # will be replaced by validation function
        if (PM.DEBUG_VISUALIZATION):
            errors = debug_visualization(frame.copy(), preprocessed_frame.copy(), keypoints, hough_lines,
                                         hough_contours, hough_contours_poly, vertical_lines, keypoint_clusters)
        if (PM.VISUALIZE_BUILDING_CORNERS):
            building_corner_visualization(frame.copy(), building_corners)
        cv2.waitKey(PM.DURATION_PER_FRAME_MAIN_MS)
    else:
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()