"""
Copyright (C) 2025 Fu Tszkok

:module: Project 09-03
:function: Morphological Solution to Problem 9.27
:author: Fu Tszkok
:date: 2025-09-25
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import cv2 as cv
import matplotlib.pyplot as plt

from connected import *


def morphological_reconstruction(marker, mask, struct_elem=np.ones((3, 3), dtype=np.uint8)):
    """Performs Morphological Reconstruction by geodesic dilation.
    :param marker: The starting marker image (e.g., initial seed pixels).
    :param mask: The mask image, which limits the growth of the marker.
    :param struct_elem: The structuring element for dilation (default is 3x3 square).
    :return: The reconstructed image.
    """
    current_marker = marker.copy()
    previous_marker = np.zeros_like(marker)

    # Iterate until the marker image stabilizes (reaches idempotence).
    while not np.array_equal(current_marker, previous_marker):
        previous_marker = current_marker.copy()
        # Step 1: Dilate the current marker image.
        # Assume 'dilation' is available from the imported module.
        dilated_marker = dilation(current_marker, struct_elem)
        # Step 2: Intersect the dilated marker with the mask (geodesic dilation).
        # Assume 'intersection' is available from the imported module.
        current_marker = intersection(dilated_marker, mask)

    return current_marker


def solve_part_a(original_image):
    """Solves Question (a): Extract particles connected to the image boundary.
    :param original_image: The input binary image of particles (I).
    :return: The image containing only the particles connected to the boundary ($R_I(M)$).
    """
    # 1. Create the marker image (M) by setting pixels on the image border equal to the original image.
    marker = np.zeros_like(original_image)
    marker[0, :] = original_image[0, :]
    marker[-1, :] = original_image[-1, :]
    marker[:, 0] = original_image[:, 0]
    marker[:, -1] = original_image[:, -1]

    # 2. Perform reconstruction to grow the boundary marker to fill all connected particles.
    boundary_particles = morphological_reconstruction(marker, original_image)
    return boundary_particles


def solve_part_b(internal_particles):
    """Solves Question (b): Identify overlapping particles among internal particles.
    :param internal_particles: The binary image containing only particles not connected to the boundary.
    :return: The image containing only the identified overlapping particles.
    """
    if np.sum(internal_particles) == 0:
        return np.zeros_like(internal_particles)

    # 1. Label all connected components (individual or overlapping particles).
    # Assume 'extract_connected_components' returns the labeled image and the number of components.
    labeled_image, num_components = extract_connected_components(internal_particles)
    if num_components == 0:
        return np.zeros_like(internal_particles)

    # 2. Compute the area (pixel count) for each labeled component.
    labels, areas = np.unique(labeled_image, return_counts=True)

    # Filter out the label 0 (background).
    particle_labels = labels[1:]
    particle_areas = areas[1:]

    if len(particle_areas) == 0:
        return np.zeros_like(internal_particles)

    # 3. Determine the reference area for a single particle using the median area,
    # which is robust to a few large overlapping particles.
    single_particle_area = np.median(particle_areas)
    print(f"Single particle reference area (median): {single_particle_area:.2f} pixels")

    # 4. Set a threshold (e.g., 1.5 times the median area) to flag components as overlapping.
    area_threshold = single_particle_area * 1.5
    print(f"Area threshold for overlapping determination: > {area_threshold:.2f} pixels")

    # 5. Find the labels corresponding to the large (overlapping) particles.
    overlapping_labels = particle_labels[particle_areas > area_threshold]

    # 6. Create a binary mask of the identified overlapping particles.
    overlapping_mask = np.isin(labeled_image, overlapping_labels)
    overlapping_particles = np.zeros_like(internal_particles)
    overlapping_particles[overlapping_mask] = 1

    return overlapping_particles


def solve_part_c(internal_particles, overlapping_particles):
    """Solves Question (c): Isolate non-overlapping (simple) internal particles.
    :param internal_particles: Image of all internal particles.
    :param overlapping_particles: Image of overlapping internal particles.
    :return: Image containing only the non-overlapping internal particles.
    """
    # Assume 'difference' is available (A - B).
    non_overlapping_particles = difference(internal_particles, overlapping_particles)
    return non_overlapping_particles


# Load the grayscale image and convert it to a binary image.
image = cv.imread('../../images/bubbles_on_black_background.bmp', cv.IMREAD_GRAYSCALE)
_, original_image = cv.threshold(image, 128, 255, cv.THRESH_BINARY)

plt.axis('off')
plt.imshow(original_image, cmap='gray')
plt.title('Original Image')
plt.show()

# --- Solution for Part (a) ---
# Extract particles connected to the boundary.
image_a = solve_part_a(original_image)
# Isolate internal particles using set difference (Original - Boundary-connected).
# Assume 'difference' is available from the imported module.
internal_particles = difference(original_image, image_a)

plt.axis('off')
plt.imshow(image_a, cmap='gray')
plt.title('Question (a) Answer: Boundary-Connected Particles')
plt.show()

# --- Solution for Part (b) ---
# Identify overlapping particles among the internal particles.
image_b = solve_part_b(internal_particles)

plt.axis('off')
plt.imshow(image_b, cmap='gray')
plt.title('Question (b) Answer: Overlapping Internal Particles')
plt.show()

# --- Solution for Part (c) ---
# Isolate non-overlapping internal particles (Internal - Overlapping).
image_c = solve_part_c(internal_particles, image_b)

plt.axis('off')
plt.imshow(image_c, cmap='gray')
plt.title('Question (c) Answer: Non-Overlapping Internal Particles')
plt.show()
