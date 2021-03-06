import cv2
import numpy as np
from src.preprocess_frame import preprocess_frame
from src.find_building_contours import detect_keypoints, detect_hough_lines
from src.validate_building_contours import get_building_corners, cluster_points_to_buildings, find_external_contours
from src.visualization import debug_visualization, building_corner_visualization, birds_eye_map
from src.estimate_distances import estimate_distances, Median
from src import carla_interface, PARAMETERS as PM


def process_frame(frame):

    # Resize Frame to predefined size
    frame = cv2.resize(frame, PM.RESIZED_FRAME_SIZE)
    preprocessed_frame = preprocess_frame(frame.copy())
    keypoints = detect_keypoints(preprocessed_frame.copy())
    hough_lines, hough_contours, hough_contours_poly = detect_hough_lines(preprocessed_frame.copy())
    vertical_lines, hough_lines_as_points = get_building_corners(frame.copy(), hough_lines.copy())
    keypoint_clusters = cluster_points_to_buildings(keypoints.copy())
    building_corners = find_external_contours(keypoint_clusters.copy(), vertical_lines.copy())
    if (PM.DEBUG_VISUALIZATION):
        errors = debug_visualization(frame.copy(), preprocessed_frame.copy(), keypoints, hough_lines,
                                     hough_contours, hough_contours_poly, vertical_lines, keypoint_clusters)

    return building_corners


if PM.USE_CARLA:
    carla = carla_interface.Carla()
else:
    cap_left = cv2.VideoCapture('videos/kempten_left_camera.avi')
    if not PM.MONO_CAMERA_MODE:
        cap_right = cv2.VideoCapture('videos/kempten_right_camera.avi')

median = Median()

fourcc = cv2.VideoWriter_fourcc(*'XVID')
output_size = (1820, 1000)
out = cv2.VideoWriter('output.avi', fourcc, 20.0, output_size)

while(True):

    frame_left = ()
    frame_right = ()

    # Capture frame-by-frame
    if PM.USE_CARLA:
        while not isinstance(frame_left, np.ndarray):
            frame_left = carla.left_image
    else:
        ret_left, frame_left = cap_left.read()

    if np.shape(frame_left) != ():
        building_corners_left = process_frame(frame_left)
    else:
        break

    if not PM.MONO_CAMERA_MODE:
        if PM.USE_CARLA:
            while not isinstance(frame_right, np.ndarray):
                frame_right = carla.right_image
        else:
            ret_right, frame_right = cap_right.read()

        if np.shape(frame_right) != ():
            building_corners_right = process_frame(frame_right)
        else:
            break

    left_frame_corners = building_corner_visualization(frame_left.copy(), building_corners_left, 'Left')
    if not PM.MONO_CAMERA_MODE:
        right_frame_corners = building_corner_visualization(frame_right.copy(), building_corners_right, 'Right')

    if not PM.MONO_CAMERA_MODE and not (building_corners_left == [] or building_corners_right == []):
        x_array, z_array = estimate_distances(frame_left, frame_right, building_corners_left, building_corners_right)
        x_array, z_array = median.update(x_array, z_array)
        #x_array = np.random.uniform(0, 100, size=10)
        #z_array = np.random.uniform(0, 100, size=10)

        output_frame = birds_eye_map(x_array, z_array, left_frame_corners, right_frame_corners)

        output_frame = cv2.resize(output_frame, output_size)
        out.write(output_frame)

    cv2.waitKey(PM.DURATION_PER_FRAME_MAIN_MS)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the capture
if PM.USE_CARLA:
    carla.destroy()
else:
    cap_left.release()
    if not PM.MONO_CAMERA_MODE:
        cap_right.release()
        out.release()
cv2.destroyAllWindows()