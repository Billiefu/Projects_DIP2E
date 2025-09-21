"""
Copyright (C) 2025 Fu Tszkok

:module: Project 06-03
:function: Color Image Enhancement by Histogram Processing
:author: Fu Tszkok
:date: 2025-02-06
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import histogram
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# Load the color image and convert its color space from BGR to RGB for correct display.
image = cv.imread('../../images/bottom_left_stream.bmp')
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
plt.axis('off')
plt.imshow(image)
plt.title('Original Image')
plt.show()

# Split the image into its individual R, G, and B color channels.
R, G, B = image[:, :, 0], image[:, :, 1], image[:, :, 2]
# Calculate and display the histograms for each original color channel.
red_hist, r_x = histogram.histogram(R)
green_hist, g_x = histogram.histogram(G)
blue_hist, b_x = histogram.histogram(B)

plt.figure(figsize=(15, 9))
plt.subplot(1, 3, 1)
plt.bar(r_x, red_hist)
plt.title('Histogram of Red Component')
plt.subplot(1, 3, 2)
plt.bar(g_x, green_hist)
plt.title('Histogram of Green Component')
plt.subplot(1, 3, 3)
plt.bar(b_x, blue_hist)
plt.title('Histogram of Blue Component')
plt.show()

# Display the grayscale images of each color channel.
plt.figure(figsize=(10, 4))
plt.subplot(1, 3, 1)
plt.axis('off')
plt.imshow(R, cmap='gray')
plt.title('Image of Red Component')
plt.subplot(1, 3, 2)
plt.axis('off')
plt.imshow(G, cmap='gray')
plt.title('Image of Green Component')
plt.subplot(1, 3, 3)
plt.axis('off')
plt.imshow(B, cmap='gray')
plt.title('Image of Blue Component')
plt.show()


# --- Method 1: Independent Histogram Equalization of each channel ---
# Apply histogram equalization to each RGB channel separately.
R_eq = histogram.equalization(R)
G_eq = histogram.equalization(G)
B_eq = histogram.equalization(B)
# Calculate and display the histograms of the equalized components.
red_eq_hist, r_x = histogram.histogram(R_eq)
green_eq_hist, g_x = histogram.histogram(G_eq)
blue_eq_hist, b_x = histogram.histogram(B_eq)

plt.figure(figsize=(15, 9))
plt.subplot(1, 3, 1)
plt.bar(r_x, red_eq_hist)
plt.title('Histogram of Equalized Red Component')
plt.subplot(1, 3, 2)
plt.bar(g_x, green_eq_hist)
plt.title('Histogram of Equalized Green Component')
plt.subplot(1, 3, 3)
plt.bar(b_x, blue_eq_hist)
plt.title('Histogram of Equalized Blue Component')
plt.show()

# Merge the equalized channels back to form a color image.
image_eq = cv.merge([R_eq, G_eq, B_eq])
plt.axis('off')
plt.imshow(image_eq)
plt.title('Equalized Image Through Different Components')
plt.show()


# --- Method 2: Histogram Normalization (Matching) to an Average Histogram ---
# Create an average histogram from the three equalized histograms. This will be the target histogram.
ave_hist = np.zeros(256)
for i in range(256):
    ave_hist[i] = np.floor((red_eq_hist[i] + green_eq_hist[i] + blue_eq_hist[i]) / 3)
# Display the average histogram.
plt.bar(r_x, ave_hist)
plt.title('Average Histogram')
plt.show()

# Apply histogram normalization to each original color channel, using the average histogram as the target.
R_nor = histogram.normalization(R, ave_hist)
G_nor = histogram.normalization(G, ave_hist)
B_nor = histogram.normalization(B, ave_hist)
# Calculate and display the histograms of the normalized components.
red_nor_hist, r_x = histogram.histogram(R_nor)
green_nor_hist, g_x = histogram.histogram(G_nor)
blue_nor_hist, b_x = histogram.histogram(B_nor)

plt.figure(figsize=(15, 9))
plt.subplot(1, 3, 1)
plt.bar(r_x, red_nor_hist)
plt.title('Histogram of Normalized Red Component')
plt.subplot(1, 3, 2)
plt.bar(g_x, green_nor_hist)
plt.title('Histogram of Normalized Green Component')
plt.subplot(1, 3, 3)
plt.bar(b_x, blue_nor_hist)
plt.title('Histogram of Normalized Blue Component')
plt.show()

# Merge the normalized channels to form the final enhanced color image.
image_nor = cv.merge([R_nor, G_nor, B_nor])
plt.axis('off')
plt.imshow(image_nor)
plt.title('Normalized Image Through Average Histogram')
plt.show()


# --- Comparison and Loss Analysis ---
# Calculate the pixel-wise absolute difference (loss) between the two enhanced images.
loss = np.abs(np.float64(image_nor) - np.float64(image_eq))
# Print the average loss value.
print(f'Average Loss: {sum(sum(sum(abs(np.float64(loss))))) / (loss.shape[0] * loss.shape[1])}')
# Normalize the loss image for better visualization and display it.
loss = (loss - np.min(loss)) / (np.max(loss) - np.min(loss))
plt.axis('off')
plt.imshow(loss)
plt.title('Loss Image')
plt.show()
