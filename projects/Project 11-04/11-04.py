"""
Copyright (C) 2025 Fu Tszkok

:module: Project 11-04
:function: Principal Components
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
import numpy as np


def calculate_pca(data_matrix):
    """Computes the mean vector, covariance matrix, and sorted eigenvalues/eigenvectors.
    :param data_matrix: Data matrix (K x N), where K is the number of samples (pixels) and N is the number of features (bands).
    :return: Tuple of (sorted_EigVal, sorted_EigVec, m_x - mean vector).
    """
    # 1. Compute the mean vector (m_x) of the data features (bands).
    m_x = np.mean(data_matrix, axis=0)
    # 2. Center the data (Z = X - m_x).
    Z = data_matrix - m_x
    # 3. Compute the covariance matrix (C_x). rowvar=False means columns are features.
    C_x = np.cov(Z, rowvar=False)
    # 4. Compute the eigenvalues and eigenvectors.
    EigVal, EigVec = np.linalg.eig(C_x)

    # 5. Sort eigenvalues in descending order and sort eigenvectors accordingly.
    order = np.argsort(EigVal)[::-1]
    sorted_EigVal = EigVal[order]
    sorted_EigVec = EigVec[:, order]
    return sorted_EigVal, sorted_EigVec, m_x


def transform_to_pc(data_matrix, sorted_EigVec):
    """Transforms the centered data onto the Principal Component basis (eigenvectors).
    :param data_matrix: Original data matrix (K x N).
    :param sorted_EigVec: Sorted eigenvector matrix (N x N).
    :return: Principal Component (PC) score matrix (K x N).
    """
    # Recenter the data.
    m_x = np.mean(data_matrix, axis=0)
    Z = data_matrix - m_x
    # Project centered data onto the eigenvector matrix.
    PC_matrix = Z @ sorted_EigVec
    return PC_matrix


def reconstruct_data(PC_matrix, m_x, sorted_EigVec, k):
    """Reconstructs the original data using only the first k Principal Components.
    :param PC_matrix: Principal Component score matrix (K x N).
    :param m_x: Mean vector (1 x N).
    :param sorted_EigVec: Sorted eigenvector matrix (N x N).
    :param k: Number of PCs to retain.
    :return: Reconstructed data matrix ($\hat{X}$).
    """
    # Select the first k eigenvectors (transpose required for matrix slicing).
    A_k = sorted_EigVec.T[:k, :]
    # Select the first k PC scores.
    Y_k = PC_matrix[:, :k]
    # Perform reconstruction and add the mean vector back.
    X_hat = (Y_k @ A_k) + m_x
    return X_hat


# Load the 6 grayscale bands of the WashingtonDC dataset.
band_images = [cv.imread(f'../../images/WashingtonDCBand{i}.bmp', cv.IMREAD_GRAYSCALE) for i in range(1, 7)]

H, W = band_images[0].shape
N = len(band_images)  # Number of bands (features).
K = H * W             # Number of pixels (samples).

# Display the original band images.
plt.figure(figsize=(13, 8))
for i in range(N):
    plt.subplot(2, 3, i + 1)
    plt.axis('off')
    plt.imshow(band_images[i], cmap='gray')
    plt.title(f'Band {i+1}')
plt.show()

print(f'Size: {H}x{W}, Number of bands: {N}')


# --- Data Structuring ---
# Flatten each band into a vector (size K).
data_vectors = [band.flatten() for band in band_images]
# Stack the vectors to form the Data Matrix (K x N), where K=pixels (samples), N=bands (features).
data_matrix = np.stack(data_vectors, axis=1).astype(np.float64)


# --- PCA Calculation ---
sorted_EigVal, sorted_EigVec, m_x = calculate_pca(data_matrix)
# A is the matrix of eigenvectors (Principal Components direction).
A = sorted_EigVec.T
# Transform the data to get the PC scores (Y).
PC_matrix = transform_to_pc(data_matrix, sorted_EigVec)

np.set_printoptions(precision=2, suppress=True)
print(f'Mean vector: {m_x}')


# --- Variance Analysis ---
total_variance = np.sum(sorted_EigVal)
# Variance explained by each PC (Eigenvalue) as a percentage of total variance.
variance_ratio = sorted_EigVal / total_variance * 100
print(f"Total variance: {total_variance:.4e}")
print()


# Print the results of the variance analysis.
header = "{:<10}{:<15}{:<25}{:<25}".format(
    "PC", "Eigenvalue", "Variance Percentage", "Cumulative Percentage"
)
separator = "-" * len(header)

print(separator)
print(header)
print(separator)
cumulative_variance = 0
for i in range(N):
    cumulative_variance += variance_ratio[i]
    row = "{:<10}{:<15.4f}{:<25.2f}{:<25.2f}".format(
        i+1, sorted_EigVal[i], variance_ratio[i] , cumulative_variance
    )
    print(row)
print()


# --- Visualization of Principal Component Images ---
np.set_printoptions(precision=8, suppress=False)
# Reshape the PC scores (K) back into image form (H x W).
principal_components = [PC_matrix[:, i].reshape(H, W) for i in range(N)]

plt.figure(figsize=(13, 8))
for i in range(N):
    pc_image = principal_components[i]
    # Normalize the PC image for display purposes (stretching values from 0 to 1).
    normalized_pc = (pc_image - np.min(pc_image)) / (np.max(pc_image) - np.min(pc_image))

    plt.subplot(2, 3, i + 1)
    plt.axis('off')
    plt.imshow(normalized_pc, cmap='gray')
    # PC1 captures the most variance (Eigenvalue is highest) and often shows the main contrast.
    plt.title(f'PC{i+1}  (λ={sorted_EigVal[i]:.2f})')
plt.show()


# --- Data Reconstruction and Error Analysis ---
# Number of Principal Components to retain for reconstruction (dimensionality reduction).
k = 2
# The sum of discarded eigenvalues represents the error variance (Mean Square Error).
error_variance = np.sum(sorted_EigVal[k:])
# The Root Mean Square (RMS) Error of the reconstruction.
e_rms = np.sqrt(error_variance)
# Cumulative variance retained by the first k PCs.
k_cumulative_variance = np.sum(variance_ratio[:k])

print(f"Discarded Eigenvalues (Variance): {sorted_EigVal[k:]}")
print(f"Mean Square Error (Sum of Discarded Variances): {error_variance:.4f}")
print(f"Root Mean Square Error: {e_rms:.4f}")
print(f"Using the first {k} PCs retains {k_cumulative_variance:.2f}% of the variance information.")

# Reconstruct the data using only the first k Principal Components.
X_hat = reconstruct_data(PC_matrix, m_x, sorted_EigVec, k)
# Reshape the reconstructed vectors back into image form.
reconstructed_bands = [X_hat[:, i].reshape(H, W) for i in range(N)]


# --- Visualization of Reconstruction Loss for Band 1 ---
band1_original = band_images[0]
band1_reconstructed = reconstructed_bands[0]
# Calculate the absolute difference (loss) between original and reconstructed Band 1.
band1_loss = np.abs(band1_original - band1_reconstructed)

plt.figure(figsize=(13, 4))
plt.subplot(1, 3, 1)
plt.axis('off')
plt.imshow(band1_original, cmap='gray')
plt.title('Original Band1 Image')

plt.subplot(1, 3, 2)
plt.axis('off')
plt.imshow(band1_reconstructed, cmap='gray')
plt.title('Reconstructed Band1 Image')

plt.subplot(1, 3, 3)
plt.axis('off')
plt.imshow(band1_loss, cmap='gray')
plt.title('Band1 Loss Image')
plt.show()
