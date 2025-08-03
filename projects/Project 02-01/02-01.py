"""
Copyright (C) 2025 Fu Tszkok

:module: Project 02-01
:function: Image Printing Program Based on Halftoning
:author: Fu Tszkok
:date: 2025-01-28
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# Define a 3x3x10 dot matrix for halftoning patterns.
# Each slice `dot[:, :, n]` represents a 3x3 pixel pattern for a specific gray level (0-9).
# These patterns simulate varying intensities of black dots on a white background.
dot = np.zeros((3, 3, 10))
dot[:, :, 1] = [[0, 255, 0], [0, 0, 0], [0, 0, 0]]
dot[:, :, 2] = [[0, 255, 0], [0, 0, 0], [0, 0, 255]]
dot[:, :, 3] = [[255, 255, 0], [0, 0, 0], [0, 0, 255]]
dot[:, :, 4] = [[255, 255, 0], [0, 0, 0], [255, 0, 255]]
dot[:, :, 5] = [[255, 255, 255], [0, 0, 0], [255, 0, 255]]
dot[:, :, 6] = [[255, 255, 255], [0, 0, 255], [255, 0, 255]]
dot[:, :, 7] = [[255, 255, 255], [0, 0, 255], [255, 255, 255]]
dot[:, :, 8] = [[255, 255, 255], [255, 0, 255], [255, 255, 255]]
dot[:, :, 9] = [[255, 255, 255], [255, 255, 255], [255, 255, 255]]


def adaption(image):
    """
    Adjusts image size to fit specific dimension constraints.
    :param image: Input grayscale image (NumPy array).
    :return: Resized image (NumPy array).
    """
    row, col = image.shape
    # Calculate scaling factors based on a target size (816/3 x 1056/3).
    rscale = row / (816 / 3)
    cscale = col / (1056 / 3)
    # Determine the overall scaling factor to fit within the target dimensions.
    scale = 1 / max(cscale, rscale)
    # Resize the image using the calculated scale.
    result = cv.resize(image, (0, 0), None, scale, scale)
    return result


def halftoning(image):
    """
    Converts a grayscale image into a halftoned image.
    :param image: Input grayscale image (NumPy array), typically with pixel values from 0-255.
    :return: The halftoned image (NumPy array), which is 3 times larger than the original image.
    """
    # Normalize image pixel values to a range of 0-9 for dot matrix lookup.
    image = np.floor(np.double(image) / 25.6)
    row, col = image.shape
    # Initialize an empty canvas for the halftoned image, 3 times larger than the original.
    result = np.zeros((row * 3, col * 3))
    # Iterate through each pixel of the original image.
    for i in range(row):
        for j in range(col):
            # Place the corresponding dot matrix pattern based on the pixel's intensity.
            result[i*3:i*3+3, j*3:j*3+3] = dot[:, :, int(image[i, j])]
    return result


# Process Lenna_face.bmp
image = cv.imread('../../images/Lenna_face.bmp', cv.IMREAD_GRAYSCALE)
row, col = image.shape
# Adapt image size if it exceeds the specified dimensions.
if (row > (816 / 3)) or (col > (1056 / 3)):
    image = adaption(image)
result = halftoning(image)

# Display original Lenna image
plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title("Original Image (Lenna)")
plt.show()

# Display halftoned Lenna image
plt.axis('off')
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title("Halftoning Image (Lenna)")
plt.show()


# Process cameraman.bmp
image = cv.imread('../../images/cameraman.bmp', cv.IMREAD_GRAYSCALE)
row, col = image.shape
# Adapt image size if it exceeds the specified dimensions.
if (row > (816 / 3)) or (col > (1056 / 3)):
    image = adaption(image)
result = halftoning(image)

# Display original Cameraman image
plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title("Original Image (Cameraman)")
plt.show()

# Display halftoned Cameraman image
plt.axis('off')
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title("Halftoning Image (Cameraman)")
plt.show()


# Process crowd.bmp
image = cv.imread('../../images/crowd.bmp', cv.IMREAD_GRAYSCALE)
row, col = image.shape
# Adapt image size if it exceeds the specified dimensions.
if (row > (816 / 3)) or (col > (1056 / 3)):
    image = adaption(image)
result = halftoning(image)

# Display original Crowd image
plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title("Original Image (Crowd)")
plt.show()

# Display halftoned Crowd image
plt.axis('off')
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title("Halftoning Image (Crowd)")
plt.show()


# Generate and process a grayscale wedge image
image = np.zeros((256, 256))
for i in range(256):
    image[:, i] = i
result = halftoning(image)

# Display original Gray Scale Wedge image
plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title("Original Image (Gray Scale Wedge)")
plt.show()

# Display halftoned Gray Scale Wedge image
plt.axis('off')
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title("Halftoning Image (Gray Scale Wedge)")
plt.show()
