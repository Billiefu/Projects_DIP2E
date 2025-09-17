"""
Copyright (C) 2025 Fu Tszkok

:module: operations
:function: The function package from Project 03-03 Arithmetic Operations
:author: Fu Tszkok
:date: 2025-02-01
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import numpy as np


def addition(image1, image2):
    """Performs pixel-wise addition of two grayscale images.
    Values are clipped to the range [0, 255].

    :param image1: The first input grayscale image (NumPy array).
    :param image2: The second input grayscale image (NumPy array).
    :return: The resulting image after addition (NumPy array).
    """
    # Check if the images have the same dimensions.
    if np.size(image1) != np.size(image2):
        print("Wrong shape! Images must have the same size.")
        return

    # Convert images to a floating-point data type for arithmetic operations.
    matrix1 = np.array(image1, dtype=np.float64)
    matrix2 = np.array(image2, dtype=np.float64)
    result = np.zeros((image1.shape[0], image1.shape[1]), dtype=np.float64)

    # Loop through each pixel and perform addition.
    for i in range(image1.shape[0]):
        for j in range(image1.shape[1]):
            result[i, j] = matrix1[i, j] + matrix2[i, j]
            # Clip the value to the maximum intensity of 255.
            if result[i, j] > 255:
                result[i, j] = 255

    # Convert the result back to an 8-bit unsigned integer type.
    result = np.uint8(result)
    return result


def subtraction(image1, image2):
    """Performs pixel-wise subtraction of two grayscale images.
    Values are clipped to the range [0, 255].

    :param image1: The first input grayscale image (NumPy array).
    :param image2: The second input grayscale image (NumPy array).
    :return: The resulting image after subtraction (NumPy array).
    """
    # Check if the images have the same dimensions.
    if np.size(image1) != np.size(image2):
        print("Wrong shape! Images must have the same size.")
        return

    # Convert images to a floating-point data type for arithmetic operations.
    matrix1 = np.array(image1, dtype=np.float64)
    matrix2 = np.array(image2, dtype=np.float64)
    result = np.zeros((image1.shape[0], image1.shape[1]), dtype=np.float64)

    # Loop through each pixel and perform subtraction.
    for i in range(image1.shape[0]):
        for j in range(image1.shape[1]):
            result[i, j] = matrix1[i, j] - matrix2[i, j]
            # Clip the value to the minimum intensity of 0.
            if result[i, j] < 0:
                result[i, j] = 0

    # Convert the result back to an 8-bit unsigned integer type.
    result = np.uint8(result)
    return result


def multiplication(image1, image2):
    """Performs pixel-wise multiplication of two grayscale images or an image by a scalar.
    The result is normalized to the range [0, 255].

    :param image1: The first input grayscale image (NumPy array).
    :param image2: The second input grayscale image or a scalar integer (NumPy array or int).
    :return: The resulting image after multiplication (NumPy array).
    """
    # Handle the case where image2 is a scalar integer.
    if isinstance(image2, int):
        image2 = np.ones((image1.shape[0], image1.shape[1]), dtype=np.float64) * image2

    # Check if the images have the same dimensions.
    if np.size(image1) != np.size(image2):
        print("Wrong shape! Images must have the same size.")
        return

    # Convert images to a floating-point data type for arithmetic operations.
    matrix1 = np.array(image1, dtype=np.float64)
    matrix2 = np.array(image2, dtype=np.float64)
    result = np.zeros((image1.shape[0], image1.shape[1]), dtype=np.float64)

    # Loop through each pixel and perform multiplication.
    for i in range(image1.shape[0]):
        for j in range(image1.shape[1]):
            result[i, j] = matrix1[i, j] * matrix2[i, j]

    # Normalize the result to the full intensity range [0, 255].
    result = np.floor(result / (np.max(result)) * 255)
    # Convert the result back to an 8-bit unsigned integer type.
    result = np.uint8(result)
    return result


def division(image1, image2):
    """Performs pixel-wise division of two grayscale images or an image by a scalar.
    Handles division by zero by setting the resulting pixel value to 0.

    :param image1: The numerator grayscale image (NumPy array).
    :param image2: The denominator grayscale image or a scalar integer (NumPy array or int).
    :return: The resulting image after division (NumPy array).
    """
    # Handle the case where image2 is a scalar integer.
    if isinstance(image2, int):
        image2 = np.ones((image1.shape[0], image1.shape[1]), dtype=np.float64) * image2

    # Check if the images have the same dimensions.
    if np.size(image1) != np.size(image2):
        print("Wrong shape! Images must have the same size.")
        return

    # Convert images to a floating-point data type for arithmetic operations.
    matrix1 = np.array(image1, dtype=np.float64)
    matrix2 = np.array(image2, dtype=np.float64)
    result = np.zeros((image1.shape[0], image1.shape[1]), dtype=np.float64)

    # Loop through each pixel and perform division.
    for i in range(image1.shape[0]):
        for j in range(image1.shape[1]):
            # Avoid division by zero.
            if matrix2[i, j] != 0:
                result[i, j] = matrix1[i, j] / matrix2[i, j]
            else:
                result[i, j] = 0

    # Convert the result back to an 8-bit unsigned integer type.
    result = np.uint8(result)
    return result
