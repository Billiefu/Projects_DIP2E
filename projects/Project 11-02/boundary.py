"""
Copyright (C) 2025 Fu Tszkok

:module: boundary
:function: The function package from Project 09-02 Boundary Extraction
:author: Fu Tszkok
:date: 2025-02-06
:license: AGPLv3 + Additional Restrictions (Non-Commercial Use)

This code is licensed under GNU Affero General Public License v3 (AGPLv3) with additional terms.
- Commercial use prohibited (including but not limited to sale, integration into commercial products)
- Academic use requires clear attribution in code comments or documentation

Full AGPLv3 text available in LICENSE file or at <https://www.gnu.org/licenses/agpl-3.0.html>
"""

import numpy as np
import set_operations


def boundary_extraction(image):
    """Extracts the boundary of objects in a binary image.
    :param image: Input binary image (NumPy array).
    :return: The resulting binary image containing only the boundaries.
    """
    # First, perform an erosion operation on the binary image.
    erosion = set_operations.erosion(image, np.ones((3, 3), np.uint8))
    # Then, calculate the difference between the original image and the eroded image to obtain the boundary.
    boundary = set_operations.difference(image, erosion)
    return boundary
