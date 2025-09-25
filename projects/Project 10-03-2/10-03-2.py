"""
Copyright (C) 2025 Fu Tszkok

:module: Project 10-03-2
:function: Optimum Thresholding Based on Otsu
:author: Fu Tszkok
:date: 2025-09-24
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import cv2 as cv

from histogram import *


def otsu_thresholding(image):
    """Applies Otsu's method to find the optimal threshold for a grayscale image.
    :param image: Input grayscale image (NumPy array).
    :return: A tuple containing the thresholded binary image and the optimal threshold value.
    """
    # Calculate the histogram of the input image.
    hist, _ = histogram(image)
    total_pixels = image.size
    # Normalize the histogram to represent probability distribution.
    normalized_hist = hist / total_pixels

    best_threshold = -1
    max_variance = 0

    # Iterate through all possible threshold values (k) from 0 to 255.
    for k in range(256):
        # Calculate P1(k): the probability of the first class (foreground), from 0 to k.
        p1 = np.sum(normalized_hist[:k+1])
        # Calculate m(k): the mean of the first class.
        m_k = np.sum(np.arange(k+1) * normalized_hist[:k+1])

        # Skip if either class probability is zero to avoid division by zero.
        if p1 == 0 or p1 == 1:
            continue

        # Calculate m_g: the global mean of the entire image.
        m_g = np.sum(np.arange(256) * normalized_hist)

        # Calculate the inter-class variance using the core Otsu formula.
        sigma_b_squared = ((m_g * p1 - m_k)**2) / (p1 * (1 - p1))
        print(f'The inter-class variance of {k} is: {np.sqrt(sigma_b_squared if sigma_b_squared > 0 else 0)}')

        # Update the best threshold if the current variance is the maximum found so far.
        if sigma_b_squared > max_variance:
            max_variance = sigma_b_squared
            best_threshold = k

    # Apply the optimal threshold to the original image to get the binary segmented image.
    _, thresholded_image = cv.threshold(image, best_threshold, 255, cv.THRESH_BINARY)

    return thresholded_image, best_threshold


# Load the grayscale image.
image = cv.imread('../../images/polymersomes.bmp', cv.IMREAD_GRAYSCALE)
# Calculate and display the histogram of the original image.
count, x = histogram(image)

plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title('Original Image')
plt.show()

plt.bar(x, count)
plt.title('Histogram (self)')
plt.show()

# Apply Otsu's method to automatically segment the image.
segmented_image, threshold = otsu_thresholding(image)
print(f"The optimal threshold (k*) calculated by Otsu is: {threshold}")

# Display the segmented image with the optimal threshold value in the title.
plt.axis('off')
plt.imshow(segmented_image, cmap='gray')
plt.title(f'Segmented Image (Threshold = {threshold})')
plt.show()
