"""
Copyright (C) 2025 Fu Tszkok

:module: Project 03-06
:function: Unsharp Masking
:author: Fu Tszkok
:date: 2025-02-01
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import filtering
import operations

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt


# Load the input grayscale image.
image = cv.imread("../../images/new-art.bmp", cv.IMREAD_GRAYSCALE)

# Display the original image for reference.
plt.axis('off')
plt.imshow(image, cmap='gray')
plt.title('Original Image')
plt.show()

# Define the high-boost filtering constant `a`.
# When a > 1, it's high-boost filtering; when a = 1, it's unsharp masking.
a = 2
[row, col] = image.shape

# Apply a 3x3 averaging filter (from a textbook, e.g., Fig 3.34(a)) using the custom function.
blur = filtering.filtering(image, [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]])
# Display the blurred image.
plt.axis('off')
plt.imshow(blur, cmap='gray')
plt.title('Blurred Image Using Core At Fig 3.34(a)')
plt.show()

# Create the unsharp mask by subtracting the blurred image from the original.
# This mask contains the high-frequency components (edges and details).
mask = operations.subtraction(image, blur)
# Display the mask image.
plt.axis('off')
plt.imshow(mask, cmap='gray')
plt.title('Mask Image Using Core At Fig 3.34(a)')
plt.show()

# Perform high-boost filtering using the formula: Result = A * Original - Blurred + Mask
# This is equivalent to: Result = Original + (A-1) * Original + Mask.
# Here, we use the equivalent formula: Result = (A-1) * Original + Mask.
# This operation enhances the edges while preserving the original image's brightness.
result = operations.addition(operations.multiplication(image, a - 1), mask)
# Display the final sharpened result from the custom implementation.
plt.axis('off')
plt.imshow(result, cmap='gray')
plt.title('Result Image Using Core At Fig 3.34(a)')
plt.show()

# For comparison, apply OpenCV's built-in filter2D function with the same kernel.
tblur = cv.filter2D(image, -1, np.array([[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]]),
                    borderType=cv.BORDER_CONSTANT)
# Display the blurred image from OpenCV.
plt.axis('off')
plt.imshow(tblur, cmap='gray')
plt.title('True Blurred Image Using Core At Fig 3.34(a)')
plt.show()

# Create the unsharp mask using OpenCV's subtract function.
tmask = cv.subtract(image, tblur)
# Display the mask image from OpenCV.
plt.axis('off')
plt.imshow(tmask, cmap='gray')
plt.title('True Mask Image Using Core At Fig 3.34(a)')
plt.show()

# Perform high-boost filtering using OpenCV's functions for verification.
tresult = cv.add(cv.multiply(image, np.uint8(np.ones((row, col)) * (a-1))), tmask)
# Display the final sharpened image from OpenCV.
plt.axis('off')
plt.imshow(tresult, cmap='gray')
plt.title('True Result Image Using Core At Fig 3.34(a)')
plt.show()

# Calculate and display the pixel-wise absolute difference (loss) between custom and OpenCV results.
loss = np.abs(np.float64(tresult) - np.float64(result))
plt.axis('off')
plt.imshow(loss, cmap='gray')
plt.title('Loss Image Using Core At Fig 3.34(a)')
# Print the average loss to quantify the accuracy of the custom implementation.
print(f'Average Loss For Core Fig 3.34(a): {np.mean(loss):.4f}')
plt.show()


# --- Unsharp Masking / High-Boost Filtering with Gaussian-like Kernel ---

# Apply a Gaussian-like filter (from a textbook, e.g., Fig 3.34(b)) using the custom function.
blur = filtering.filtering(image, [[1/16, 2/16, 1/16], [2/16, 4/16, 2/16], [1/16, 2/16, 1/16]])
# Display the blurred image.
plt.axis('off')
plt.imshow(blur, cmap='gray')
plt.title('Blurred Image Using Core At Fig 3.34(b)')
plt.show()

# Create the unsharp mask by subtracting the blurred image from the original.
mask = operations.subtraction(image, blur)
# Display the mask image.
plt.axis('off')
plt.imshow(mask, cmap='gray')
plt.title('Mask Image Using Core At Fig 3.34(b)')
plt.show()

# Perform high-boost filtering.
result = operations.addition(operations.multiplication(image, a - 1), mask)
# Display the final sharpened result from the custom implementation.
plt.axis('off')
plt.imshow(result, cmap='gray')
plt.title('Result Image Using Core At Fig 3.34(b)')
plt.show()

# For comparison, apply OpenCV's built-in filter2D function.
tblur = cv.filter2D(image, -1, np.array([[1/16, 2/16, 1/16], [2/16, 4/16, 2/16], [1/16, 2/16, 1/16]]),
                    borderType=cv.BORDER_CONSTANT)
# Display the blurred image from OpenCV.
plt.axis('off')
plt.imshow(tblur, cmap='gray')
plt.title('True Blurred Image Using Core At Fig 3.34(b)')
plt.show()

# Create the unsharp mask using OpenCV.
tmask = cv.subtract(image, tblur)
# Display the mask image from OpenCV.
plt.axis('off')
plt.imshow(tmask, cmap='gray')
plt.title('True Mask Image Using Core At Fig 3.34(b)')
plt.show()

# Perform high-boost filtering using OpenCV.
tresult = cv.add(cv.multiply(image, np.uint8(np.ones((row, col)) * (a-1))), tmask)
# Display the final sharpened image from OpenCV.
plt.axis('off')
plt.imshow(tresult, cmap='gray')
plt.title('True Result Image Using Core At Fig 3.34(b)')
plt.show()

# Calculate and display the pixel-wise absolute difference (loss) between custom and OpenCV results.
loss = np.abs(np.float64(tresult) - np.float64(result))
plt.axis('off')
plt.imshow(loss, cmap='gray')
plt.title('Loss Image Using Core At Fig 3.34(b)')
# Print the average loss to quantify the accuracy.
print(f'Average Loss For Core Fig 3.34(b): {np.mean(loss):.4f}')
plt.show()
