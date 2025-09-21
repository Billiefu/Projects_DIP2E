"""
Copyright (C) 2025 Fu Tszkok

:module: Project 10-01
:function: Edge Detection Combined with Smoothing and Thresholding
:author: Fu Tszkok
:date: 2025-02-06
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import filtering
import histogram

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


# Step 1: Pre-processing and Initial Visualization
# Load the grayscale image and convert its data type to float64 for calculations.
image = cv.imread('../../images/headCT-Vandy.bmp', cv.IMREAD_GRAYSCALE)
image = np.float64(image)
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

# Calculate and display the histogram of the original image to show its pixel value distribution.
count, x = histogram.histogram(image)
plt.bar(x, count)
plt.title('Histogram of Original Image')
plt.show()


# Step 2: Edge Detection using Sobel Operator
# Apply a smoothing filter to the image. This is a common pre-processing step
# to reduce noise before applying the Sobel operator.
image = filtering.filtering(image)
# Convolve the image with the Sobel kernels to compute the gradients in the x and y directions.
# Sobel kernel for x-direction: [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
sobel_x = filtering.filtering(image, [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
# Sobel kernel for y-direction: [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
sobel_y = filtering.filtering(image, [[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
# Calculate the gradient magnitude using the formula: $G = \sqrt{G_x^2 + G_y^2}$.
# This combines the horizontal and vertical gradients into a single image.
sobel = np.sqrt(sobel_x ** 2 + sobel_y ** 2)
plt.axis('off')
plt.imshow(sobel, cmap='gray')
plt.title('Gradient Image')
plt.show()


# Step 3: Thresholding and Final Result
# Calculate and display the histogram of the Sobel gradient image. This helps in
# determining an appropriate threshold value for edge detection.
count, x = histogram.histogram(sobel)
plt.bar(x, count)
plt.title('Histogram of Sobel Edges')
plt.show()

# Apply a binary threshold to the gradient magnitude image. Pixels with a
# gradient value greater than T are considered edges and set to 255.
T = 75
_, edges = cv.threshold(sobel, T, 255, cv.THRESH_BINARY)
plt.axis('off')
plt.imshow(edges, cmap='gray')
plt.title('Edges Image')
plt.show()
