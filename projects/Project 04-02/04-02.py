"""
Copyright (C) 2025 Fu Tszkok

:module: Project 04-02
:function: Fourier Spectrum and Average Value
:author: Fu Tszkok
:date: 2025-02-01
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import fft2d
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


# Load the grayscale image and display the original.
image = cv.imread('../../images/ray_traced_bottle_original.bmp', cv.IMREAD_GRAYSCALE)
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

# Convert the image to float64 for numerical operations.
image = np.array(image, dtype=np.float64)

# Perform the 2D FFT using the custom `fft2d` function.
# The function returns the processed image and the frequency spectrum.
result, spectrum = fft2d.fft2d(image)

# Display the frequency spectrum. A log transformation is applied to
# enhance the visibility of lower-magnitude frequency components.
plt.axis('off')
plt.imshow(2 * np.log(np.abs(spectrum)), cmap='gray')
plt.title('Frequency Spectrum')
plt.show()

# Calculate the mean pixel value of the image.
# The DC component (zero-frequency term) of the FFT is located at the center
# of the shifted spectrum. Its value is proportional to the sum of all pixels.
# The mean is therefore the DC component's magnitude divided by the total number of pixels.
mean_value = np.abs(spectrum[spectrum.shape[0]//2, spectrum.shape[1]//2]) / (spectrum.shape[0] * spectrum.shape[1])
print(f"Image Mean Value from FFT: {mean_value}")
