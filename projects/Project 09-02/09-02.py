"""
Copyright (C) 2025 Fu Tszkok

:module: Project 09-02
:function: Boundary Extraction [Multiple Uses]
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
import set_operations
import matplotlib.pyplot as plt


def boundary_extraction(image):
    """Extracts the boundary of objects in a binary image.
    :param image: Input binary image (NumPy array).
    :return: The resulting binary image containing only the boundaries.
    """
    # First, perform an erosion operation on the binary image.
    erosion = set_operations.erosion(image, np.ones((3, 3), np.uint8))
    # Then, calculate the difference between the original image and the eroded image to obtain the boundary.
    boundary = set_operations.difference(image, erosion)
    return boundary


# Load the image, convert it to grayscale, and then apply a binary threshold.
image = cv.imread('../../images/text_image.bmp', cv.IMREAD_GRAYSCALE)
_, binary_image = cv.threshold(image, 127, 255, cv.THRESH_BINARY)
plt.axis('off')
plt.imshow(binary_image, cmap='gray')
plt.title('Original Binary Image')
plt.show()

# Call the boundary extraction function to get the object boundaries.
boundary = boundary_extraction(binary_image)
plt.axis('off')
plt.imshow(boundary, cmap='gray')
plt.title('Boundary Binary Image')
plt.show()
