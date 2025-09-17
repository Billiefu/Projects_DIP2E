"""
Copyright (C) 2025 Fu Tszkok

:module: Project 03-04
:function: Spatial Filtering [Multiple Uses]
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


# Load images for demonstration.
image1 = cv.imread('../images/wingding-arrow-down.bmp', cv.IMREAD_GRAYSCALE)
image2 = cv.imread('../images/wingding-arrow-up.bmp', cv.IMREAD_GRAYSCALE)

# Display the original images.
plt.axis('off')
plt.imshow(image1, cmap='gray')
plt.title('Original Image 1')
plt.show()

plt.axis('off')
plt.imshow(image2, cmap='gray')
plt.title('Original Image 2')
plt.show()

# Define kernels for different filtering effects.
# Laplace kernel for edge detection.
laplace_kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]])
# Gaussian-like kernel (often called "Cassette" in some contexts) for blurring.
gaussian_kernel = np.array([[1/16, 2/16, 1/16], [2/16, 4/16, 2/16], [1/16, 2/16, 1/16]])

# Apply custom filtering function with the defined kernels.
result1 = filtering(image1, laplace_kernel)
result2 = filtering(image1, gaussian_kernel)

# Apply OpenCV's built-in filter for comparison.
# The borderType=cv.BORDER_CONSTANT parameter ensures zero-padding for a fair comparison.
true1 = cv.filter2D(image1, -1, laplace_kernel, borderType=cv.BORDER_CONSTANT)
true2 = cv.filter2D(image1, -1, gaussian_kernel, borderType=cv.BORDER_CONSTANT)

# Calculate the absolute difference (loss) between custom and OpenCV results.
loss1 = np.abs(np.float64(true1) - np.float64(result1))
loss2 = np.abs(np.float64(true2) - np.float64(result2))

# Print the average loss for each filtering operation.
print(f"Average Loss1 (Laplace): {np.mean(loss1)}")
print(f"Average Loss2 (Gaussian): {np.mean(loss2)}")
print()

# Display the filtered images from the custom function.
plt.axis('off')
plt.imshow(result1, cmap='gray')
plt.title('Custom Filtered Image (Laplace)')
plt.show()

plt.axis('off')
plt.imshow(result2, cmap='gray')
plt.title('Custom Filtered Image (Gaussian)')
plt.show()

# Display the filtered images from OpenCV.
plt.axis('off')
plt.imshow(true1, cmap='gray')
plt.title('OpenCV Filtered Image (Laplace)')
plt.show()

plt.axis('off')
plt.imshow(true2, cmap='gray')
plt.title('OpenCV Filtered Image (Gaussian)')
plt.show()

# Display the loss images to visualize the difference.
plt.axis('off')
plt.imshow(loss1, cmap='gray')
plt.title('Loss Image (Laplace)')
plt.show()

plt.axis('off')
plt.imshow(loss2, cmap='gray')
plt.title('Loss Image (Gaussian)')
plt.show()
