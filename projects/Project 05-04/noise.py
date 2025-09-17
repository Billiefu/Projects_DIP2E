"""
Copyright (C) 2025 Fu Tszkok

:module: noise
:function: The function package from Project 05-01 Noise Generators
:author: Fu Tszkok
:date: 2025-02-06
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import numpy as np


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
    noisy_image = np.array(image, dtype=float) + gaussian_noise
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
