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

ddd

<center class ='img'>
<img src="../figure/02-03/result.png" width="80%">
</center>
