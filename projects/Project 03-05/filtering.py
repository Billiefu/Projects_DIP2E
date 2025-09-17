"""
Copyright (C) 2025 Fu Tszkok

:module: filtering
:function: The function package from Project 03-04 Spatial Filtering
:author: Fu Tszkok
:date: 2025-02-01
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import numpy as np


def filtering(image, core=None):
    """
    Applies spatial filtering (convolution) to a grayscale image using a 3x3 kernel.

    This function performs convolution by padding the image, then iterating through
    each pixel to calculate the new value based on the weighted sum of its neighbors.
    The default kernel is a 3x3 averaging filter.

    :param image: Input grayscale image (NumPy array).
    :param core: A 3x3 kernel (list of lists or NumPy array) to use for filtering.
                 Defaults to a 3x3 averaging kernel.
    :return: The filtered image (NumPy array).
    """
    # Define a default averaging kernel if no core is provided.
    if core is None:
        core = [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]

    # Pad the image with a one-pixel border (zero-padding) to handle edges.
    matrix = np.zeros((image.shape[0] + 2, image.shape[1] + 2), dtype=np.float64)
    result = np.zeros((image.shape[0], image.shape[1]), dtype=np.float64)

    # Copy the original image data into the center of the padded matrix.
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            matrix[i + 1, j + 1] = image[i, j]

    # Perform the convolution operation by iterating through each pixel.
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # Calculate the weighted sum of the 3x3 neighborhood.
            result[i, j] = (matrix[i, j] * core[2][2] + matrix[i+1, j] * core[1][2] + matrix[i+2, j] * core[0][2] +
                            matrix[i, j+1] * core[2][1] + matrix[i+1, j+1] * core[1][1] + matrix[i+2, j+1] * core[0][1] +
                            matrix[i, j+2] * core[2][0] + matrix[i+1, j+2] * core[1][0] + matrix[i+2, j+2] * core[0][0])

    return result
