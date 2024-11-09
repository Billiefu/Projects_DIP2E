## PROJECT 02-01  Image Printing Program Based on Halftoning

The following figure shows ten shades of gray approximated by dot patterns. Each gray level is represented by a $3 \times 3$ pattern of black and white dots. A $3 \times 3$ area full of black dots is the approximation to gray-level black, or 0. Similarly, a $3 \times 3$ area of white dots represents gray level 9, or white. The other dot patterns are approximations to gray levels in between these two extremes. A gray-level printing scheme based on dots patterns such as these is called "halftoning." Note that each pixel in an input image will correspond to $3 \times 3$ pixels on the printed image, so spatial resolution will be reduced to 33% of the original in both the vertical and horizontal direction. Size scaling as required in (a) may further reduce resolution, depending on the size of the input image.

(a) Write a halftoning computer program for printing gray-scale images based on the dot patterns just discussed. Your program must be able to scale the size of an 
input image so that it does not exceed the area available in a sheet of size $8.5 \times 11$ inches ($21.6 \times 27.9$ cm). Your program must also scale the gray levels of the input image to span the full halftoning range.

(b) Write a program to generate a test pattern image consisting of a gray scale wedge of size $256 \times 256$, whose first column is all 0's, the next column is all 1's, and so on, with the last column being 255's. Print this image using your gray-scale printing program.

(c) Print book Figs. 2.22(a) through (c) using your gray-scale printing program. Do your results agree with the conclusions arrived at in the text in pgs. 61-62 and Fig. 2.23? Explain. You will need to download Figs. 2.22(a) through (c).

<img src=".\figure.png">  
