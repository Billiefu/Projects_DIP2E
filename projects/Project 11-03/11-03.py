"""
Copyright (C) 2025 Fu Tszkok

:module: Project 11-03
:function: Texture
:author: Fu Tszkok
:date: 2025-09-25
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

from histogram import histogram


def compute_measures(image, levels=256):
    """Calculates various statistical measures for image texture.
    :param image: Input single-channel grayscale image (NumPy array).
    :param levels: Number of gray levels (default is 256).
    :return: A dictionary containing the computed statistical measures.
    :raises ValueError: If the input image is not single-channel.
    """
    if image.ndim > 2:
        raise ValueError("The input image must be a single-channel grayscale image.")

    # Get the histogram and total pixel count.
    counts, _ = histogram(image)
    total_pixels = image.size

    if total_pixels == 0:
        return {
            'Mean': 0.0, 'Standard Deviation': 0.0, 'Rel-Smooth': 0.0,
            'Third Moment': 0.0, 'Uniformity': 0.0, 'Entropy': 0.0
        }

    # Calculate the normalized histogram (probability distribution, p).
    p = counts.astype(np.float64) / total_pixels
    # Create an array of intensity values (z).
    z = np.arange(levels, dtype=np.float64)
    measures = {}

    # --- Mean ---
    # $m = \sum z_i p(z_i)$ (Average intensity)
    m = np.sum(z * p)
    measures['Mean'] = m

    # Pre-calculate the difference from the mean for central moments.
    z_minus_m = z - m

    # --- Variance ---
    # $\mu_2 = \sum (z_i - m)^2 p(z_i)$
    mu_2 = np.sum((z_minus_m ** 2) * p)
    # Standard Deviation ($\sigma = \sqrt{\mu_2}$): Measures contrast/spread.
    std_dev = np.sqrt(mu_2)
    measures['Standard Deviation'] = std_dev

    # --- Relative Smoothness ---
    # $R = 1 - \frac{1}{1 + \mu_2}$ (Value approaches 1 for a very rough image).
    R = 1.0 - (1.0 / (1.0 + mu_2))
    measures['Rel-Smooth'] = R

    # --- Third Central Moment ---
    # $\mu_3 = \sum (z_i - m)^3 p(z_i)$ (Measures asymmetry of the histogram).
    mu_3 = np.sum((z_minus_m ** 3) * p)
    measures['Third Moment'] = mu_3

    # --- Uniformity ---
    # $U = \sum p(z_i)^2$ (Measures homogeneity; high U for uniform images).
    U = np.sum(p ** 2)
    measures['Uniformity'] = U

    # --- Entropy ---
    # $H = -\sum p(z_i) \log_2 p(z_i)$ (Measures randomness/complexity; high H for complex images).
    non_zero_indices = p > 0
    p_non_zero = p[non_zero_indices]

    entropy = -np.sum(p_non_zero * np.log2(p_non_zero))
    measures['Entropy'] = entropy

    return measures


def crop(image):
    """Extracts a 100x100 sub-image from the bottom-right corner of the input image.
    :param image: Input grayscale image (NumPy array).
    :return: The cropped sub-image (NumPy array).
    """
    H, W = image.shape

    # Define the starting row and column for a 100x100 crop from the bottom-right.
    start_row = H - 100
    start_col = W - 100

    # Handle cases where the image is smaller than 100x100 (though unlikely for these examples).
    if start_row < 0 or start_col < 0:
        start_row = max(0, start_row)
        start_col = max(0, start_col)

    # Perform the slicing to extract the sub-image.
    sub_image = image[start_row:H, start_col:W]

    return sub_image


# Load the specified grayscale images for texture analysis.
images = {
    'Fig 1.14(a)': cv.imread('../../images/cktboard.bmp', cv.IMREAD_GRAYSCALE),
    'Fig 1.14(d)': cv.imread('../../images/bubbles.bmp', cv.IMREAD_GRAYSCALE),
    'Fig 1.14(e)': cv.imread('../../images/cereal.bmp', cv.IMREAD_GRAYSCALE)
}

measures = {}
# Iterate through each image, crop it, and compute the texture measures.
for name, image in images.items():
    # Crop images
    crop_image = crop(image)

    # Display original image and croped image.
    plt.axis('off')
    plt.imshow(image, cmap='gray')
    plt.title(f'{name} (Original Image)')
    plt.show()

    plt.axis('off')
    plt.imshow(crop_image, cmap='gray')
    plt.title(f'{name} (Crop Image)')
    plt.show()

    # Compute the texture measures
    measures[name] = compute_measures(crop_image)

# Define the header for the results table.
header = "{:<20}{:<15}{:<15}{:<15}{:<15}{:<15}{:<15}".format(
    "Texture", "Mean", "Std.Dev.", "R(Rel-Smooth)", "Third Moment", "Uniformity", "Entropy"
)
separator = "-" * len(header)

print(separator)
print(header)
print(separator)

# Print the computed measures for each image in a formatted table row.
for name, data in measures.items():
    row = "{:<20}{:<15.2f}{:<15.2f}{:<15.4f}{:<15.4f}{:<15.3f}{:<15.3f}".format(
        name, data['Mean'], data['Standard Deviation'], data['Rel-Smooth'], data['Third Moment'],
        data['Uniformity'], data['Entropy']
    )
    print(row)
print(separator)
