"""
Copyright (C) 2025 Fu Tszkok

:module: Project 06-01
:function: Web-Safe Colors Conversion
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

# Load the original image and convert its color space from BGR to RGB.
image = cv.imread('../../images/RGB-full-color-cube.bmp')
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

# --- Quantize the image colors to the web-safe palette ---
# The six intensity levels for each channel are 0, 51, 102, 153, 204, 255.
# These are multiples of 51. The range 0-255 is divided into 6 bins.
# The step size for each bin is 255 / 6 ≈ 42.5.

# Iterate through each of the three color channels (R, G, B).
for k in range(3):
    # Iterate through each pixel of the image.
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # Determine which of the 6 bins the current pixel's intensity value falls into.
            # This maps the 0-255 range to a discrete index from 0 to 5.
            case = np.floor(image[i, j, k] / 42.5)
            # A value of 255 gets mapped to 6, so we correct it to 5 to stay in the index range.
            if case == 6:
                case = 5
            # Map the index back to the corresponding web-safe intensity level.
            image[i, j, k] = case * 51

# Display the converted image with web-safe colors.
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Converted Image')
plt.show()
