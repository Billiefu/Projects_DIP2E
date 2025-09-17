"""
Copyright (C) 2025 Fu Tszkok

:module: Project 04-05
:function: Correlation in the Frequency Domain
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
    # This operation is required for frequency-domain correlation.
    for i in range(template.shape[0]):
        for j in range(template.shape[1]):
            f_template[i, j] = np.conjugate(f_template[i, j])
    return f_template


# Load the main image and the template.
image = cv.imread('../../images/UTK.bmp', cv.IMREAD_GRAYSCALE)
template = cv.imread('../../images/letterT.bmp', cv.IMREAD_GRAYSCALE)

# Display the original image and template.
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

plt.axis('off')
plt.imshow(template, cmap='gray')
plt.title('Template')
plt.show()

# Get dimensions for padding. The correlation theorem requires padding
# to at least (A+C-1) x (B+D-1) for images of size A x B and C x D.
A, B = image.shape
C, D = template.shape

P = A + C - 1
Q = B + D - 1

# Create expanded images of the required size and pad with zeros.
expanded_image = np.zeros((P, Q), dtype=np.float32)
expanded_image[:A, :B] = image.astype(np.float32)

expanded_template = np.zeros((P, Q), dtype=np.float32)
expanded_template[:C, :D] = template.astype(np.float32)

# Display the padded images.
plt.axis('off')
plt.imshow(expanded_image, cmap='gray')
plt.title('Expanded Original Image')
plt.show()

plt.axis('off')
plt.imshow(expanded_template, cmap='gray')
plt.title('Expanded Template')
plt.show()

# Perform frequency-domain correlation.
# The `fft2d.fft2d` function implicitly handles the multiplication in the
# frequency domain and the inverse FFT.
corr_image, _ = fft2d.fft2d(copy.deepcopy(expanded_image), conjugate, copy.deepcopy(expanded_template))

# Find the maximum value and its position in the correlation image.
# This position corresponds to the location of the best match.
max_value = np.max(corr_image)
max_pos = np.unravel_index(np.argmax(corr_image), corr_image.shape)
max_pos = (int(max_pos[0]), int(max_pos[1]))

# Display the correlation function image with a marker at the maximum point.
plt.axis('off')
plt.imshow(corr_image, cmap='gray')
plt.title('Correlation Function Image')
plt.scatter(max_pos[1], max_pos[0], color='red', marker='x', label=f'Max: {max_pos}')
plt.legend()
plt.show()

# Print the coordinates of the best match.
print(f"The maximum position: (x, y) = {max_pos}")
