"""
Copyright (C) 2025 Fu Tszkok

:module: Project 04-05
:function: Correlation in the Frequency Domain (Comparison)
:author: Fu Tszkok
:date: 2025-02-01
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import copy
import fft2d
import bilinear
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def conjugate(image, template):
    """Computes the complex conjugate of the FFT of a template.
    :param image: The main image array (used for dimensions).
    :param template: The template image (the pattern to be found).
    :return: The complex conjugate of the padded template's FFT.
    """
    row, col = image.shape
    template = copy.deepcopy(template)
    # Pad the template to the size of the image using bilinear interpolation.
    template = bilinear.bilinear_interpolation(template, row, col)

    # Center the template for proper FFT calculation.
    for i in range(row):
        for j in range(col):
            template[i, j] = template[i, j] * ((-1) ** (i + j))
    f_template = np.fft.fft2(template)

    # Compute the complex conjugate of the template's FFT.
    for i in range(template.shape[0]):
        for j in range(template.shape[1]):
            f_template[i, j] = np.conjugate(f_template[i, j])
    return f_template


def gaussian_lowpass(image, D0):
    """Generates a Gaussian lowpass filter kernel for the frequency domain.
    :param image: The input image (used to determine filter dimensions).
    :param D0: The cutoff frequency, where the filter's magnitude is 0.607 of its maximum value.
    :return: A 2D NumPy array representing the Gaussian lowpass filter kernel.
    """
    row, col = image.shape
    # Determine the center of the frequency spectrum.
    u0, v0 = row // 2, col // 2
    H = np.zeros((row, col))

    for i in range(row):
        for j in range(col):
            # Calculate the Euclidean distance from the center of the spectrum.
            D = np.sqrt((i - u0) ** 2 + (j - v0) ** 2)
            # Apply the Gaussian filter formula.
            H[i, j] = np.exp(-(D ** 2) / (2 * D0 ** 2))
    return H


# Load the main image and the template.
image = cv.imread('../../images/crowd.bmp', cv.IMREAD_GRAYSCALE)
template = cv.imread('../../images/face.bmp', cv.IMREAD_GRAYSCALE)

# Display the original image and template.
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

plt.axis('off')
plt.imshow(template, cmap='gray')
plt.title('Template')
plt.show()

# Get dimensions for zero-padding.
A, B = image.shape
C, D = template.shape

P = A + C - 1
Q = B + D - 1

# Create expanded images of the required size and pad with zeros.
expanded_image = np.zeros((P, Q), dtype=np.float32)
expanded_image[:A, :B] = image.astype(np.float32)

expanded_template = np.zeros((P, Q), dtype=np.float32)
expanded_template[:C, :D] = template.astype(np.float32)

# Further pad dimensions to the next power of 2 for efficient FFT computation.
if (P & (P - 1)) != 0 or (Q & (Q - 1)) != 0:
    P = 2 ** np.ceil(np.log2(P)).astype(int)
    Q = 2 ** np.ceil(np.log2(Q)).astype(int)
    expanded_image = bilinear.bilinear_interpolation(expanded_image, P, Q)
    expanded_template = bilinear.bilinear_interpolation(expanded_template, P, Q)

# Display the padded images.
plt.axis('off')
plt.imshow(expanded_image, cmap='gray')
plt.title('Expanded Original Image')
plt.show()

plt.axis('off')
plt.imshow(expanded_template, cmap='gray')
plt.title('Expanded Template')
plt.show()

# Calculate the baseline correlation on the unfiltered image.
corr_image, _ = fft2d.fft2d(copy.deepcopy(expanded_image), conjugate, copy.deepcopy(expanded_template))
max_value = np.max(corr_image)
max_pos = np.unravel_index(np.argmax(corr_image), corr_image.shape)
max_pos = (int(max_pos[0]), int(max_pos[1]))

# Loop through different cutoff frequencies (D0) to analyze filtering effects.
for i in range(12):
    # --- 1. Correlation on Smoothed (Low-pass) Images ---
    # Apply Gaussian low-pass filter to both the image and the template.
    expanded_image_smooth, _ = fft2d.fft2d(copy.deepcopy(expanded_image), gaussian_lowpass, i + 1)
    expanded_template_smooth, _ = fft2d.fft2d(copy.deepcopy(expanded_template), gaussian_lowpass, i + 1)
    # Perform correlation on the smoothed images.
    corr_image_smooth, _ = fft2d.fft2d(expanded_image_smooth, conjugate, expanded_template_smooth)
    max_value_smooth = np.max(corr_image_smooth)
    max_pos_smooth = np.unravel_index(np.argmax(corr_image_smooth), corr_image_smooth.shape)
    max_pos_smooth = (int(max_pos_smooth[0]), int(max_pos_smooth[1]))

    # --- 2. Correlation on Sharpened (High-pass) Images ---
    # Get the unfiltered versions for subtraction.
    expanded_image_unfiltered, _ = fft2d.fft2d(copy.deepcopy(expanded_image))
    expanded_template_unfiltered, _ = fft2d.fft2d(copy.deepcopy(expanded_template))
    # Subtract the low-pass result from the unfiltered image to get the high-pass result.
    expanded_image_sharp = np.abs(np.int64(np.floor(np.abs(np.float64(expanded_image_unfiltered) - np.float64(expanded_image_smooth)))))
    expanded_template_sharp = np.abs(np.int64(np.floor(np.abs(np.float64(expanded_template_unfiltered) - np.float64(expanded_template_smooth)))))
    # Perform correlation on the sharpened images.
    corr_image_sharp, _ = fft2d.fft2d(copy.deepcopy(expanded_image_sharp), conjugate, copy.deepcopy(expanded_template_sharp))
    max_value_sharp = np.max(corr_image_sharp)
    max_pos_sharp = np.unravel_index(np.argmax(corr_image_sharp), corr_image_sharp.shape)
    max_pos_sharp = (int(max_pos_sharp[0]), int(max_pos_sharp[1]))

    # --- 3. Visualization and Output ---
    plt.axis('off')
    plt.imshow(corr_image, cmap='gray')
    plt.title(f'Correlation Function Image (D0 = {i+1})')
    # Plot markers for the best match locations of all three methods for comparison.
    plt.scatter(max_pos[1], max_pos[0], color='green', marker='x', label=f'Max: {max_pos}')
    plt.scatter(max_pos_smooth[1], max_pos_smooth[0], color='blue', marker='x', label=f'Max_Smooth: {max_pos_smooth}')
    plt.scatter(max_pos_sharp[1], max_pos_sharp[0], color='red', marker='x', label=f'Max_Sharp: {max_pos_sharp}')
    plt.legend()
    plt.show()

    # Print the coordinates of the best match for each method.
    print(f"D0 = {i+1}")
    print(f"The maximum position: (x, y) = {max_pos}")
    print(f"The smoothed maximum position: (x, y) = {max_pos_smooth}")
    print(f"The sharpening maximum position: (x, y) = {max_pos_sharp}")
    print()
