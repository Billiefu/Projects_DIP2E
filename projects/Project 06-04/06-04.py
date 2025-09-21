"""
Copyright (C) 2025 Fu Tszkok

:module: Project 06-04
:function: Color Image Segmentation
:author: Fu Tszkok
:date: 2025-02-06
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def segment_color_regions(image, target_color, threshold=10):
    """Segments an image based on the Mahalanobis distance to a target color.
    :param image: Input color image (NumPy array).
    :param target_color: The target color to segment (a list or array of 3 values, e.g., [R, G, B]).
    :param threshold: The maximum Mahalanobis distance for a pixel to be included in the segment.
    :return: A binary mask (NumPy array) highlighting the segmented regions in white.
    """
    # Reshape the image into a 2D array of pixels and ensure float32 data type for calculations.
    pixels = image.reshape(-1, 3).astype(np.float32)
    target_color = np.array(target_color, dtype=np.float32)

    # Calculate the covariance matrix of the pixel colors. The covariance
    # matrix captures the relationships between the R, G, and B color channels.
    cov = np.cov(pixels, rowvar=False)
    # Add a small value to the diagonal for numerical stability, ensuring the matrix is invertible.
    cov += np.eye(cov.shape[0]) * 1e-6
    inv_cov = np.linalg.inv(cov)

    # Calculate the Mahalanobis distance for each pixel. The formula involves
    # the inverse covariance matrix, which normalizes the distance by the
    # variance and correlation of the color channels.
    mahalanobis_distances = np.sqrt(np.sum((pixels - target_color) @ inv_cov * (pixels - target_color), axis=1))
    # Reshape the distances back into a 2D array matching the original image dimensions.
    mahalanobis_distances = mahalanobis_distances.reshape(image.shape[:2])

    # Create a binary mask by thresholding the Mahalanobis distances.
    # Pixels with a distance less than the threshold are set to 255 (white).
    color_mask = np.uint8(mahalanobis_distances < threshold) * 255
    return color_mask


# Load the image and convert its color space from BGR to RGB.
image = cv.imread('../../images/jupiter-Io-closeup.bmp')
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
if image.dtype != np.uint8:
    image = (image * 255).astype(np.uint8)
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

# Define the target color and threshold for segmentation.
# Here, the script segments regions that are close to black [0, 0, 0].
target_color = [0, 0, 0]
color_mask = segment_color_regions(image, target_color, 3)
plt.axis('off')
plt.imshow(color_mask, cmap='gray')
plt.title('Color Mask')
plt.show()
