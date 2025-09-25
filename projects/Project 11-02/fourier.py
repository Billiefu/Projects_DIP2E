"""
Copyright (C) 2025 Fu Tszkok

:module: fourier
:function: The function package from Project 11-02 Fourier Descriptors
:author: Fu Tszkok
:date: 2025-09-25
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

from scipy.interpolate import interp1d

from boundary import *
from set_operations import *


def get_counter(binary_image):
    """Performs boundary tracing on a binary image using a radial sweep/bug method.
    :param binary_image: Input binary image (NumPy array).
    :return: A NumPy array of (x, y) coordinates representing the traced contour.
    """
    # Use morphological boundary extraction (A - A eroded) to get a thin boundary.
    boundary_image = boundary_extraction(binary_image)

    tracing_mask = (boundary_image > 0).astype(np.uint8)
    rows, cols = tracing_mask.shape

    # Find the starting point for tracing (the first foreground pixel encountered).
    start_point_rc = None
    for r in range(rows):
        for c in range(cols):
            if tracing_mask[r, c] == 1:
                start_point_rc = (r, c)
                break
        if start_point_rc:
            break

    if not start_point_rc:
        print("Warning: No boundary points found for tracing.")
        return np.array([])

    # 8-connectivity neighbors in counter-clockwise (CCW) order, starting from East (0, 1).
    neighbors_ccw = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    current_r, current_c = start_point_rc
    # Contour points are stored as (c, r) -> (x, y).
    contour = [(current_c, current_r)]

    # Start searching from the neighbor index that is most likely to be the next boundary point.
    # Initial search direction is set to 5 (West) to ensure the first step is correct.
    search_dir_start = 5
    max_iter = rows * cols * 2  # Safety brake to prevent infinite loops.

    for _ in range(max_iter):
        found_next = False

        for i in range(8):
            # Rotate search direction CCW. The search logic ensures boundary following.
            current_dir_idx = (search_dir_start + i) % 8

            dr, dc = neighbors_ccw[current_dir_idx]

            next_r, next_c = current_r + dr, current_c + dc
            next_point_rc = (next_r, next_c)

            # Check if the next point is valid (within bounds and is a boundary pixel).
            if 0 <= next_r < rows and 0 <= next_c < cols and tracing_mask[next_r, next_c] == 1:
                # Break condition: If the starting point is reached and the contour has been formed.
                if next_point_rc == start_point_rc and len(contour) > 1:
                    found_next = True
                    break

                # Update current position and add to contour.
                contour.append((next_c, next_r))
                current_r, current_c = next_r, next_c

                # Update the starting search direction for the next iteration (backtrack: (current_dir_idx - 1) % 8).
                search_dir_start = (current_dir_idx + 7) % 8
                found_next = True
                break

        if not found_next:
            # Tracing stopped before returning to the start point (e.g., failed to find a neighbor).
            break
        if next_point_rc == start_point_rc and len(contour) > 1:
            # Boundary closure achieved.
            break

    points = np.array(contour)
    if len(points) < 2:
        print("Warning: Boundary tracing failed or found fewer than 2 points.")
        return np.array([])

    return points


def get_boundary_points(points, num_points):
    """Samples the contour points to get a fixed, uniformly-spaced number of points.
    :param points: NumPy array of (x, y) contour points.
    :param num_points: The desired number of uniformly sampled points.
    :return: A NumPy array of the sampled (x, y) boundary points.
    """
    if points.ndim == 1 or len(points) < 2:
        print("Warning: Contour contains fewer than 2 points.")
        return np.array([])

    # Calculate the distance between consecutive points (arc length segments).
    distances = np.sqrt(np.sum(np.diff(points, axis=0) ** 2, axis=1))
    # Calculate the cumulative distance along the contour.
    cumulative_distances = np.insert(np.cumsum(distances), 0, 0)
    total_length = cumulative_distances[-1]

    if total_length == 0:
        print("Warning: Contour has zero length.")
        return np.array([])

    # Define the desired distances for uniform sampling.
    desired_distances = np.linspace(0, total_length, num_points)

    # Use linear interpolation to find the (x, y) coordinates at the desired distances.
    f_x = interp1d(cumulative_distances, points[:, 0], kind='linear')
    f_y = interp1d(cumulative_distances, points[:, 1], kind='linear')

    sampled_x = f_x(desired_distances)
    sampled_y = f_y(desired_distances)

    sampled_points = np.vstack((sampled_x, sampled_y)).T
    return sampled_points


def fourier_descriptor(points):
    """Calculates the Fourier Descriptors of the boundary points.
    :param points: NumPy array of uniformly sampled (x, y) boundary points.
    :return: A NumPy array of the complex Fourier Descriptors.
    """
    # Convert boundary coordinates to a complex sequence.
    complex_sequence = points[:, 0] + 1j * points[:, 1]
    # Compute the DFT using the Fast Fourier Transform (FFT) algorithm.
    descriptors = np.fft.fft(complex_sequence)
    return descriptors


def reconstruct_boundary(descriptors, num_coefficients):
    """Reconstructs the boundary using a limited number of Fourier Descriptors.
    :param descriptors: The full array of complex Fourier Descriptors.
    :param num_coefficients: The number of low-frequency descriptors to use (P).
    :return: A NumPy array of the reconstructed (x, y) boundary points.
    """
    K = len(descriptors)
    P = num_coefficients

    reconstructed_descriptors = np.zeros_like(descriptors)

    # Ensure P is even for symmetric selection of frequency components.
    if P % 2 != 0:
        P += 1

    num_half = P // 2

    # Retain the DC component (u_0). This relates to the shape's center of mass.
    reconstructed_descriptors[0] = descriptors[0]
    # Retain the first $P/2 - 1$ positive frequency components ($u_1$ to $u_{P/2-1}$).
    reconstructed_descriptors[1:num_half] = descriptors[1:num_half]
    # Retain the corresponding negative frequency components ($u_{K-P/2+1}$ to $u_{K-1}$).
    reconstructed_descriptors[K - num_half + 1:] = descriptors[K - num_half + 1:]

    # Apply the Inverse DFT (IDFT) to the filtered set of descriptors.
    reconstructed_sequence = np.fft.ifft(reconstructed_descriptors)
    # Convert the complex sequence back to real (x) and imaginary (y) coordinates.
    reconstructed_points = np.vstack((reconstructed_sequence.real, reconstructed_sequence.imag)).T

    return reconstructed_points
