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


def normalization(image, target_histogram):
    """Normalizes the histogram of an image to match a target histogram.
    :param image: Input grayscale image (NumPy array) to be normalized.
    :param target_histogram: A NumPy array representing the target histogram (e.g., a histogram from another image).
    :return: The normalized image with its histogram matching the target.
    """
    # Calculate the histogram and normalized cumulative distribution function (CDF) of the input image.
    hist, bins = np.histogram(image.flatten(), bins=256, range=[0, 256], density=True)
    cdf = hist.cumsum()
    cdf_normalized = cdf / cdf[-1]

    # Calculate the normalized cumulative distribution function (CDF) of the target histogram.
    target_cdf = target_histogram.cumsum()
    target_cdf_normalized = target_cdf / target_cdf[-1]

    # Create a mapping function (lookup table) based on the CDFs.
    # This interpolates the input image's CDF values to the target histogram's intensity levels.
    mapping = np.interp(cdf_normalized, target_cdf_normalized, np.arange(256))

    # Apply the mapping to the flattened image pixels.
    # This transforms each pixel's intensity value to its new value from the lookup table.
    normalized_image = np.interp(image.flatten(), np.arange(256), mapping)

    # Reshape the array back to the original image dimensions and finalize.
    normalized_image = normalized_image.reshape(image.shape)
    # Clip values to the valid range [0, 255] and convert to uint8 format.
    normalized_image = np.clip(normalized_image, 0, 255).astype(np.uint8)

    return normalized_image
