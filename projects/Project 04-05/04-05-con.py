"""
Copyright (C) 2025 Fu Tszkok

:module: Project 04-05
:function: Correlation in the Frequency Domain (Convolution)
:author: Fu Tszkok
:date: 2025-02-01
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

# Load the main image and the template.
image = cv.imread('../../images/crowd.bmp', cv.IMREAD_GRAYSCALE)
template = cv.imread('../../images/attack-on-grandma.bmp', cv.IMREAD_GRAYSCALE)

# Convert images to float32 for accurate numerical computation during convolution.
image = image.astype(np.float32)
template = template.astype(np.float32)

# To perform correlation using convolution, the template must be spatially
# flipped both horizontally and vertically.
flipped_template = np.flipud(np.fliplr(template))

# Perform the convolution.
# `mode='same'` ensures the output size is the same as the input image.
# `boundary='fill'` and `fillvalue=0` pad the edges with zeros.
result = convolve2d(image, flipped_template, mode='same', boundary='fill', fillvalue=0)

# Find the maximum value and its position in the convolution result.
# This position indicates the best match location.
max_value = np.max(result)
max_loc = np.unravel_index(np.argmax(result), result.shape)
max_loc = (int(max_loc[0]), int(max_loc[1]))
print(f"The point value with the highest relevance: {max_value}")
print(f"The position of the point with the highest correlation: {max_loc}")

# Display the original image.
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

# Display the convolution result image, which represents the correlation.
# The brightest point indicates the highest correlation.
plt.axis('off')
plt.imshow(result, cmap='gray')
plt.title('Convolution Result')
plt.show()

# Create a copy of the result image and plot a marker at the best match location.
annotated_image = image.copy()
plt.axis('off')
plt.imshow(result, cmap='gray')
plt.scatter(max_loc[1], max_loc[0], color='red', marker='x', label=f'Max: {max_loc}')
plt.title('Best Match Highlighted')
plt.show()
