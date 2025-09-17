"""
Copyright (C) 2025 Fu Tszkok

:module: Project 05-02
:function: Noise Reduction Using a Median Filter
:author: Fu Tszkok
:date: 2025-02-06
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import noise
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def median_filtering(image):
    """Applies a 3x3 median filter to a grayscale image.
    :param image: Input grayscale image (NumPy array).
    :return: The median-filtered image.
    """
    # Create a padded matrix to handle image borders. The padding size is 1 pixel.
    matrix = np.zeros((image.shape[0] + 2, image.shape[1] + 2), dtype=np.float64)
    # Create an array to store the filtered result.
    result = np.zeros((image.shape[0], image.shape[1]), dtype=np.float64)

    # Copy the original image content into the padded matrix.
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            matrix[i + 1, j + 1] = image[i, j]

    # Iterate through each pixel of the original image to apply the filter.
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # Calculate the median of the 3x3 neighborhood centered at the current pixel.
            result[i, j] = np.median([matrix[i - 1, j - 1], matrix[i, j - 1], matrix[i + 1, j - 1],
                                     matrix[i - 1, j], matrix[i, j], matrix[i + 1, j],
                                     matrix[i - 1, j], matrix[i, j + 1], matrix[i + 1, j + 1]])

    return result


# Load the original image and display it.
image = cv.imread('../../images/ckt-board.bmp', cv.IMREAD_GRAYSCALE)
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

# Add salt-and-pepper noise to the image and display the noisy result.
noise = noise.salt_pepper(image, 0.2, 0.2)
plt.axis('off')
plt.imshow(noise, cmap='gray')
plt.title('Salt Pepper Noise Image')
plt.show()

# Apply median filtering to the noisy image.
filtered = median_filtering(noise)
plt.axis('off')
plt.imshow(filtered, cmap='gray')
plt.title('Median Filtered Image')
plt.show()

# Calculate the pixel-wise difference (loss) between the original and filtered images.
# This provides a visual and quantitative measure of the filtering effect.
loss = np.abs(np.int64(np.float64(image) - np.float64(filtered)))
print(f'Average Loss: {sum(sum(abs(np.float64(loss)))) / (loss.shape[0] * loss.shape[1])}')
plt.axis('off')
plt.imshow(loss, cmap='gray')
plt.title('Loss Image')
plt.show()
