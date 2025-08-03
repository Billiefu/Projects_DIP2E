"""
Copyright (C) 2025 Fu Tszkok

:module: Project 03-01
:function: Image Enhancement Using Intensity Transformations
:author: Fu Tszkok
:date: 2025-02-01
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import math
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# Load a grayscale image and normalize pixel values to the range [0, 1].
image = cv.imread('../../images/spine.bmp', cv.IMREAD_GRAYSCALE)
image = np.float64(image) / 255.0

# Display the original image
plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=1)
plt.title("Original Image")
plt.show()


# Define the constant 'c' for the logarithmic transformation.
C = [1, 2.5, 5]

# Iterate through different 'c' values to apply the transformation.
for c in C:
    # Initialize a new image array for the result.
    result = np.zeros((image.shape[0], image.shape[1]))
    # Apply the logarithmic transformation to each pixel: s = c * log(1 + r).
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            result[i, j] = c * math.log(1 + image[i, j])

    # Display the transformed image.
    plt.axis('off')
    plt.imshow(result, cmap='gray', vmin=0, vmax=1)
    plt.title(f"c={c} Logarithmic Image")
    plt.show()


# Define constants 'c' and 'gamma' for the power-law transformation.
C = [0.8, 1, 1.5]
Gamma = [1.5, 0.6, 0.4]

# Iterate through different 'c' and 'gamma' values.
for c in C:
    for gamma in Gamma:
        # Initialize a new image array for the result.
        result = np.zeros((image.shape[0], image.shape[1]))
        # Apply the power-law transformation to each pixel: s = c * r^gamma.
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                result[i, j] = c * math.pow(image[i, j], gamma)

        # Display the transformed image.
        plt.axis('off')
        plt.imshow(result, cmap='gray', vmin=0, vmax=1)
        plt.title(f"c={c}, γ={gamma} Power-law Image")
        plt.show()
