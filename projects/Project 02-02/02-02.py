"""
Copyright (C) 2025 Fu Tszkok

:module: Project 02-02
:function: Reducing the Number of Gray Levels in an Image
:author: Fu Tszkok
:date: 2025-01-28
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import cv2 as cv
import matplotlib.pyplot as plt

# Load a grayscale image from the specified path
image = cv.imread('../../images/ctskull-256.bmp', cv.IMREAD_GRAYSCALE)

# Display the original image
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title("Original Image")
plt.show()

# Initialize the current grayscale level. For an 8-bit image, it starts at 256 levels (0-255).
grayscale = 256

# Iterate 7 times to progressively reduce grayscale levels
for k in range(7):
    # Iterate through each pixel of the image
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # Divide each pixel value by 2, effectively reducing the number of grayscale levels
            image[i, j] /= 2

    # Update the displayed grayscale level count
    grayscale /= 2
    # Display the image with reduced grayscale levels
    plt.axis('off')
    plt.imshow(image, cmap='gray')
    plt.title(f"Grayscale {grayscale} Image")
    plt.show()
