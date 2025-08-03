"""
Copyright (C) 2025 Fu Tszkok

:module: Project 02-04
:function: Zooming and Shrinking Images by Bilinear Interpolation [Multiple Uses]
:author: Fu Tszkok
:date: 2025-01-28
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

The functions of this program will be packaged as 'bilinear' for multiple uses.

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


def bilinear_interpolation(image, new_width, new_height):
    """Performs image scaling using bilinear interpolation.
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

    scale_x = old_width / new_width  # Calculate the horizontal scaling factor.
    scale_y = old_height / new_height  # Calculate the vertical scaling factor.

    for y in range(new_height):
        for x in range(new_width):
            # Calculate the floating-point coordinates in the original image (inverse mapping).
            src_x = (x + 0.5) * scale_x - 0.5
            src_y = (y + 0.5) * scale_y - 0.5

            # Get the integer coordinates of the four adjacent pixels.
            x1 = int(src_x)
            y1 = int(src_y)
            x2 = min(x1 + 1, old_width - 1)  # Ensure it doesn't go out of bounds.
            y2 = min(y1 + 1, old_height - 1)  # Ensure it doesn't go out of bounds.

            dx = src_x - x1  # Calculate the difference in the x-direction.
            dy = src_y - y1  # Calculate the difference in the y-direction.

            # Compute the interpolation result.
            # Perform linear interpolation in the x-direction for the top and bottom rows.
            top_left = image[y1, x1] * (1 - dx) + image[y1, x2] * dx
            bottom_left = image[y2, x1] * (1 - dx) + image[y2, x2] * dx
            # Perform linear interpolation in the y-direction on the interpolated values.
            final_value = top_left * (1 - dy) + bottom_left * dy

            # Assign the computed value to the pixel in the new image, and clip it to the 0-255 range.
            new_image[y, x] = np.clip(final_value, 0, 255)

    return new_image


# Load and display the original image.
image = cv.imread('../../images/rose1024.bmp', cv.IMREAD_GRAYSCALE)
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

# Scale the image down to 256x256 using the custom bilinear interpolation function.
image_resized_down = bilinear_interpolation(image, 256, 256)
image_resized_down = np.uint8(image_resized_down)  # Convert to 8-bit unsigned integer type.
plt.axis('off')
plt.imshow(image_resized_down, cmap='gray')
plt.title('Scaled Down Image')
plt.show()

# Scale the downsized image back up to 1024x1024.
image_resized_up = bilinear_interpolation(image_resized_down, 1024, 1024)
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
