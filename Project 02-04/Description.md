## Project 02-04 &emsp; Zooming and Shrinking Images by Bilinear Interpolation [Multiple Uses]

### Question

(a) Write a computer program capable of zooming and shrinking an image bybilinear interpolation. The input to your program is the desired size of the resultingimage in the horizontal and vertical direction. You may ignore aliasing effects.

(b) Download `rose1024.bmp` and use your program to shrink this image from $1024 \times 1024$ to $256 \times 256$ pixels.

(c) Use your program to zoom the image in (b) back to $1024 \times 1024$. Explain the reasons for their differences.

### Method

The bilinear interpolation method uses the grayscale values of the four nearest neighbors to calculate the grayscale value at a given position. Let $(x, y)$ represent the coordinates of the position to be assigned a grayscale value, and let $v(x, y)$ represent the grayscale value. For bilinear interpolation, the assigned value is obtained using the following formula:

$$
v(x, y) = ax + by + cxy + d
$$

Here, the four coefficients can be determined by solving a system of four unknown equations derived from the four nearest neighboring points of $(x, y)$. Bilinear interpolation yields much better results than nearest neighbor interpolation, but the computational cost increases as a result.

### Result

During the process of comparing the generated results with the original input image to construct the loss image, we observed that the loss is primarily concentrated in the edge regions of the image. The analysis of the loss in the edge areas is consistent with the findings from the analysis conducted in Project 02-03. When applying the bilinear interpolation algorithm for image processing, we noticed that the average loss is approximately 2.77 grayscale units. This value is lower than the average loss obtained with the nearest neighbor interpolation algorithm, indicating that bilinear interpolation can reduce the misjudgment of edge pixels to some extent.

<center class ='img'>
<img src="../figure/02-03/result.png" width="60%">
</center>
