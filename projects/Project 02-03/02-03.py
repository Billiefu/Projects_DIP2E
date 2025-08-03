"""
Copyright (C) 2025 Fu Tszkok

:module: Project 02-03
:function: Zooming and Shrinking Images by Pixel Replication
:author: Fu Tszkok
:date: 2025-01-28
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def nearest_neighbor_interpolation(image, new_width, new_height):
    """Performs image scaling using nearest neighbor interpolation.
    :param image: The input image before scaling.
    :param new_width: The width of the scaled output image.
    :param new_height: The height of the scaled output image.
    :return: The scaled image (NumPy array).
    """
    # Convert the input image to a floating-point array for interpolation calculations.
    image = np.array(image, dtype=np.float64)
    old_height, old_width = image.shape  # Get the dimensions of the original image.

    # Create a new blank image with the desired size, initialized with zeros.
    new_image = np.zeros((new_height, new_width), dtype=np.float64)

    # Calculate the scaling factors for the x and y axes.
    scale_x = old_width / new_width
    scale_y = old_height / new_height

    # Iterate through each pixel of the new (output) image.
    for y in range(new_height):
        for x in range(new_width):
            # Calculate the corresponding coordinates in the original image (inverse mapping).
            src_x = int((x + 0.5) * scale_x - 0.5)
            src_y = int((y + 0.5) * scale_y - 0.5)

            # Ensure the calculated coordinates are within the valid range of the original image.
            # This implementation incorrectly averages four pixels instead of picking the nearest one.
            x1 = max(min(src_x, old_width - 1), 0)
            y1 = max(min(src_y, old_height - 1), 0)
            x2 = max(min(x1 + 1, old_width - 1), 0)
            y2 = max(min(y1 + 1, old_height - 1), 0)

            # Calculate the average value of the four neighboring pixels as the new pixel value.
            # This is not a true nearest neighbor interpolation but a simple averaging method.
            ave_value = np.uint8((image[y1, x1] + image[y1, x2] + image[y2, x1] + image[y2, x2]) / 4)

            # Assign the calculated value to the new image's pixel and clip it to the 0-255 range.
            new_image[y, x] = np.clip(ave_value, 0, 255)

    return new_image


# Load and display the original image.
image = cv.imread('../../images/rose1024.bmp', cv.IMREAD_GRAYSCALE)
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

# Scale the image down to 256x256 using the custom interpolation function.
image_resized_down = nearest_neighbor_interpolation(image, 256, 256)
image_resized_down = np.uint8(image_resized_down)  # Convert to 8-bit unsigned integer type.
plt.axis('off')
plt.imshow(image_resized_down, cmap='gray')
plt.title('Scaled Down Image')
plt.show()

# Scale the downsized image back up to 1024x1024.
image_resized_up = nearest_neighbor_interpolation(image_resized_down, 1024, 1024)
image_resized_up = np.uint8(image_resized_up)  # Convert to 8-bit unsigned integer type.
plt.axis('off')
plt.imshow(image_resized_up, cmap='gray')
plt.title('Scaled Up Image')
plt.show()

# Calculate and display the loss image (difference between original and up-scaled).
loss = np.float64(image_resized_up) - np.float64(image)
loss = np.uint8(np.abs(loss))  # Take the absolute difference and convert to 8-bit.
print(f'Average Loss: {sum(sum(abs(np.float64(loss)))) / (loss.shape[0] * loss.shape[1])}')
plt.axis('off')
plt.imshow(loss, cmap='gray')
plt.title('Loss Image')
plt.show()
