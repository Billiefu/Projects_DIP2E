"""
Copyright (C) 2025 Fu Tszkok

:module: Project 10-03
:function: Optimum Thresholding
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


def calculate_patch_stats(image_patch):
    """Calculates the mean and standard deviation of a given image patch.
    :param image_patch: A small NumPy array representing a region of the image.
    :return: A tuple containing the mean and variance of the patch.
    """
    mean = np.mean(image_patch)
    var = np.var(image_patch)
    return mean, var


def optimum_thresholding(image, mu1, mu2, sigma_sq, p1, p2):
    """Applies Bayesian optimal thresholding to segment an image.
    :param image: Input grayscale image (NumPy array).
    :param mu1: Mean of the first class (e.g., object).
    :param mu2: Mean of the second class (e.g., background).
    :param sigma_sq: Common variance of the two classes.
    :param p1: Prior probability of the first class.
    :param p2: Prior probability of the second class.
    :return: A tuple containing the thresholded binary image and the optimal threshold value.
    """
    if mu1 == mu2:
        # Special case: If means are equal, the threshold is simply their average.
        threshold = (mu1 + mu2) / 2
    else:
        log_ratio = np.log(p2 / p1)
        # Calculate the optimal threshold using the Bayesian formula.
        threshold = (mu1 + mu2) / 2 + (sigma_sq / (mu1 - mu2)) * log_ratio

    # Apply the calculated threshold to the image.
    _, segmented_image = cv.threshold(image, threshold, 255, cv.THRESH_BINARY)

    return segmented_image, threshold


# Load the grayscale image and display its histogram and image.
image = cv.imread('../../images/original_septagon.bmp', cv.IMREAD_GRAYSCALE)
count, x = histogram(image)

plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title('Original Image')
plt.show()

plt.bar(x, count)
plt.title('Histogram (self)')
plt.show()

# Manually select small patches to represent the object and background classes.
obj_patch = image[100:120, 100:120]  # Example patch from the object region.
bg_patch = image[10:30, 10:30]      # Example patch from the background region.

# Compute the mean and variance for each patch to estimate the class parameters.
mu1_est, var1_est = calculate_patch_stats(obj_patch)
mu2_est, var2_est = calculate_patch_stats(bg_patch)

# Assume a common variance for the two classes by averaging the estimated variances.
sigma_sq_est = (var1_est + var2_est) / 2

# Manually estimate the prior probabilities based on visual inspection of the image.
# For example, if the object occupies approximately 20% of the image area.
p1_est = 0.2
p2_est = 0.8

# Print the estimated parameters for clarity.
print(f"Estimated Object Mean (mu1): {mu1_est:.2f}")
print(f"Estimated Background Mean (mu2): {mu2_est:.2f}")
print(f"Estimated Common Variance (sigma^2): {sigma_sq_est:.2f}")
print(f"Estimated Object Probability (P1): {p1_est:.2f}")
print(f"Estimated Background Probability (P2): {p2_est:.2f}")

# Call the optimal thresholding function with the estimated parameters.
segmented_image, threshold = optimum_thresholding(image, mu1_est, mu2_est, sigma_sq_est, p1_est, p2_est)
print(f"The optimal threshold is: {threshold}")

# Display the segmented image with the final threshold value in the title.
plt.axis('off')
plt.imshow(segmented_image, cmap='gray')
plt.title(f'Segmented Image (Threshold = {threshold})')
plt.show()
