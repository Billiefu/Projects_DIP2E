"""
Copyright (C) 2025 Fu Tszkok

:module: Project 05-01
:function: Noise Generators [Multiple Uses]
:author: Fu Tszkok
:date: 2025-02-06
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import histogram
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def gaussian(image, mean=0, std=0.05):
    """Adds Gaussian (random) noise to a grayscale image.
    :param image: Input grayscale image (NumPy array).
    :param mean: The mean of the Gaussian distribution.
    :param std: The standard deviation of the Gaussian distribution.
    :return: The image with Gaussian noise applied.
    """
    # Generate random Gaussian noise with the specified mean and standard deviation.
    gaussian_noise = np.random.normal(mean, std, image.shape)
    # Add the noise to the image, scaling it to the [0, 255] range.
    noisy_image = np.array(image, dtype=float) + gaussian_noise * 255
    # Clip pixel values to ensure they remain within the valid range [0, 255].
    noisy_image = np.clip(noisy_image, 0, 255)
    # Convert the image back to an unsigned 8-bit integer format.
    noisy_image = noisy_image.astype(np.uint8)
    return noisy_image


def salt_pepper(image, salt=0.05, pepper=0.05):
    """Adds Salt-and-Pepper (impulsive) noise to a grayscale image.
    :param image: Input grayscale image (NumPy array).
    :param salt: The proportion of pixels to be corrupted with salt noise.
    :param pepper: The proportion of pixels to be corrupted with pepper noise.
    :return: The image with salt-and-pepper noise applied.
    """
    noisy_image = image.copy()
    total_pixels = image.size

    # Add salt noise (white pixels).
    num_salt = int(total_pixels * salt)
    salt_coords = [np.random.randint(0, i - 1, num_salt) for i in image.shape]
    noisy_image[tuple(salt_coords)] = 255

    # Add pepper noise (black pixels).
    num_pepper = int(total_pixels * pepper)
    pepper_coords = [np.random.randint(0, i - 1, num_pepper) for i in image.shape]
    noisy_image[tuple(pepper_coords)] = 0

    return noisy_image


# Load the image and display the original.
image = cv.imread('../../images/test-pattern.bmp', cv.IMREAD_GRAYSCALE)
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

# Calculate and display the histogram of the original image.
count, x = histogram.histogram(image)
plt.bar(x, count)
plt.title('Histogram of Original Image')
plt.show()

# Apply Gaussian noise and display the noisy image and its histogram.
image_gaussian = gaussian(image)
plt.axis('off')
plt.imshow(image_gaussian, cmap='gray')
plt.title('Gaussian Noise Image')
plt.show()

count_gaussian, x_gaussian = histogram.histogram(image_gaussian)
plt.bar(x_gaussian, count_gaussian)
plt.title('Histogram of Gaussian Noise Image')
plt.show()

# Apply Salt-and-Pepper noise and display the noisy image and its histogram.
image_salt_pepper = salt_pepper(image)
plt.axis('off')
plt.imshow(image_salt_pepper, cmap='gray')
plt.title('Salt Pepper Noise Image')
plt.show()

count_salt_pepper, x_salt_pepper = histogram.histogram(image_salt_pepper)
plt.bar(x_salt_pepper, count_salt_pepper)
plt.title('Histogram of Salt Pepper Noise Image')
plt.show()
