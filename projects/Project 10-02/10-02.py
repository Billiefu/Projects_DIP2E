"""
Copyright (C) 2025 Fu Tszkok

:module: Project 10-02 [Multiple Uses]
:function: Global Thresholding
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


def global_thresholding(image, delta_T=1e-2):
    """Finds an optimal global threshold using an iterative approach.
    :param image: Input grayscale image (NumPy array).
    :param delta_T: The tolerance for the change in threshold, which serves as the stopping criterion for the iteration.
    :return: A tuple containing the thresholded binary image and the final threshold value.
    """
    # Step 1: Initialize the threshold with the mean intensity of the entire image.
    threshold = np.mean(image)

    # Step 2: Begin the iterative loop.
    while True:
        # Partition the image into two groups (G1 and G2) based on the current threshold.
        G1 = image[image > threshold]  # Pixels with intensity > threshold (e.g., foreground)
        G2 = image[image <= threshold] # Pixels with intensity <= threshold (e.g., background)

        # Check for empty groups. If one group is empty, the algorithm cannot proceed
        # as it would lead to a division by zero.
        if G1.size == 0 or G2.size == 0:
            print("Warning: One of the pixel groups is empty. The algorithm might not converge properly.")
            break

        # Calculate the mean intensity for each group.
        m1 = np.mean(G1)
        m2 = np.mean(G2)

        # Calculate the new threshold as the average of the two means.
        threshold_new = 0.5 * (m1 + m2)

        # Check for convergence. If the change in threshold is less than delta_T, stop the iteration.
        if abs(threshold_new - threshold) < delta_T:
            threshold = threshold_new
            print(f"Threshold converged at T = {threshold:.2f}")
            break

        # Update the threshold for the next iteration.
        threshold = threshold_new
        print(f"Current threshold: {threshold:.2f}")

    # Apply the final converged threshold to the image to create the binary output.
    _, thresholded_image = cv.threshold(image, threshold, 255, cv.THRESH_BINARY)

    return thresholded_image, threshold


# Load the grayscale image.
image = cv.imread('../../images/original_septagon.bmp', cv.IMREAD_GRAYSCALE)
# Calculate and display the histogram of the original image.
count, x = histogram(image)

plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title('Original Image')
plt.show()

plt.bar(x, count)
plt.title('Histogram (self)')
plt.show()

# Apply the iterative global thresholding algorithm to segment the image.
segmented_image, threshold = global_thresholding(image)
print(f"The global threshold is: {threshold}")

# Display the segmented image with the final threshold value in the title.
plt.axis('off')
plt.imshow(segmented_image, cmap='gray')
plt.title(f'Segmented Image (Threshold = {threshold})')
plt.show()
