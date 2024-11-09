"""
Project 02-01 Image Printing Program Based on Halftoning
Author: Billyfu
Date: 2024/10/27
"""

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# 根据题目含义定义点阵
dot = np.zeros((3, 3, 10))
dot[:, :, 1] = [[0, 255, 0], [0, 0, 0], [0, 0, 0]]
dot[:, :, 2] = [[0, 255, 0], [0, 0, 0], [0, 0, 255]]
dot[:, :, 3] = [[255, 255, 0], [0, 0, 0], [0, 0, 255]]
dot[:, :, 4] = [[255, 255, 0], [0, 0, 0], [255, 0, 255]]
dot[:, :, 5] = [[255, 255, 255], [0, 0, 0], [255, 0, 255]]
dot[:, :, 6] = [[255, 255, 255], [0, 0, 255], [255, 0, 255]]
dot[:, :, 7] = [[255, 255, 255], [0, 0, 255], [255, 255, 255]]
dot[:, :, 8] = [[255, 255, 255], [255, 0, 255], [255, 255, 255]]
dot[:, :, 9] = [[255, 255, 255], [255, 255, 255], [255, 255, 255]]


# 此函数用于调整图像大小
# 若图像超过所要求的大小，则调整其至要求的极限大小
def adaption(image):
    row, col = image.shape
    rscale = row / (816 / 3)
    cscale = col / (1056 / 3)
    # 极限大小要求的是最长的边要比要求的要小
    # 因此要找到需要缩放的最大的倍数
    scale = 1 / max(cscale, rscale)
    result = cv.resize(image, (0, 0), None, scale, scale)
    return result


# 此函数用于将一幅图像半色调化
def halftoning(image):
    # 灰度分级（分成10级）
    # 与Matlab不同，这里不加1是为了更好的索引
    image = np.floor(np.double(image) / 25.6)
    row, col = image.shape
    result = np.zeros((row * 3, col * 3))
    for i in range(row):
        for j in range(col):
            # 对每个像素所在的位置扩大为3*3的点阵，并根据灰度级赋点阵
            result[i*3:i*3+3, j*3:j*3+3] = dot[:, :, int(image[i, j])]
    return result


# Lenna图（Figs. 2.22(a)）展示
image = cv.imread('../data/face.bmp', cv.IMREAD_GRAYSCALE)
# 如果大小超过了限制，则需要对图像的大小进行缩放
# 一般 8.5英寸=816像素 11英寸=1056像素
# 但是这里需要注意的是，最后呈现的图像的边长需要扩大3倍，因此原图边上的像素还得除以3
row, col = image.shape
if (row > (816 / 3)) or (col > (1056 / 3)):
    image = adaption(image)
result = halftoning(image)

plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title("Original Image (Figs. 2.22(a))")
plt.show()

plt.axis('off')
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title("Halftoning Image (Figs. 2.22(a))")
plt.show()

# 摄影师图（Figs. 2.22(b)）展示
image = cv.imread('../data/cameraman.bmp', cv.IMREAD_GRAYSCALE)
# 如果大小超过了限制，则需要对图像的大小进行缩放
# 一般 8.5英寸=816像素 11英寸=1056像素
# 但是这里需要注意的是，最后呈现的图像的边长需要扩大3倍，因此原图边上的像素还得除以3
row, col = image.shape
if (row > (816 / 3)) or (col > (1056 / 3)):
    image = adaption(image)
result = halftoning(image)

plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title("Original Image (Figs. 2.22(b))")
plt.show()

plt.axis('off')
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title("Halftoning Image (Figs. 2.22(b))")
plt.show()

# 人群图（Figs. 2.22(c)）展示
image = cv.imread('../data/crowd.bmp', cv.IMREAD_GRAYSCALE)
# 如果大小超过了限制，则需要对图像的大小进行缩放
# 一般 8.5英寸=816像素 11英寸=1056像素
# 但是这里需要注意的是，最后呈现的图像的边长需要扩大3倍，因此原图边上的像素还得除以3
row, col = image.shape
if (row > (816 / 3)) or (col > (1056 / 3)):
    image = adaption(image)
result = halftoning(image)

plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title("Original Image (Figs. 2.22(c))")
plt.show()

plt.axis('off')
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title("Halftoning Image (Figs. 2.22(c))")
plt.show()

# 灰度测试图（Question(b)）展示
image = np.zeros((256, 256))
for i in range(256):
    image[:, i] = i
# 这里由于该图像边长像素只有256，小于816/3像素，即272像素
# 因此这里不需要对该图像进行缩放
result = halftoning(image)

plt.axis('off')
plt.imshow(image, cmap='gray', vmin=0, vmax=255)
plt.title("Original Image (Gray Scale Wedge)")
plt.show()

plt.axis('off')
plt.imshow(result, cmap='gray', vmin=0, vmax=255)
plt.title("Halftoning Image (Gray Scale Wedge)")
plt.show()
