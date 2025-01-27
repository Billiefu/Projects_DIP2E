"""
Project 02-04  Zooming and Shrinking Images by Bilinear Interpolation [Multiple Uses]
Author: Billiefu
The functions of this program will be packaged as 'bilinear' for multiple uses.
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def bilinear_interpolation(image, new_width, new_height):
    """
    Use the bilinear interpolation algorithm for interpolation to perform image scaling
    :param image: The image before scaling
    :param new_width: The width of the scaled image
    :param new_height: The height of the scaled image
    :return: The scaled image
    """
    # Convert the input image to a floating-point array for interpolation calculations
    image = np.array(image, dtype=np.float64)
    old_height, old_width = image.shape  # Get the height and width of the original image

    # Create a new blank image with size new_height x new_width
    new_image = np.zeros((new_height, new_width), dtype=np.float64)

    scale_x = old_width / new_width  # Calculate the horizontal scaling factor
    scale_y = old_height / new_height  # Calculate the vertical scaling factor

    for y in range(new_height):
        for x in range(new_width):
            # Calculate the floating-point coordinates in the original image (inverse mapping)
            src_x = (x + 0.5) * scale_x - 0.5
            src_y = (y + 0.5) * scale_y - 0.5

            # Get the integer coordinates of the four adjacent pixels
            x1 = int(src_x)
            y1 = int(src_y)
            x2 = min(x1 + 1, old_width - 1)  # Ensure it doesn't go out of bounds
            y2 = min(y1 + 1, old_height - 1)  # Ensure it doesn't go out of bounds

            dx = src_x - x1  # Calculate the difference in the x-direction
            dy = src_y - y1  # Calculate the difference in the y-direction

            # Compute the interpolation result
            # Final interpolation result = top interpolation result + bottom interpolation result
            top_left = image[y1, x1] * (1 - dx) + image[y1, x2] * dx
            bottom_left = image[y2, x1] * (1 - dx) + image[y2, x2] * dx
            final_value = top_left * (1 - dy) + bottom_left * dy

            # Assign the computed value to the pixel in the new image, ensuring it stays between 0 and 255
            new_image[y, x] = np.clip(final_value, 0, 255)

    return new_image


image = cv.imread('../data/rose1024.bmp', cv.IMREAD_GRAYSCALE)
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

image_resized_down = bilinear_interpolation(image, 256, 256)
image_resized_down = np.uint8(image_resized_down)
plt.axis('off')
plt.imshow(image_resized_down, cmap='gray')
plt.title('Scaled Down Image')
plt.show()

image_resized_up = bilinear_interpolation(image_resized_down, 1024, 1024)
image_resized_up = np.uint8(image_resized_up)
plt.axis('off')
plt.imshow(image_resized_up, cmap='gray')
plt.title('Scaled Up Image')
plt.show()

loss = np.float64(image_resized_up) - np.float64(image)
loss = np.uint8(np.abs(loss))
print(f'Average Loss: {sum(sum(abs(np.float64(loss)))) / (loss.shape[0] * loss.shape[1])}')
plt.axis('off')
plt.imshow(loss, cmap='gray')
plt.title('Loss Image')
plt.show()
