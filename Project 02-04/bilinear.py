"""
The function package from Project 02-04 Zooming and Shrinking Images by Bilinear Interpolation
"""

import numpy as np


def bilinear_interpolation(image, new_width, new_height):
    image = np.array(image, dtype=np.float64)
    old_height, old_width = image.shape

    new_image = np.zeros((new_height, new_width), dtype=np.float64)

    scale_x = old_width / new_width
    scale_y = old_height / new_height

    for y in range(new_height):
        for x in range(new_width):
            src_x = (x + 0.5) * scale_x - 0.5
            src_y = (y + 0.5) * scale_y - 0.5

            x1 = int(src_x)
            y1 = int(src_y)
            x2 = min(x1 + 1, old_width - 1)
            y2 = min(y1 + 1, old_height - 1)

            dx = src_x - x1
            dy = src_y - y1

            top_left = image[y1, x1] * (1 - dx) + image[y1, x2] * dx
            bottom_left = image[y2, x1] * (1 - dx) + image[y2, x2] * dx
            final_value = top_left * (1 - dy) + bottom_left * dy

            new_image[y, x] = np.clip(final_value, 0, 255)

    return new_image