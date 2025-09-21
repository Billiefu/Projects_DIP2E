"""
Copyright (C) 2025 Fu Tszkok

:module: Project 06-plus
:function: Color Space-based Face Detection (YCbCr+HSV Space)
:author: Fu Tszkok
:date: 2025-02-06
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import copy
import cv2 as cv
from tqdm import tqdm
import matplotlib.pyplot as plt

# Load the original image, convert it to RGB for display, and show it.
image = cv.imread('../../images/test.bmp')
show = cv.cvtColor(copy.deepcopy(image), cv.COLOR_BGR2RGB)
plt.imshow(show)
plt.axis('off')
plt.title("Original Image")
plt.show()


# Step 1: Create a Mask using Y'CbCr Color Space
# Convert the image from BGR to Y'CbCr. This color space separates luminance
# (Y') from chrominance (Cb and Cr), making it robust to lighting variations.
ycbcr_image = cv.cvtColor(image, cv.COLOR_BGR2YCrCb)

# Define the lower and upper bounds of the target color in Y'CbCr space.
lower_ycbcr = (80, 130, 70)
upper_ycbcr = (255, 180, 120)

# Apply a Gaussian blur to the Y'CbCr image to reduce noise before thresholding.
blurred_ycbcr_image = cv.GaussianBlur(ycbcr_image, (5, 5), 0)

# Create a binary mask where pixels within the specified Y'CbCr range are white.
mask_ycbcr = cv.inRange(blurred_ycbcr_image, lower_ycbcr, upper_ycbcr)


# Step 2: Create a Mask using HSV Color Space
# Convert the image from BGR to HSV. This color space is also highly effective
# for color segmentation as it separates Hue, Saturation, and Value.
hsv_image = cv.cvtColor(image, cv.COLOR_BGR2HSV)

# Define the lower and upper bounds of the target color in HSV space.
lower_hsv = (0, 20, 60)
upper_hsv = (50, 150, 255)

# Apply a Gaussian blur to the HSV image for noise reduction.
blurred_hsv_image = cv.GaussianBlur(hsv_image, (5, 5), 0)

# Create a binary mask where pixels within the specified HSV range are white.
mask_hsv = cv.inRange(blurred_hsv_image, lower_hsv, upper_hsv)


# Step 3: Combine and Refine the Masks
# Combine the two masks using a logical AND operation. This creates a final mask
# where a pixel is white only if it was within the color range in BOTH Y'CbCr
# and HSV color spaces, increasing the precision of the segmentation.
combined_mask = cv.bitwise_and(mask_ycbcr, mask_hsv)

# Define a morphological kernel, in this case, an ellipse shape.
kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (7, 7))

# Apply morphological operations to clean the combined mask.
# cv.MORPH_CLOSE fills small holes within the detected regions.
mask_cleaned = cv.morphologyEx(combined_mask, cv.MORPH_CLOSE, kernel)
# cv.MORPH_OPEN removes small noise specks outside the main regions.
mask_cleaned = cv.morphologyEx(mask_cleaned, cv.MORPH_OPEN, kernel)


# Step 4: Contour Detection and Filtering
# Find the contours (boundaries) of the detected regions in the cleaned mask.
contours, _ = cv.findContours(mask_cleaned, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
# Set the line width for drawing rectangles based on image dimensions.
width = max(int(image.shape[0]/400), int(image.shape[1]/400))
# Iterate through the detected contours with a progress bar.
for contour in tqdm(contours, desc="Processing contours"):
    # Filter contours based on their area and aspect ratio to identify potential objects.
    if cv.contourArea(contour) > 1000:
        x, y, w, h = cv.boundingRect(contour)

        # Check if the object's aspect ratio is approximately square or circular.
        aspect_ratio = w / h
        if 0.75 < aspect_ratio < 1.5:
            # Draw a green rectangle around the detected object on the original image.
            cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), width)


# Step 5: Display the Final Result
# Convert the image with drawn rectangles to RGB for display.
image_rgb = image
image_rgb = cv.cvtColor(image_rgb, cv.COLOR_BGR2RGB)
plt.imshow(image_rgb)
plt.axis('off')
plt.title("Detected Image (Y'CbCr + HSV)")
plt.show()
