"""
Copyright (C) 2025 Fu Tszkok

:module: histogram
:function: The function package from Project 03-02 Histogram Equalization
:author: Fu Tszkok
:date: 2025-01-28
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import copy

import matplotlib.pyplot as plt
import numpy as np


def histogram(image):
    """Calculates the histogram of a grayscale image.
    :param image: Input grayscale image (NumPy array).
    :return: A tuple containing the counts of each grayscale level and the levels themselves.
    """
    x = [i for i in range(256)]  # Create a list of grayscale levels from 0 to 255.
    count = np.zeros(256)  # Initialize an array to store the counts of each level.
    for i in range(256):
        count[i] = np.sum(image == i)  # Count the number of pixels with value 'i'.
    return count, x


def equalization(image):
    """Performs histogram equalization on a grayscale image.
    :param image: Input grayscale image (NumPy array).
    :return: The equalized image (NumPy array).
    """
    row, col = image.shape
    count, x = histogram(image)  # Get the histogram of the original image.
    count = np.double(count) / (row * col)  # Normalize the histogram to get the probability of each level.

    # Calculate the cumulative distribution function (CDF).
    equal = np.zeros(256)
    for i in range(256):
        for j in range(i + 1):
            equal[i] += count[j]

    # Scale the CDF to the range [0, 255].
    equal = np.round(equal * 255)

    # Re-scale the transformation function to span the full range [0, 255].
    trans = np.zeros(256)
    diff = int(np.max(equal) - np.min(equal))
    for i in range(256):
        trans[i] = (equal[i] - np.min(equal)) * 255 / diff

    # Plot the histogram equalization transformation function.
    plt.plot(x, trans, '-', color='blue')
    plt.xlim([0, 255])
    plt.ylim([0, 255])
    plt.title('Histogram Equalization Transformation Function')
    plt.show()

    # Apply the transformation function to the image.
    result = copy.deepcopy(image)
    for i in range(256):
        result[image == i] = trans[i]
    return result
