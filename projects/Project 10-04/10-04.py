"""
Copyright (C) 2025 Fu Tszkok

:module: Project 10-04
:function: Region Growing
:author: Fu Tszkok
:date: 2025-09-24
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def region_growing(image, seed_point, threshold, initial_mean):
    """Segments a single region from an image using the region growing algorithm.
    :param image: Input grayscale image (NumPy array).
    :param seed_point: A tuple (row, col) representing the starting pixel for the region.
    :param threshold: The maximum allowed difference between a neighbor's pixel value and the initial mean to be included in the region.
    :param initial_mean: The mean intensity of the initial seed patch.
    :return: A binary image (NumPy array) of the segmented region.
    """
    row, col = image.shape
    segmented_image = np.zeros_like(image, dtype=np.uint8)

    # Initialize a list to act as a queue for points to check.
    points_to_check = [seed_point]
    segmented_image[seed_point] = 255

    # Use a set to keep track of visited pixels for efficiency.
    visited = {seed_point}

    # Process pixels from the queue until it is empty.
    while points_to_check:
        current_point = points_to_check.pop(0)
        r, c = current_point

        # Define the 8-connectivity neighbors of the current pixel.
        neighbors = [(r - 1, c - 1), (r - 1, c), (r - 1, c + 1), (r, c - 1), (r, c + 1), (r + 1, c - 1), (r + 1, c), (r + 1, c + 1)]

        for neighbor_r, neighbor_c in neighbors:
            # Check if the neighbor is within image bounds and has not been visited.
            if 0 <= neighbor_r < row and 0 <= neighbor_c < col and (neighbor_r, neighbor_c) not in visited:
                neighbor_pixel_value = image[neighbor_r, neighbor_c]

                # Check the similarity criterion: is the neighbor's value within the threshold?
                if np.abs(neighbor_pixel_value - initial_mean) <= threshold:
                    # If similar, add the neighbor to the segmented region.
                    segmented_image[neighbor_r, neighbor_c] = 255
                    # Add the neighbor to the queue for future checking.
                    points_to_check.append((neighbor_r, neighbor_c))
                    # Mark the neighbor as visited.
                    visited.add((neighbor_r, neighbor_c))

    return segmented_image


def calculate_patch_stats(image_patch):
    """Calculates the mean and standard deviation of a given image patch.
    :param image_patch: A small NumPy array representing a region of the image.
    :return: A tuple containing the mean and standard deviation of the patch.
    """
    mean = np.mean(image_patch)
    std_dev = np.std(image_patch)
    return mean, std_dev


# Load the grayscale image and initialize an empty image for the final combined result.
image = cv.imread('../../images/original_septagon.bmp', cv.IMREAD_GRAYSCALE)
# image = cv.imread('../../images/defective_weld.bmp', cv.IMREAD_GRAYSCALE)

final_segmented_image = np.zeros_like(image, dtype=np.uint8)

# Define seed point and corresponding 'k' value of original_septagon.bmp for adaptive thresholding.
seed_points = [(407, 326)]
k = [1]

# Define seed points and corresponding 'k' values of defective_weld.bmp for adaptive thresholding.
# seed_points = [(254, 138), (245, 205), (252, 294), (239, 441)]
# k = [10, 0.6, 5, 4.5]

# Iterate through each seed point to grow a separate region.
for i, seed_point in enumerate(seed_points):
    # Extract a small patch (11x11) around the current seed point.
    patch = image[seed_point[0] - 5:seed_point[0] + 6, seed_point[1] - 5:seed_point[1] + 6]
    # Calculate the mean and standard deviation of the patch.
    initial_mean, initial_std_dev = calculate_patch_stats(patch)

    # Set the threshold based on the patch's standard deviation and a constant k.
    # This makes the threshold adaptive to the local image statistics.
    threshold = initial_std_dev * k[i]

    # Print the parameters used for the current region.
    print(f"Seed Point: {seed_point}")
    print(f"Initial Patch Mean: {initial_mean:.2f}")
    print(f"Initial Patch Standard Deviation: {initial_std_dev:.2f}")
    print(f"Using Threshold (k): {threshold:.2f}\n")

    # Segment the current region using the region growing algorithm.
    current_segmented_region = region_growing(image, seed_point, threshold, initial_mean)

    # Combine the newly segmented region with the final result using a bitwise OR operation.
    final_segmented_image = cv.bitwise_or(final_segmented_image, current_segmented_region)

# Display the original and the final segmented images.
plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title('Original Image')
plt.show()

plt.axis('off')
plt.imshow(final_segmented_image, cmap='gray', vmin=0, vmax=255)
plt.title('Segmented Image (Multiple Regions)')
plt.show()
