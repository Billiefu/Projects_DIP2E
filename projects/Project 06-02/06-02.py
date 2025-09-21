"""
Copyright (C) 2025 Fu Tszkok

:module: Project 06-02
:function: Pseudo-Color Image Processing
:author: Fu Tszkok
:date: 2025-02-06
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import cv2 as cv
import matplotlib.pyplot as plt

# Load the image in grayscale and color. The grayscale version will be used as a mask
# to determine the intensity values, and the color version will be modified.
mask = cv.imread('../../images/WashingtonDCBand4.bmp', cv.IMREAD_GRAYSCALE)
image = cv.imread('../../images/WashingtonDCBand4.bmp')
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

# Define the threshold for intensity and the color to apply.
# Pixels with an intensity value (from the grayscale mask) less than or equal to
# the threshold will be colored.
threshold = 30
color = [255, 255, 0]  # This color is yellow in RGB.
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        # Check the intensity value of the current pixel in the grayscale mask.
        if mask[i, j] <= threshold:
            # If the condition is met, apply the defined color to the corresponding
            # pixel in the color image.
            image[i, j] = color

# Display the resulting pseudo-color image.
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()
