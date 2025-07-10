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

image = cv.imread('../data/ctskull-256.bmp', cv.IMREAD_GRAYSCALE)
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title("Original Image")
plt.show()

grayscale = 256
for k in range(7):
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            image[i, j] /= 2

    grayscale /= 2
    plt.axis('off')
    plt.imshow(image, cmap='gray')
    plt.title(f"Grayscale {grayscale} Image")
    plt.show()
