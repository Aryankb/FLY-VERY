import cv2
import numpy as np
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt

def make_cluster(img_path):
# Load the segmented image
    image = cv2.imread(img_path)

    # Define the color range for yellow and dark yellow in HSV
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([30, 255, 255])
    lower_dark_yellow = np.array([15, 100, 100])
    upper_dark_yellow = np.array([25, 255, 255])

    # Convert the image to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Create masks for yellow and dark yellow
    mask_yellow = cv2.inRange(hsv_image, lower_yellow, upper_yellow)
    mask_dark_yellow = cv2.inRange(hsv_image, lower_dark_yellow, upper_dark_yellow)

    # Combine masks
    mask = cv2.bitwise_or(mask_yellow, mask_dark_yellow)

    # Find the coordinates of the land pixels
    land_pixels = np.column_stack(np.where(mask > 0))

    # Apply DBSCAN clustering
    db = DBSCAN(eps=12, min_samples=100).fit(land_pixels)
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)

    print(f'Estimated number of clusters: {n_clusters}')

    # Extract the coordinates of the cluster centers
    cluster_centers = []
    for cluster_id in range(n_clusters):
        cluster_points = land_pixels[labels == cluster_id]
        centroid = cluster_points.mean(axis=0)
        cluster_centers.append(centroid)
        print(f'Centroid of cluster {cluster_id}: {centroid}')

    cluster_centers = np.array(cluster_centers)

    # Plot the clusters
    plt.figure(figsize=(10, 10))
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    for cluster_id in range(n_clusters):
        cluster_mask = (labels == cluster_id)
        cluster_points = land_pixels[cluster_mask]
        plt.scatter(cluster_points[:, 1], cluster_points[:, 0], s=2, label=f'Cluster {cluster_id}')

    # Plot the cluster centers with a unique marker
    for i, center in enumerate(cluster_centers):
        plt.scatter(center[1], center[0], c='red', marker='x', s=100, label=f'Center {i}')

    plt.legend()
    plt.show()

    
        
