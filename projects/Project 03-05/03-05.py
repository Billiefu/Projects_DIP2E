"""
Copyright (C) 2025 Fu Tszkok

:module: Project 03-05
:function: Enhancement Using the Laplacian
:author: Fu Tszkok
:date: 2025-02-01
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import filtering
import operations

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


# Define a list of Laplacian kernels from a reference source, likely a textbook figure (e.g., Gonzalez and Woods, Fig. 3.39).
# These kernels are used to detect edges in different directions.
cores = [[[0, 1, 0], [1, -4, 1], [0, 1, 0]],
         [[1, 1, 1], [1, -8, 1], [1, 1, 1]],
         [[0, -1, 0], [-1, 4, -1], [0, -1, 0]],
         [[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]]]
title = ['a', 'b', 'c', 'd']

# Load the input image.
image = cv.imread("../../images/blurry-moon.bmp", cv.IMREAD_GRAYSCALE)
[row, col] = image.shape

# Display the original image.
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

# Iterate through each Laplacian kernel to perform edge detection and enhancement.
for i in range(4):
    # Apply the custom filtering function to get the edges (Laplacian).
    edges = filtering.filtering(image, cores[i])

    # Display the edges image.
    plt.axis('off')
    plt.imshow(edges, cmap='gray')
    plt.title(f'Edges Image Using Core At Fig 3.39(' + title[i] + ')')
    plt.show()

    # Perform image enhancement by subtracting the Laplacian (edges) from the original image.
    # Note: subtracting the edges from the original image enhances sharpness.
    result = operations.subtraction(image, edges)

    # Display the enhanced result image.
    plt.axis('off')
    plt.imshow(result, cmap='gray')
    plt.title('Result Image Using Core At Fig 3.39(' + title[i] + ')')
    plt.show()

    # For comparison, apply OpenCV's built-in filter2D function.
    tedges = cv.filter2D(image, -1, np.array(cores[i]), cv.BORDER_CONSTANT)

    # Display the edges image from OpenCV.
    plt.axis('off')
    plt.imshow(tedges, cmap='gray')
    plt.title('True Edges Image Using Core At Fig 3.39(' + title[i] + ')')
    plt.show()

    # Enhance the image using OpenCV's subtract function.
    tresult = cv.subtract(image, tedges)

    # Display the enhanced result image from OpenCV.
    plt.axis('off')
    plt.imshow(tresult, cmap='gray')
    plt.title('True Result Image Using Core At Fig 3.39(' + title[i] + ')')
    plt.show()

    # Calculate and display the pixel-wise difference (loss) between the custom and OpenCV results.
    loss = np.abs(np.float64(tresult) - np.float64(result))

    plt.axis('off')
    plt.imshow(loss, cmap='gray')
    plt.title('Loss Image Using Core At Fig 3.39(' + title[i] + ')')

    # Print the average loss for the current kernel.
    print('Average Loss For Core Fig 3.39(' + title[i] + f'): {np.mean(loss)}')

    plt.show()
