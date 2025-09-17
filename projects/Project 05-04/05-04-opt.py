"""
Copyright (C) 2025 Fu Tszkok

:module: Project 05-04
:function: Parametric Wiener Filter (Optimal)
:author: Fu Tszkok
:date: 2025-02-06
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import fft2d
import noise
import bilinear
import filtering

import copy
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def SNR(original, denoised):
    """Calculates the Signal-to-Noise Ratio (SNR) between two images.
    :param original: The original, undegraded image.
    :param denoised: The restored image after filtering.
    :return: The calculated SNR value.
    """
    original = np.array(original, dtype=np.float64)
    denoised = np.array(denoised, dtype=np.float64)

    # Calculate the power of the original signal.
    temp1 = 0
    # Calculate the power of the noise (the difference between the restored and original images).
    temp2 = 0

    for i in range(original.shape[0]):
        for j in range(denoised.shape[1]):
            temp1 += original[i, j] ** 2
            temp2 += (denoised[i, j] - original[i, j]) ** 2

    return temp1 / temp2


def gaussian_lowpass(image, D0):
    """Generates a Gaussian lowpass filter kernel for the frequency domain.
    :param image: The input image (used to determine filter dimensions).
    :param D0: The cutoff frequency.
    :return: A 2D NumPy array representing the Gaussian lowpass filter kernel.
    """
    row, col = image.shape
    u0, v0 = row // 2, col // 2
    H = np.zeros((row, col))

    for i in range(row):
        for j in range(col):
            D = np.sqrt((i - u0) ** 2 + (j - v0) ** 2)
            H[i, j] = np.exp(-(D ** 2) / (2 * D0 ** 2))
    return H


def motion_blur(image, parameters):
    """Generates a frequency-domain filter for motion blur.
    :param image: The original image (used to determine filter dimensions).
    :param parameters: A list containing [T, a, b], where T is the exposure time
                       and (a, b) are the motion components.
    :return: A complex 2D NumPy array representing the motion blur filter.
    """
    row, col = image.shape
    T, a, b = parameters
    H = np.zeros((row, col), dtype=complex)

    for u in range(row):
        for v in range(col):
            u_centered = u - row // 2
            v_centered = v - col // 2
            numerator = np.sin(np.pi * T * (u_centered * a + v_centered * b))
            denominator = np.pi * (u_centered * a + v_centered * b) + 1e-6
            H[u, v] = numerator / denominator * np.exp(-1j * np.pi * T * (u_centered * a + v_centered * b))
    return H


def wiener_filter(image, blured_core, enhance_factor=0.75):
    """Generates a Wiener filter for image restoration.
    :param image: The FFT of the degraded image (noisy and blurred).
    :param blured_core: The known motion blur filter (H) in the frequency domain.
    :param enhance_factor: A factor to adjust the filter's behavior.
    :return: A complex 2D NumPy array representing the Wiener filter.
    """
    H = blured_core
    H_magnitude_squared = np.abs(H) ** 2
    # The signal power spectrum is approximated by the magnitude of the noisy image's spectrum.
    signal_power = np.abs(image) ** 2

    # The noise power spectrum is assumed to be zero for simplicity in this case.
    # noise = np.random.normal(0, 10, image.shape)
    # noise = np.fft.fftshift(np.fft.fft2(noise))
    # noise_power = np.abs(noise) ** 2

    # In a real-world scenario, this would be estimated from the image or a known value.
    noise_power = np.zeros(image.shape)

    # The core Wiener filter formula.
    G = (np.conj(H) / (H_magnitude_squared + noise_power / (signal_power + 1e-6) + 1e-6))
    # An optional enhancement factor can be applied to improve results.
    G = G * (1 + enhance_factor * (1 - H_magnitude_squared))
    return G


def marr_hildreth_edge_detection(image, sigma=1.0, threshold=0.0):
    """Performs edge detection using the Marr-Hildreth (LoG) algorithm.
    :param image: Input grayscale image.
    :param sigma: The standard deviation of the Gaussian filter.
    :param threshold: A value to filter out weak zero-crossings.
    :return: The edge-detected image.
    """
    # 1. Smooth the image with a Gaussian filter.
    smoothed = cv.GaussianBlur(image, ksize=(3, 3), sigmaX=sigma)

    # 2. Apply the Laplacian operator to find zero-crossings.
    laplacian = cv.Laplacian(smoothed, ddepth=cv.CV_64F)

    # 3. Find the zero-crossings.
    zero_crossing = np.zeros_like(laplacian, dtype=np.uint8)
    rows, cols = laplacian.shape

    for i in range(1, rows - 1):
        for j in range(1, cols - 1):
            patch = laplacian[i - 1:i + 2, j - 1:j + 2]
            min_val = patch.min()
            max_val = patch.max()

            # A zero-crossing occurs if the min and max values have opposite signs.
            # A threshold is used to filter out noise-induced zero-crossings.
            if min_val < 0 and max_val > 0 and abs(max_val - min_val) > threshold:
                zero_crossing[i, j] = 255

    return zero_crossing


# --- Main Image Processing Pipeline ---

# Load the image and pad it to a power-of-2 size for efficient FFT.
image = cv.imread('../../images/DIP.bmp', cv.IMREAD_GRAYSCALE)
image = bilinear.bilinear_interpolation(image, 512, 512)
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

# Define parameters for the motion blur.
T = 1
a = 0.1
b = 0.1

# --- Step 1: Image Degradation ---
# Simulate motion blur and add Gaussian noise to the image.
motion_image, _ = fft2d.fft2d(copy.deepcopy(image), motion_blur, [T, a, b])
plt.axis('off')
plt.imshow(motion_image, cmap='gray')
plt.title('Motion Blured Image')
plt.show()

noisy_image = noise.gaussian(copy.deepcopy(motion_image), 0, 10)
noisy_image = np.float64(noisy_image)
plt.axis('off')
plt.imshow(noisy_image, cmap='gray')
plt.title('Noisy Image')
plt.show()

# --- Step 2: Image Restoration ---
# Apply a two-stage filtering process.
# First, apply a Gaussian low-pass filter to smooth out some of the high-frequency noise.
filtered, _ = fft2d.fft2d(copy.deepcopy(noisy_image), gaussian_lowpass, 20)
# Then, apply the Wiener filter to deblur the image.
filtered, _ = fft2d.fft2d(copy.deepcopy(filtered), wiener_filter, motion_blur(copy.deepcopy(image), [T, a, b]))
plt.axis('off')
plt.imshow(filtered, cmap='gray')
plt.title('Filtered Image')
plt.show()

# Evaluate the initial restoration by calculating the SNR.
SNR1 = SNR(image, filtered)
print(f'SNR (Only Wiener): {SNR1}')

# --- Step 3: Image Enhancement (Post-processing) ---
# Detect edges from the original image using the Marr-Hildreth algorithm.
edges = marr_hildreth_edge_detection(image, sigma=0.25, threshold=0.01)
plt.axis('off')
plt.imshow(edges, cmap='gray')
plt.title('Edges Image')
plt.show()

# Refine the filtered image with a 3x3 averaging filter for additional smoothing.
blured = filtering.filtering(filtered, [[1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9]])
blured = filtering.filtering(blured, [[1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9]])
# Combine the smoothed, restored image with the detected edges to re-introduce
# sharp details and improve visual quality.
blured = blured + 0.55 * edges
plt.axis('off')
plt.imshow(blured, cmap='gray')
plt.title('Final Filtered Image')
plt.show()

# Evaluate the final restored and enhanced image by calculating the SNR.
SNR2 = SNR(image, blured)
print(f'SNR (After Processing): {SNR2}')
