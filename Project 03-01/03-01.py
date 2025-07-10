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

image = cv.imread('../data/spine.bmp', cv.IMREAD_GRAYSCALE)
image = np.float64(image)
plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title("Original Image")
plt.show()

# Experiment of Log Transformation
C = [15, 30, 45]
for c in C:
    result = np.zeros((image.shape[0], image.shape[1]))
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            result[i, j] = c * math.log(1 + image[i, j])
    plt.axis('off')
    plt.imshow(result, cmap='gray', vmin=0, vmax=255)
    plt.title(f"c={c} Logarithmic Image")
    plt.show()

# Experiment of Power-law Transformation
C = [5, 10, 15]
Gamma = [0.6, 0.4, 0.3]
for c in C:
    for gamma in Gamma:
        result = np.zeros((image.shape[0], image.shape[1]))
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                result[i, j] = c * math.pow(image[i, j], gamma)
        plt.axis('off')
        plt.imshow(result, cmap='gray', vmin=0, vmax=255)
        plt.title(f"c={c}, γ={gamma} Power-law Image")
        plt.show()
