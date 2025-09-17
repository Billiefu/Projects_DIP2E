"""
Copyright (C) 2025 Fu Tszkok

:module: Project 05-03
:function: Periodic Noise Reduction Using a Notch Filter
:author: Fu Tszkok
:date: 2025-02-06
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


def sinusoidal_noise(image, A=100, u0=16, v0=16):
    """Adds a sinusoidal noise pattern to a grayscale image.
    :param image: Input grayscale image (NumPy array).
    :param A: The amplitude of the sine wave.
    :param u0: The horizontal frequency component of the sine wave.
    :param v0: The vertical frequency component of the sine wave.
    :return: The image with sinusoidal noise applied.
    """
    M, N = image.shape[0], image.shape[1]
    noisy_image = np.ones((image.shape[0], image.shape[1]))
    # Add the sine wave to each pixel of the image.
    for i in range(M):
        for j in range(N):
            noisy_image[i, j] = image[i, j] + A * np.sin(2 * np.pi * (u0 * i / M + v0 * j / N))
    return noisy_image


def notch_filter(image, parameters):
    """Generates an ideal Butterworth notch filter kernel.
    :param image: The input image (used to determine filter dimensions).
    :param parameters: A list containing [u0, v0, D0], where (u0, v0) are the
                       notch's coordinates relative to the center and D0 is the cutoff.
    :return: A 2D NumPy array representing the notch filter kernel.
    """
    row, col = image.shape
    u0, v0, D0 = parameters
    H = np.zeros((row, col))

    for i in range(row):
        for j in range(col):
            # Calculate the distance from the notch center (u0, v0).
            D1 = np.sqrt((i - row / 2 - u0) ** 2 + (j - col / 2 - v0) ** 2)
            # Calculate the distance from the conjugate notch center (-u0, -v0).
            D2 = np.sqrt((i - row / 2 + u0) ** 2 + (j - col / 2 + v0) ** 2)
            if D1 == 0 or D2 == 0:
                # Avoid division by zero at the exact notch locations.
                H[i, j] = 10 ** -10
            else:
                # Apply the Butterworth notch filter formula.
                H[i, j] = 1 / (1 + ((D0 * D0) / (D1 * D2)) ** 4)
    return H


# Load the original image and pad it to a power-of-2 size for efficient FFT.
image = cv.imread('../../images/DIP.bmp', cv.IMREAD_GRAYSCALE)
image = bilinear.bilinear_interpolation(image, 512, 512)
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

# Display the frequency spectrum of the original image (without noise).
_, spectrum = fft2d.fft2d(copy.deepcopy(image))
plt.axis('off')
plt.imshow(2 * np.log(np.abs(spectrum)), cmap='gray')
plt.title('Frequency Spectrum of Original Image')
plt.show()

# Define sinusoidal noise parameters.
A = 100
u0 = 128
v0 = 0
D0 = 10

# Add sinusoidal noise to the image.
noise_image = sinusoidal_noise(copy.deepcopy(image), A, u0, v0)
plt.axis('off')
plt.imshow(noise_image, cmap='gray')
plt.title('Sinusoidal Noise Image')
plt.show()

# Display the frequency spectrum of the noisy image.
# Note the appearance of two bright spikes corresponding to the noise frequency.
_, noise_spectrum = fft2d.fft2d(copy.deepcopy(noise_image))
plt.axis('off')
plt.imshow(2 * np.log(np.abs(noise_spectrum)), cmap='gray')
plt.title('Frequency Spectrum of Noise Image')
plt.show()

# Apply the notch filter to the noisy image to remove the spikes.
# The filter is passed as a parameter to the `fft2d` function.
denoised_image, denoised_spectrum = fft2d.fft2d(noise_image, notch_filter, [u0, v0, D0])
plt.axis('off')
plt.imshow(denoised_image, cmap='gray')
plt.title('Denoised Image')
plt.show()

# Display the frequency spectrum of the denoised image, showing the removal of the spikes.
plt.axis('off')
plt.imshow(2 * np.log(np.abs(denoised_spectrum)), cmap='gray')
plt.title('Frequency Spectrum of Denoised Image')
plt.show()

# Calculate and display the loss image (the difference between the original and denoised images).
loss = np.abs(np.float64(image) - np.float64(denoised_image))
print(f'Average Loss: {sum(sum(abs(np.float64(loss)))) / (loss.shape[0] * loss.shape[1])}')
plt.axis('off')
plt.imshow(loss, cmap='gray')
plt.title('Loss Image')
plt.show()
