"""
Project 02-01  Image Printing Program Based on Halftoning
Author: Billiefu
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# First, generate all halftone dot patterns
dot = np.zeros((3, 3, 10))
dot[:, :, 1] = [[0, 255, 0], [0, 0, 0], [0, 0, 0]]
dot[:, :, 2] = [[0, 255, 0], [0, 0, 0], [0, 0, 255]]
dot[:, :, 3] = [[255, 255, 0], [0, 0, 0], [0, 0, 255]]
dot[:, :, 4] = [[255, 255, 0], [0, 0, 0], [255, 0, 255]]
dot[:, :, 5] = [[255, 255, 255], [0, 0, 0], [255, 0, 255]]
dot[:, :, 6] = [[255, 255, 255], [0, 0, 255], [255, 0, 255]]
dot[:, :, 7] = [[255, 255, 255], [0, 0, 255], [255, 255, 255]]
dot[:, :, 8] = [[255, 255, 255], [255, 0, 255], [255, 255, 255]]
dot[:, :, 9] = [[255, 255, 255], [255, 255, 255], [255, 255, 255]]


def adaption(image):
    """
    Rescale the image that exceeds the standard dimensions back to the standard size.
    :param image: The image before rescaling
    :return: The image after rescaling
    """
    row, col = image.shape
    rscale = row / (816 / 3)
    cscale = col / (1056 / 3)
    scale = 1 / max(cscale, rscale)
    result = cv.resize(image, (0, 0), None, scale, scale)
    return result


def halftoning(image):
    """
    Convert the image into a halftone image.
    :param image: The image before conversion to halftone
    :return: The image after conversion to halftone
    """
    image = np.floor(np.double(image) / 25.6)
    row, col = image.shape
    result = np.zeros((row * 3, col * 3))
    for i in range(row):
        for j in range(col):
            result[i*3:i*3+3, j*3:j*3+3] = dot[:, :, int(image[i, j])]
    return result


# Experiment with Lenna
image = cv.imread('../data/Lenna_face.bmp', cv.IMREAD_GRAYSCALE)
row, col = image.shape
if (row > (816 / 3)) or (col > (1056 / 3)):
    image = adaption(image)
result = halftoning(image)

plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title("Original Image (Lenna)")
plt.show()

plt.axis('off')
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title("Halftoning Image (Lenna)")
plt.show()


# Experiment with Cameraman
image = cv.imread('../data/cameraman.bmp', cv.IMREAD_GRAYSCALE)
row, col = image.shape
if (row > (816 / 3)) or (col > (1056 / 3)):
    image = adaption(image)
result = halftoning(image)

plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title("Original Image (Cameraman)")
plt.show()

plt.axis('off')
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title("Halftoning Image (Cameraman)")
plt.show()


# Experiment with Crowd
image = cv.imread('../data/crowd.bmp', cv.IMREAD_GRAYSCALE)
row, col = image.shape
if (row > (816 / 3)) or (col > (1056 / 3)):
    image = adaption(image)
result = halftoning(image)

plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title("Original Image (Crowd)")
plt.show()

plt.axis('off')
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title("Halftoning Image (Crowd)")
plt.show()

# Experiment with continuous grayscale image
image = np.zeros((256, 256))
for i in range(256):
    image[:, i] = i
result = halftoning(image)

plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title("Original Image (Gray Scale Wedge)")
plt.show()

plt.axis('off')
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title("Halftoning Image (Gray Scale Wedge)")
plt.show()
