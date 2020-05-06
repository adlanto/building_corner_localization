import cv2
import numpy as np
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt

# Value to be changed
crop_value_from_top = 230

def cluster_points_to_buildings(points):

    # Make horizonal axis less relevant
    relevance_factor = 1.5
    for point in points:
        point[0] = point[0] * relevance_factor

    # Cluster points by distance threshold
    cluster = AgglomerativeClustering(n_clusters=None, linkage='single', distance_threshold=80)
    cluster.fit(points)

    # Print Clusters
    custom_clusters = []
    colors = ['g.', 'r.', 'b.', 'y.', 'c.']
    for cclass, color in zip(range(0, 5), colors):
        Xk = points[cluster.labels_ == cclass]
        #plt.plot(Xk[:, 0], Xk[:, 1], color, alpha=0.3)
        # Just continue with clusters that contain more than three points
        if Xk.shape[0] > 3:
            custom_clusters.append(Xk)
    #plt.plot(points[cluster.labels_ == -1, 0], points[cluster.labels_ == -1, 1], 'k+', alpha=0.1)
    #plt.show()

    custom_clusters = np.array(custom_clusters)
    #print('Returned', custom_clusters.shape[0], 'clusters.')
    #print(custom_clusters)

    return custom_clusters


def detect_corners(gray: np.ndarray, image: np.ndarray) -> np.ndarray:

    # # surf = cv2.HARRIS_create(1000)
    # # Find keypoints and descriptors directly
    # kp, des = surf.detectAndCompute(gray, None)

    crop = gray[0:crop_value_from_top]
    crop = np.float32(crop)

    # result = cv2.drawKeypoints(gray, kp, None, (255, 0, 0), 4)
    dst = cv2.cornerHarris(crop, 2, 3, 0.04)

    # result is dilated for marking the corners, not important
    dst = cv2.dilate(dst, None)

    ret, dst = cv2.threshold(dst, 0.01*dst.max(), 255, 0)
    dst = np.uint8(dst)

    # find centroids
    ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

    # define the criteria to stop and refine the corners
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
    corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, -1), criteria)
    cluster_points_to_buildings(np.vstack(corners))
    # copy_dst = cv2.copyMakeBorder(dst, 0, image.shape[0]-crop_value_from_top, 0, 0, cv2.BORDER_CONSTANT, 0)
    # Threshold for an optimal value, it may vary depending on the image.

    #image[copy_dst > 0.01 * copy_dst.max()] = [0, 0, 255]

    # Now draw them
    res = np.hstack((centroids, corners))
    res = np.int0(res)
    errors = 0
    try:
        image[res[:, 1], res[:, 0]] = [0, 0, 255]
        image[res[:, 3], res[:, 2]] = [0, 255, 0]
    except:
        errors = errors + 1
        # print("A detected keypoint was not part of the image - ignoring point.")
    cv2.imshow('dst', image)

    result = gray
    return result


def detect_corners2(gray: np.ndarray, image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    crop_image = image[0:crop_value_from_top]
    blur_image = cv2.bilateralFilter(crop_image, 5, 20, 20)
    canny_image = cv2.Canny(blur_image, 50, 200, 3)
    kernel = kernel = np.ones((30,30),np.uint8)
    canny_image = cv2.morphologyEx(canny_image, cv2.MORPH_CLOSE, kernel)
    cv2.imshow('canny', canny_image)
    result = np.copy(image)
    result2 = np.copy(image)

    contours, hierarchy = cv2.findContours(canny_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #print(hierarchy)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:100]
    cv2.drawContours(result2, contours, -1, (0, 255, 0), 3)
    cv2.imshow('Contours', result2)

    contours_poly = [None]*len(contours)
    bound_rect = [None]*len(contours)
    centers = [None]*len(contours)
    radius = [None]*len(contours)
    for i, c in enumerate(contours):
        contours_poly[i] = cv2.approxPolyDP(c, 2, True)
        bound_rect[i] = cv2.boundingRect(contours_poly[i])
        centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])

    drawing = np.zeros(gray.shape, np.uint8)

    for i in range(len(contours)):
        #color = (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
        cv2.drawContours(drawing, contours_poly, i, (255,255,255))
        #cv2.rectangle(drawing, (int(bound_rect[i][0]), int(bound_rect[i][1])), \
        #             (int(bound_rect[i][0] + bound_rect[i][2]), int(bound_rect[i][1] + bound_rect[i][3])), color, 2)
        #cv2.circle(drawing, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, 2)

    mask = np.zeros_like(image)  # Create mask where white is what we want, black otherwise
    cv2.drawContours(mask, contours, 1, 255, -1)  # Draw filled contour in mask
    out = np.zeros_like(image)  # Extract out the object and place into output image
    out[mask == 255] = image[mask == 255]
    cv2.imshow('test', out)
    cv2.imshow('Contours', drawing)

    # new_rect = np.ndarray
    # for i, rect in enumerate(bound_rect):
    #     print('rect', rect)
    #     mask = cv2.copyMakeBorder(canny_image, 1, 1, 1, 1, cv2.BORDER_CONSTANT, 0)
    #     seed_point = (int(np.around((rect[0] + rect[1]) / 2, decimals=0)), int(np.around((rect[2] + rect[3]) / 2, decimals=0)))
    #     print(seed_point)
    #     #if (seed_point)
    #     cv2.floodFill(canny_image, mask, seed_point, 255)

    #cv2.imshow('after floodfill', canny_image)

    lines = cv2.HoughLinesP(drawing, rho=1, theta=np.pi/180, threshold=40, minLineLength=5, maxLineGap=20)

    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(result, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return result, lines


def get_building_corners(counter:int, image: np.ndarray, lines: np.ndarray) -> np.ndarray:

    result = np.copy(image)
    vertical_lines = []
    # Check if vertical
    for line in lines:
        #print(line)
        # Check if lines are vertical
        for x1, y1, x2, y2 in line:
            if x1-5 < x2 < x1+5:
                vertical_lines.append(line)

    points = []
    for line in vertical_lines:
        for x1, y1, x2, y2 in line:
            # Ignore Lines at the image borders
            if x1 != 0 and x1 != image.shape[0] and x1 != 0 and x1 != image.shape[0]:
                cv2.line(result, (x1, y1), (x2, y2), (0, 255, 0), 2)
                points.append(np.array([x1, y1]))
                points.append(np.array([x2, y2]))

    cv2.imshow('Vertical Lines', result)
    #cv2.imwrite('images//image'+str(counter)+'.jpg', result)

    return vertical_lines