"""
Copyright (C) 2025 Fu Tszkok

:module: Project 04-04
:function: Highpass Filtering Using a Lowpass Image
:author: Fu Tszkok
:date: 2025-02-01
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import copy
import fft2d
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def gaussian_lowpass(image, D0):
    """Generates a Gaussian lowpass filter kernel for the frequency domain.
    :param image: The input image (used to determine filter dimensions).
    :param D0: The cutoff frequency, where the filter's magnitude is 0.607 of its maximum value.
    :return: A 2D NumPy array representing the Gaussian lowpass filter kernel.
    """
    row, col = image.shape
    # Determine the center of the frequency spectrum.
    u0, v0 = row // 2, col // 2
    H = np.zeros((row, col))

    for i in range(row):
        for j in range(col):
            # Calculate the Euclidean distance from the center of the spectrum.
            D = np.sqrt((i - u0) ** 2 + (j - v0) ** 2)
            # Apply the Gaussian filter formula.
            H[i, j] = np.exp(-(D ** 2) / (2 * D0 ** 2))
    return H


# Load the grayscale image and convert it to float64 for numerical stability.
image = cv.imread('../../images/ray_traced_bottle_original.bmp', cv.IMREAD_GRAYSCALE)
image = np.array(image, dtype=np.float64)

# Display the original image.
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

# Define a list of cutoff frequencies to demonstrate the filter's effect.
D0_values = [5, 15, 30, 80, 230, 511]

# Iterate through each cutoff frequency to apply the high-pass filter.
for D0 in D0_values:
    # 1. Apply the Gaussian low-pass filter and get the blurred image result.
    flat, _ = fft2d.fft2d(copy.deepcopy(image), gaussian_lowpass, D0)

    # 2. Get the original image after it passes through the FFT/IFFT cycle with no filtering.
    real, _ = fft2d.fft2d(copy.deepcopy(image))

    # 3. Subtract the low-pass result from the unfiltered image to get the high-pass result.
    # The absolute value is taken to ensure all pixel values are non-negative.
    result = np.abs(np.int64(real - flat))

    # Display the high-pass filtered image.
    plt.axis('off')
    plt.imshow(result, cmap='gray')
    plt.title(f'Gaussian High-pass Filtered Image (D$_0$={D0})')
    plt.show()

    # Calculate and print the average pixel value of the high-pass result.
    print(f'Average values of {D0} = {np.sum(result) / (result.shape[0] * result.shape[1])}')
