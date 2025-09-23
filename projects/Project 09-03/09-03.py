"""
Copyright (C) 2025 Fu Tszkok

:module: Project 09-03
:function: Connected Components [Multiple Uses]
:author: Fu Tszkok
:date: 2025-09-23
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import cv2 as cv
import matplotlib.pyplot as plt

from set_operations import *


def find_root(equivalences, label):
    """Finds the root of a label in the Union-Find data structure with path compression.
    :param equivalences: A list or array representing the parent pointers of labels.
    :param label: The label whose root needs to be found.
    :return: The root label.
    """
    while equivalences[label] != label:
        # Path compression: make each node point to its grandparent.
        equivalences[label] = equivalences[equivalences[label]]
        label = equivalences[label]
    return label


def extract_connected_components(binary_image, connectivity=8):
    """Performs connected component labeling on a binary image using a two-pass algorithm.
    :param binary_image: The input binary image (0 for background, >0 for foreground).
    :param connectivity: The type of connectivity to consider (4 or 8). Default is 8.
    :return: A tuple containing the labeled image and the total count of components.
    """
    # Ensure the image is in a binary format (0 or 1).
    binary_image = (binary_image > 0).astype(np.uint8)
    h, w = binary_image.shape
    # Initialize an image to store the labels.
    labeled_image = np.zeros_like(binary_image, dtype=np.int32)
    next_label = 1

    # Initialize the equivalence list for the Union-Find algorithm.
    # The list maps a label to its root.
    equivalences = [0]

    # Pass 1: Labeling and Equivalence Recording
    for r in range(h):
        for c in range(w):
            if binary_image[r, c] == 1:
                neighbors = []
                # Check for labeled neighbors based on the connectivity (4 or 8).
                if r > 0:
                    if labeled_image[r - 1, c] != 0: neighbors.append(labeled_image[r - 1, c])
                    if connectivity == 8:
                        if c > 0 and labeled_image[r - 1, c - 1] != 0: neighbors.append(labeled_image[r - 1, c - 1])
                        if c < w - 1 and labeled_image[r - 1, c + 1] != 0: neighbors.append(labeled_image[r - 1, c + 1])
                if c > 0 and labeled_image[r, c - 1] != 0: neighbors.append(labeled_image[r, c - 1])

                if not neighbors:
                    # If no labeled neighbors, assign a new unique label.
                    labeled_image[r, c] = next_label
                    equivalences.append(next_label)
                    next_label += 1
                else:
                    # If neighbors exist, assign the minimum label to the current pixel.
                    min_label = min(neighbors)
                    labeled_image[r, c] = min_label

                    # Record equivalences: union the sets of all neighboring labels.
                    for label in neighbors:
                        root_min = find_root(equivalences, min_label)
                        root_current = find_root(equivalences, label)
                        if root_min != root_current:
                            equivalences[root_current] = root_min

    # Pass 2: Equivalence Resolution and Final Labeling
    final_labels = {}
    component_count = 0
    for r in range(h):
        for c in range(w):
            label = labeled_image[r, c]
            if label > 0:
                # Find the root of the current pixel's label.
                root_label = find_root(equivalences, label)

                # Assign a new, unique label for each distinct root.
                if root_label not in final_labels:
                    component_count += 1
                    final_labels[root_label] = component_count

                # Update the pixel's label with its final, resolved label.
                labeled_image[r, c] = final_labels[root_label]

    return labeled_image, component_count


# Load the image, apply a Gaussian blur for pre-processing, and convert to binary.
image = cv.imread('../../images/region-filling-reflections.bmp', cv.IMREAD_GRAYSCALE)
_, binary_image = cv.threshold(image, 138, 255, cv.THRESH_BINARY)
plt.axis('off')
plt.imshow(binary_image, cmap='gray')
plt.title('Original Binary Image')
plt.show()

# Perform connected component labeling.
labeled_image, component_label = extract_connected_components(binary_image)
print("The number of connected components is: ", component_label)
plt.axis('off')
# Display the labeled image. Each component (unique label) will have a distinct shade of gray.
plt.imshow(labeled_image, cmap='gray')
plt.title('Connected Components')
plt.show()
