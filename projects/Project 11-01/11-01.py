"""
Copyright (C) 2025 Fu Tszkok

:module: Project 11-01
:function: Skeletons
:author: Fu Tszkok
:date: 2025-09-24
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

from matplotlib import pyplot as plt

from set_operations import *
from threshold import *


def get_skeleton(binary_image):
    """Computes the skeleton of a binary image using the distance transform method.
    :param binary_image: Input binary image (NumPy array). Assumes 0 for background, non-zero for foreground.
    :return: The skeletonized binary image. Returns None if the input is not binary.
    """
    # Verify that the input image is binary.
    if len(np.unique(binary_image)) > 2:
        print("Input image is not binary. Please provide a binary image.")
        return None

    h, w = binary_image.shape
    # Initialize the distance transform map. Foreground pixels are set to infinity, background to 0.
    distance_transform = np.where(binary_image > 0, np.inf, 0)

    # Step 1: First Pass (Forward Raster Scan)
    # Computes initial distances by checking top, top-left, top-right, and left neighbors.
    for y in range(h):
        for x in range(w):
            if distance_transform[y, x] != 0:
                min_dist = distance_transform[y, x]
                if x > 0:
                    min_dist = min(min_dist, distance_transform[y, x - 1] + 1)
                if y > 0:
                    min_dist = min(min_dist, distance_transform[y - 1, x] + 1)
                if x > 0 and y > 0:
                    min_dist = min(min_dist, distance_transform[y - 1, x - 1] + np.sqrt(2))
                if x < w - 1 and y > 0:
                    min_dist = min(min_dist, distance_transform[y - 1, x + 1] + np.sqrt(2))
                distance_transform[y, x] = min_dist

    # Step 2: Second Pass (Backward Raster Scan)
    # Refines distances by checking bottom, bottom-left, bottom-right, and right neighbors.
    for y in range(h - 1, -1, -1):
        for x in range(w - 1, -1, -1):
            if distance_transform[y, x] != 0:
                min_dist = distance_transform[y, x]
                if x < w - 1:
                    min_dist = min(min_dist, distance_transform[y, x + 1] + 1)
                if y < h - 1:
                    min_dist = min(min_dist, distance_transform[y + 1, x] + 1)
                if x < w - 1 and y < h - 1:
                    min_dist = min(min_dist, distance_transform[y + 1, x + 1] + np.sqrt(2))
                if x > 0 and y < h - 1:
                    min_dist = min(min_dist, distance_transform[y + 1, x - 1] + np.sqrt(2))
                distance_transform[y, x] = min_dist

    # Step 3: Local Maxima Extraction
    # Initialize the skeleton image.
    skeleton = np.zeros_like(binary_image, dtype=np.uint8)
    # Find pixels that are local maxima in the distance transform.
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            current_dist = distance_transform[y, x]

            is_local_maxima = True
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy == 0 and dx == 0:
                        continue
                    if distance_transform[y + dy, x + dx] > current_dist:
                        is_local_maxima = False
                        break
                if not is_local_maxima:
                    break
            # If a pixel is a local maximum and part of the foreground, it belongs to the skeleton.
            if is_local_maxima and current_dist > 0:
                skeleton[y, x] = 255

    return skeleton


# Load the grayscale image.
image = cv.imread('../../images/chromosome.bmp', cv.IMREAD_GRAYSCALE)

# Convert the grayscale image to a binary image using a global thresholding method.
thresholded_image, _ = global_thresholding(image)

# Compute the skeleton of the binary image.
skeleton_image = get_skeleton(thresholded_image)

# Apply dilation to the skeleton to make it thicker and more visible for visualization.
skeleton_image = dilation(dilation(dilation(skeleton_image, np.ones((3, 3), np.uint8)), np.ones((3, 3), np.uint8)), np.ones((3, 3), np.uint8))

# Display the original, thresholded, and skeletonized images.
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original image')
plt.show()

plt.axis('off')
plt.imshow(thresholded_image, cmap='gray')
plt.title('Thresholded image')
plt.show()

plt.axis('off')
plt.imshow(skeleton_image, cmap='gray')
plt.title('Skeleton image')
plt.show()
