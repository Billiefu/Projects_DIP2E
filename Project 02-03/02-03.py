"""
Project 02-03  Zooming and Shrinking Images by Pixel Replication
Author: Billiefu
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def nearest_neighbor_interpolation(image, new_width, new_height):
    """
    Use the nearest neighbor algorithm for interpolation to perform image scaling
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

    # Calculate the scaling factors for the x and y axes
    scale_x = old_width / new_width
    scale_y = old_height / new_height

    # Iterate through each pixel of the new image
    for y in range(new_height):
        for x in range(new_width):
            # Calculate the corresponding coordinates in the original image (inverse mapping)
            src_x = int((x + 0.5) * scale_x - 0.5)
            src_y = int((y + 0.5) * scale_y - 0.5)

            # Ensure the coordinates are within the valid range of the original image
            x1 = max(min(src_x, old_width - 1), 0)
            y1 = max(min(src_y, old_height - 1), 0)
            x2 = max(min(x1 + 1, old_width - 1), 0)
            y2 = max(min(y1 + 1, old_height - 1), 0)

            # Calculate the average value of the four neighboring pixels as the new pixel value
            # (simple nearest-neighbor interpolation)
            ave_value = np.uint8((image[y1, x1] + image[y1, x2] + image[y2, x1] + image[y2, x2]) / 4)

            # Assign the calculated value to the new image's pixel and ensure it is in the range of 0 to 255
            new_image[y, x] = np.clip(ave_value, 0, 255)

    return new_image


image = cv.imread('../data/rose1024.bmp', cv.IMREAD_GRAYSCALE)
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

image_resized_down = nearest_neighbor_interpolation(image, 256, 256)
image_resized_down = np.uint8(image_resized_down)
plt.axis('off')
plt.imshow(image_resized_down, cmap='gray')
plt.title('Scaled Down Image')
plt.show()

image_resized_up = nearest_neighbor_interpolation(image_resized_down, 1024, 1024)
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
