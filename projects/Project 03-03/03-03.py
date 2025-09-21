"""
Copyright (C) 2025 Fu Tszkok

:module: Project 03-03
:function: Arithmetic Operations [Multiple Uses]
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


# Load images.
image1 = cv.imread('../../images/wingding-arrow-down.bmp', cv.IMREAD_GRAYSCALE)
image2 = cv.imread('../../images/wingding-arrow-up.bmp', cv.IMREAD_GRAYSCALE)

# Display original images.
plt.axis('off')
plt.imshow(image1, cmap='gray')
plt.title('Original Image 1')
plt.show()

plt.axis('off')
plt.imshow(image2, cmap='gray')
plt.title('Original Image 2')
plt.show()

# Perform arithmetic operations using custom functions.
result1 = addition(image1, image2)
result2 = subtraction(image1, image2)
result3 = multiplication(image1, image2)
result4 = division(image1, image2)

# Perform arithmetic operations using OpenCV's built-in functions for comparison.
true1 = cv.add(image1, image2)
true2 = cv.subtract(image1, image2)
true3 = cv.multiply(image1, image2)
true4 = cv.divide(image1, image2)

# Calculate and print the average difference (loss) between custom and OpenCV results.
loss1 = np.float64(true1) - np.float64(result1)
loss2 = np.float64(true2) - np.float64(result2)
loss3 = np.float64(true3) - np.float64(result3)
loss4 = np.float64(true4) - np.float64(result4)
print(f"Addition Average Loss: {sum(sum(abs(loss1))) / (loss1.shape[0] * loss1.shape[1])}")
print(f"Subtraction Average Loss: {sum(sum(abs(loss2))) / (loss2.shape[0] * loss2.shape[1])}")
print(f"Multiplication Average Loss: {sum(sum(abs(loss3))) / (loss3.shape[0] * loss3.shape[1])}")
print(f"Division Average Loss: {sum(sum(abs(loss4))) / (loss4.shape[0] * loss4.shape[1])}")

# Display images from custom functions.
plt.axis('off')
plt.imshow(result1, cmap='gray')
plt.title('Addition Result Image (Custom)')
plt.show()

plt.axis('off')
plt.imshow(result2, cmap='gray')
plt.title('Subtraction Result Image (Custom)')
plt.show()

plt.axis('off')
plt.imshow(result3, cmap='gray')
plt.title('Multiplication Result Image (Custom)')
plt.show()

plt.axis('off')
plt.imshow(result4, cmap='gray')
plt.title('Division Result Image (Custom)')
plt.show()

# Display images from OpenCV's built-in functions.
plt.axis('off')
plt.imshow(true1, cmap='gray')
plt.title('Addition Result Image (OpenCV)')
plt.show()

plt.axis('off')
plt.imshow(true2, cmap='gray')
plt.title('Subtraction Result Image (OpenCV)')
plt.show()

plt.axis('off')
plt.imshow(true3, cmap='gray')
plt.title('Multiplication Result Image (OpenCV)')
plt.show()

plt.axis('off')
plt.imshow(true4, cmap='gray')
plt.title('Division Result Image (OpenCV)')
plt.show()

# Display the loss images.
plt.axis('off')
plt.imshow(loss1, cmap='gray')
plt.title('Addition Loss Image')
plt.show()

plt.axis('off')
plt.imshow(loss2, cmap='gray')
plt.title('Subtraction Loss Image')
plt.show()

plt.axis('off')
plt.imshow(loss3, cmap='gray')
plt.title('Multiplication Loss Image')
plt.show()

plt.axis('off')
plt.imshow(loss4, cmap='gray')
plt.title('Division Loss Image')
plt.show()
