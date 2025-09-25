"""
Copyright (C) 2025 Fu Tszkok

:module: set_operations
:function: The function package from Project 09-01 Morphological and Other Set Operations
:author: Fu Tszkok
:date: 2025-02-06
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import numpy as np


def dilation(binary_image, struct_elem):
    """Performs a dilation operation on a binary image.
    :param binary_image: Input binary image (NumPy array).
    :param struct_elem: The structuring element (NumPy array) used for the operation.
    :return: The dilated binary image.
    """
    struct_elem = np.array(struct_elem)
    pad_h, pad_w = struct_elem.shape[0] // 2, struct_elem.shape[1] // 2
    # Pad the image to handle boundary pixels correctly.
    padded_image = np.pad(binary_image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    result = np.zeros_like(binary_image)

    # Iterate over each pixel of the original image.
    for i in range(binary_image.shape[0]):
        for j in range(binary_image.shape[1]):
            # Extract the region of interest (ROI) centered at the current pixel.
            region = padded_image[i:i + struct_elem.shape[0], j:j + struct_elem.shape[1]]
            # If the ROI contains any white pixel where the structuring element also has a 1,
            # set the result pixel to 1. This is a logical OR operation.
            if np.any(region & struct_elem):
                result[i, j] = 1

    return result


def erosion(binary_image, struct_elem):
    """Performs an erosion operation on a binary image.
    :param binary_image: Input binary image (NumPy array).
    :param struct_elem: The structuring element (NumPy array) used for the operation.
    :return: The eroded binary image.
    """
    struct_elem = np.array(struct_elem)
    pad_h, pad_w = struct_elem.shape[0] // 2, struct_elem.shape[1] // 2
    # Pad the image to handle boundary pixels.
    padded_image = np.pad(binary_image, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    result = np.zeros_like(binary_image)

    # Iterate over each pixel of the original image.
    for i in range(binary_image.shape[0]):
        for j in range(binary_image.shape[1]):
            # Extract the region of interest (ROI) centered at the current pixel.
            region = padded_image[i:i + struct_elem.shape[0], j:j + struct_elem.shape[1]]
            # If the ROI contains only white pixels where the structuring element has a 1,
            # set the result pixel to 1. This is a logical AND operation.
            if np.all(region & struct_elem):
                result[i, j] = 1

    return result


def union(image1, image2):
    """Performs a pixel-wise logical OR (union) on two binary images.
    :param image1: The first binary image.
    :param image2: The second binary image.
    :return: The resulting image of the union operation.
    """
    return np.maximum(image1, image2)


def intersection(image1, image2):
    """Performs a pixel-wise logical AND (intersection) on two binary images.
    :param image1: The first binary image.
    :param image2: The second binary image.
    :return: The resulting image of the intersection operation.
    """
    return np.minimum(image1, image2)


def difference(image1, image2):
    """Performs a pixel-wise logical difference (A AND NOT B) on two binary images.
    :param image1: The first binary image (minuend).
    :param image2: The second binary image (subtrahend).
    :return: The resulting image of the difference operation.
    """
    return np.where(image2 == 0, image1, 0)


def complement(image):
    """Performs a pixel-wise logical NOT (complement) on a binary image.
    :param image: The input binary image.
    :return: The resulting inverted image.
    """
    return 255 - image
