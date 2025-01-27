"""
Project 02-02  Reducing the Number of Gray Levels in an Image
Author: Billiefu
"""

import cv2 as cv
import matplotlib.pyplot as plt

image = cv.imread('../data/ctskull-256.bmp', cv.IMREAD_GRAYSCALE)
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title("Original Image")
plt.show()

grayscale = 256
for k in range(7):
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            image[i, j] /= 2

    grayscale /= 2
    plt.axis('off')
    plt.imshow(image, cmap='gray')
    plt.title(f"Grayscale {grayscale} Image")
    plt.show()
