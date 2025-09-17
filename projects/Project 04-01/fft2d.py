"""
Copyright (C) 2025 Fu Tszkok

:module: fft2d
:function: The function package from Project 04-01 Two-Dimensional Fast Fourier Transform
:author: Fu Tszkok
:date: 2025-02-01
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import bilinear
import numpy as np


def fft2d(image, filter_func=None, parameters=None):
    """Performs a 2D Fast Fourier Transform on an image.
    :param image: Input grayscale image (NumPy array).
    :param filter_func: An optional function to apply a filter in the frequency domain.
    :param parameters: Optional parameters for the filter function.
    :return: A tuple containing the processed image and the frequency spectrum.
    """
    row, col = image.shape

    # Check if image dimensions are a power of 2 for efficient FFT computation.
    # If not, pad the image to the next largest power of 2 using bilinear interpolation.
    if (row & (row - 1)) != 0 or (col & (col - 1)) != 0:
        row = 2 ** np.ceil(np.log2(row)).astype(int)
        col = 2 ** np.ceil(np.log2(col)).astype(int)
        image = bilinear.bilinear_interpolation(image, row, col)

    # Shift the zero-frequency component to the center of the spectrum by
    # multiplying the image by (-1)^(x+y).
    for i in range(row):
        for j in range(col):
            image[i, j] = image[i, j] * ((-1) ** (i + j))

    # Perform the 2D Fast Fourier Transform.
    f_transform = np.fft.fft2(image)

    # Apply the optional filter in the frequency domain.
    if filter_func is not None:
        filter = filter_func(f_transform, parameters)  # Get the filter mask from the function.
        # Element-wise multiplication of the transform with the filter.
        for i in range(row):
            for j in range(col):
                f_transform[i, j] = filter[i, j] * f_transform[i, j]

    # Perform the inverse 2D Fast Fourier Transform.
    f_inv_transform = np.fft.ifft2(f_transform)

    # Reconstruct the image by shifting the zero-frequency component back
    # and taking the real part of the complex result.
    result = np.zeros((row, col))
    for i in range(row):
        for j in range(col):
            result[i, j] = np.real(f_inv_transform[i, j]) * ((-1) ** (i + j))
    result = np.float64(result)

    # The frequency spectrum is the magnitude of the FFT result.
    spectrum = f_transform

    return result, spectrum
