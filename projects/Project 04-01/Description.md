## Project 04-01 &emsp; Two-Dimensional Fast Fourier Transform [Multiple Uses]

> Copyright © 2002 Prentice Hall &emsp; Copyright © 2025 Fu Tszkok

### Question

The purpose of this project is to develop a 2-D FFT program "package" that will be used in several other projects that follow. Your implementation must have the capabilities to:

1. Multiply the input image by $(-1)^{x+y}$ to center the transform for filtering.
2. Multiply the resulting (complex) array by a real function (in the sense that the the real coefficients multiply both the real and imaginary parts of the transforms). Recall that multiplication of two images is done on pairs of corresponding elements.
3. Compute the inverse Fourier transform.
4. Multiply the result by $(-1)^{x+y}$ and take the real part.
5. Compute the spectrum.

Basically, this project implements Fig. 4.5. If you are using MATLAB, then your Fourier transform program will not be limited to images whose size are integer powers of 2. If you are implementing the program yourself, then the FFT routine you are using may be limited to integer powers of 2. In this case, you may need to zoom or shrink an image to the proper size by using the program you developed in Project 02-04.

**An approximation**: To simplify this and the following projects (with the exception of Project 04-05), you may ignore image padding (Section 4.6.3). Although your results will not be strictly correct, significant simplifications will be gained not only in image sizes, but also in the need for cropping the final result. The principles will not be affected by this approximation.

### Technical Discussion

[Updating]

### Experiment

[Updating]
