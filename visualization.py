import cv2
import numpy as np
import matplotlib.pyplot as plt
import PARAMETERS as PM


def building_corner_visualization(frame, building_corners, name):

    for building_corner in building_corners:
        for x1, y1, x2, y2 in building_corner:
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    if PM.DEBUG_VISUALIZATION:
        cv2.imshow('Building Corners '+name, frame)

    return frame


def debug_visualization(frame, preprocessed_frame, keypoints, hough_lines,
                                         hough_contours, hough_contours_poly, vertical_lines, keypoint_clusters) -> int:

    errors = 0
    # Show the image after the preprocess step
    cv2.imshow('Preprocessed Image', np.int8(preprocessed_frame))

    # Hough visualization
    if (PM.VISUALIZE_HOUGH):
        errors = errors + hough_lines_visualization(frame.copy(), hough_contours, hough_contours_poly, hough_lines, vertical_lines)

    # Harris visualization
    if (PM.VISUALIZE_HARRIS):
        errors = errors + harris_visualization(frame.copy(), keypoints)
        if (PM.VISUALIZE_HARRIS_CLUSTERS):
            errors = errors + cluster_visualization(keypoint_clusters)

    return errors


def cluster_visualization(clusters: np.ndarray) -> bool:

    colors = ['g.', 'r.', 'b.', 'y.', 'c.']
    for cluster, color in zip(clusters, colors):
        plt.plot(cluster[:, 0], cluster[:, 1], color, alpha=0.5)
    plt.show()

    #plt.plot(points[cluster.labels_ == -1, 0], points[cluster.labels_ == -1, 1], 'k+', alpha=0.1)

    return 0


def harris_visualization(image: np.ndarray, corners: np.ndarray) -> int:

    errors = 0
    for point in corners:
        point = np.int0(point)
        try:
            image = cv2.circle(image, (point[0], point[1]), radius=3, color=(0, 0, 255), thickness=-1)
            #image[res[:, 1], res[:, 0]] = [0, 0, 255]
            #image[res[:, 3], res[:, 2]] = [0, 255, 0]
        except:
            errors = errors + 1
            # print("A detected keypoint was not part of the image - ignoring point.")
    cv2.imshow('Harris', image)

    return errors


def hough_lines_visualization(image: np.ndarray, contours, contours_poly, lines, vertical_lines) -> bool:

    empty_image = np.zeros(image.shape, np.uint8)
    hough_image = np.copy(image)
    vertical_hough_image = np.copy(image)
    for i in range(len(contours)):
        cv2.drawContours(image, contours, -1, (0, 255, 0), 3)
        cv2.drawContours(image, contours_poly, i, (255, 255, 255))
        cv2.drawContours(empty_image, contours, -1, (0, 255, 0), 3)
        cv2.drawContours(empty_image, contours_poly, i, (255, 255, 255))

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(hough_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    for line in vertical_lines:
        for x1, y1, x2, y2 in line:
            cv2.line(vertical_hough_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

    cv2.imshow('Hough_Lines', hough_image)
    cv2.imshow('Vertical_Hough_Lines', vertical_hough_image)
    cv2.imshow('Contours_Only', empty_image)
    cv2.imshow('Contours', image)

    return True


def birds_eye_map(x_array, y_array, left_frame_with_corners, right_frame_with_corners):

    # All variables in meter - scale for displaying an image in a higher resolution
    scale = 10
    map_size_x = 100
    map_size_y = 100
    ego_x = 50
    ego_y = 100
    ego_width = 2
    camera_distance = 1
    camera_fov = PM.CAMERA_FOV
    y_camera_range = 100

    map = np.full((map_size_x * scale, map_size_y * scale, 3), (62, 117, 59), dtype=np.uint8)

    # ** Draw lines **
    left_line_x = (map_size_x / 2 - 5.25) * scale
    right_line_x = (map_size_x / 2 + 1.75) * scale
    middle_line_x = (map_size_x / 2 - 1.75) * scale
    cv2.line(map, (int(left_line_x), 0), (int(left_line_x), map_size_y * scale), color=(80, 80, 80), thickness=2)
    cv2.line(map, (int(right_line_x), 0), (int(right_line_x), map_size_y * scale), color=(80, 80, 80), thickness=2)
    lane = np.array([[(int(left_line_x), 0), (int(left_line_x), map_size_y * scale),
                      (int(right_line_x), map_size_y * scale), (int(right_line_x), 0)]], dtype=np.int32)
    cv2.fillPoly(map, lane, color=(150, 150, 150))
    cv2.line(map, (int(middle_line_x), 0), (int(middle_line_x), map_size_y * scale), color=(255, 255, 255), thickness=1)

    # Draw Ego Vehicle
    left_upper_ego_point = (int((ego_x - ego_width / 2) * scale), int((ego_y - 1) * scale))
    right_bottom_ego_point = (int((ego_x + ego_width / 2) * scale), int(ego_y * scale))
    cv2.rectangle(map, left_upper_ego_point, right_bottom_ego_point, (0, 0, 0), -1)

    # Draw Camera Centers on Ego Vehicle
    camera_left_center = (int((ego_x - camera_distance / 2) * scale), int((ego_y - 1) * scale))
    cv2.circle(map, camera_left_center, 2, (0, 0, 255), 2)
    camera_right_center = (int((ego_x + camera_distance / 2) * scale), int((ego_y - 1) * scale))
    cv2.circle(map, camera_right_center, 2, (0, 255, 0), 2)

    # ** Draw Field of View Cones **

    # Create Overlay for Cones
    cone_overlay_right = np.full((map_size_x * scale, map_size_y * scale, 3), 255, dtype=np.uint8)
    cone_overlay_left = np.full((map_size_x * scale, map_size_y * scale, 3), 255, dtype=np.uint8)

    # Recalculate Variables based on Scale
    camera_fov = np.pi * camera_fov / 180
    x_camera_range = y_camera_range * np.tan(camera_fov / 2)
    x_camera_range = x_camera_range * scale
    y_camera_range = y_camera_range * scale
    map_size_y = map_size_y * scale

    # Cone of Left Camera
    camera_left_cone_left_pt = np.array([int(camera_left_center[0] - x_camera_range / 2), map_size_y - y_camera_range])
    camera_left_cone_right_pt = np.array([int(camera_left_center[0] + x_camera_range / 2), map_size_y - y_camera_range])
    left_cone = np.array([[camera_left_center, camera_left_cone_left_pt, camera_left_cone_right_pt]], dtype=np.int32)
    cv2.fillPoly(cone_overlay_left, left_cone, color=(0, 0, 255))

    # Cone of Right Camera
    camera_right_cone_left_pt = (int(camera_right_center[0] - x_camera_range / 2), map_size_y - y_camera_range)
    camera_right_cone_right_pt = (int(camera_right_center[0] + x_camera_range / 2), map_size_y - y_camera_range)
    right_cone = np.array([[camera_right_center, camera_right_cone_left_pt, camera_right_cone_right_pt]],
                          dtype=np.int32)
    cv2.fillPoly(cone_overlay_right, right_cone, color=(0, 255, 0))

    # Add weighted Overlays to the original map
    cv2.addWeighted(cone_overlay_left, 0.3, map, 1 - 0.3, 0, map)
    cv2.addWeighted(cone_overlay_right, 0.3, map, 1 - 0.3, 0, map)

    # ** Draw Points of Building Corner Localization **

    # Iterate over all points
    for x, y in zip(x_array, y_array):
        x_text = 'x: ' + str(np.round(x, 2))
        y_text = 'y: ' + str(np.round(y, 2))
        x = (map_size_x / 2 + x) * scale
        y = map_size_y - y * scale
        # Draw every Point as Circle on the Map
        cv2.circle(map, (int(x), int(y)), radius=int(scale / 2), color=(0, 0, 0), thickness=-1)
        # Write coordinates of the Point next to it on the Map
        cv2.putText(map, x_text, (int(x + scale), int(y - scale)), cv2.FONT_ITALIC, 0.05 * scale, (0, 0, 0), 1)
        cv2.putText(map, y_text, (int(x + scale), int(y + scale)), cv2.FONT_ITALIC, 0.05 * scale, (0, 0, 0), 1)

    # ** Other Information **

    # Legend 62, 117, 59
    cv2.line(map, (10, map_size_y - 80), (20, map_size_y - 80), color=(40, 80, 215), thickness=5)
    cv2.putText(map, 'Left Camera', (25, map_size_y - 75), cv2.FONT_ITALIC, 0.05 * scale, (0, 0, 0), 1)
    cv2.line(map, (10, map_size_y - 50), (20, map_size_y - 50), color=(40, 185, 40), thickness=5)
    cv2.putText(map, 'Right Camera', (25, map_size_y - 45), cv2.FONT_ITALIC, 0.05 * scale, (0, 0, 0), 1)
    cv2.line(map, (10, map_size_y - 20), (20, map_size_y - 20), color=(83, 134, 30), thickness=5)
    cv2.putText(map, 'Camera Overlap', (25, map_size_y - 15), cv2.FONT_ITALIC, 0.05 * scale, (0, 0, 0), 1)

    # Status Information
    status_text = 'Number of detected building corners: ' + str(len(x_array))
    cv2.putText(map, status_text, (10, 20), cv2.FONT_ITALIC, 0.05 * scale, (0, 0, 0), 2)

    # ***** Create visualization image *****

    # Combine Stereo Camera images
    cv2.putText(left_frame_with_corners, 'Left Camera', (10, 30), cv2.FONT_ITALIC, 0.1 * scale, (0, 255, 255), 2)
    cv2.putText(right_frame_with_corners, 'Right Camera', (10, 30), cv2.FONT_ITALIC, 0.1 * scale, (0, 255, 255), 2)
    difference = int(map.shape[0]) - (int(left_frame_with_corners.shape[0]) * 2)

    # Create border image to plot between birds eye map and stereo camera images
    height = int(difference / 3)
    border_vertical = np.full((height, left_frame_with_corners.shape[1], 3), (159, 187, 160), dtype=np.uint8)
    stereo_camera_images = cv2.vconcat([border_vertical, left_frame_with_corners, border_vertical,
                                        right_frame_with_corners, border_vertical])
    # cv2.imshow("stereo_camera_images", stereo_camera_images)
    border_horizontal = np.full((map.shape[0], 60, 3), (159, 187, 160), dtype=np.uint8)
    scaler = map.shape[1] / stereo_camera_images.shape[1]
    # print(map.shape[1], stereo_camera_images.shape[0], scaler)
    stereo_camera_images = cv2.resize(stereo_camera_images, (stereo_camera_images.shape[1], map.shape[0]))

    # Bring all together and show it
    vis_image = cv2.hconcat([border_horizontal, stereo_camera_images, border_horizontal, map, border_horizontal])
    # cv2.imshow('Birds-Eye-View Map', map)
    cv2.imshow('Building Corner Localization', vis_image)

    return vis_image


