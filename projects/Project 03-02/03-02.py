"""
Copyright (C) 2025 Fu Tszkok

:module: Project 03-02
:function: Histogram Equalization [Multiple Uses]
:author: Fu Tszkok
:date: 2025-02-01
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import copy
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def histogram(image):
    """Calculates the histogram of a grayscale image.
    :param image: Input grayscale image (NumPy array).
    :return: A tuple containing the counts of each grayscale level and the levels themselves.
    """
    x = [i for i in range(256)]  # Create a list of grayscale levels from 0 to 255.
    count = np.zeros(256)  # Initialize an array to store the counts of each level.
    for i in range(256):
        count[i] = np.sum(image == i)  # Count the number of pixels with value 'i'.
    return count, x


def equalization(image):
    """Performs histogram equalization on a grayscale image.
    :param image: Input grayscale image (NumPy array).
    :return: The equalized image (NumPy array).
    """
    row, col = image.shape
    count, x = histogram(image)  # Get the histogram of the original image.
    count = np.double(count) / (row * col)  # Normalize the histogram to get the probability of each level.

    # Calculate the cumulative distribution function (CDF) which serves as the transformation function.
    trans = np.zeros(256)
    for i in range(256):
        for j in range(i + 1):
            trans[i] = trans[i] + count[j]

    trans = np.round(trans * 255)  # Scale the CDF to the range [0, 255] and round to the nearest integer.

    # Plot the histogram equalization transformation function.
    plt.plot(x, trans, '-', color='blue')
    plt.xlim([0, 255])
    plt.ylim([0, 255])
    plt.title('Histogram Equalization Transformation Function')
    plt.show()

    # Apply the transformation function to the image.
    result = copy.deepcopy(image)
    for i in range(256):
        result[image == i] = trans[i]
    return result


# Load image and compute its histogram.
image = cv.imread('../../images/spine.bmp', cv.IMREAD_GRAYSCALE)
count, x = histogram(image)

# Display the original image and its histogram (custom implementation).
plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title('Original Image')
plt.show()

plt.bar(x, count)
plt.title('Histogram (self)')
plt.show()

# Display the histogram using matplotlib's built-in function for comparison.
plt.hist(image.ravel(), 256, [0, 256])
plt.title('Histogram (ravel)')
plt.show()

# Perform histogram equalization using the custom function and OpenCV's built-in function.
result = equalization(image)
[eq_count, eq_x] = histogram(result)
real = cv.equalizeHist(image)
[rcount, rx] = histogram(real)

# Display the custom equalized image and its histogram.
plt.axis('off')
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title('Equalized Image (self)')
plt.show()

plt.bar(eq_x, eq_count)
plt.title('Equalized Histogram (self)')
plt.show()

# Display the OpenCV equalized image and its histogram.
plt.axis('off')
plt.imshow(real, cmap='gray', vmin=0, vmax=255)
plt.title('Equalized Image (opencv)')
plt.show()

plt.bar(rx, rcount)
plt.title('Equalized Histogram (opencv)')
plt.show()

# Calculate the pixel-wise difference (loss) between the two equalized images.
loss = np.zeros((image.shape[0], image.shape[1]), dtype=int)
for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        loss[i, j] = np.abs(int(real[i, j]) - int(result[i, j]))

# Display the loss image and print the average loss.
plt.axis('off')
plt.imshow(loss, cmap='gray')
plt.title('Loss Image')
plt.show()
print(f"Average Loss: {sum(sum(loss)) / (loss.shape[0] * loss.shape[1]):.{4}}")
