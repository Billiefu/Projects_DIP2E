## Project 10-04 &emsp; Region Growing

> Copyright © 2002 Prentice Hall &emsp; Copyright © 2025 Fu Tszkok

### Question

(a) Implement a region-growing procedure (see Section 10.4.2) for segmenting an image into two regions.

*Hint: One approach is to grow only one region. Then, by default, the other region is the set of points left over after growth of the first region stops. At any step in the growth process, a new point is appended to the region only if a set of pre-established predicates is satisfied. For example, let s represent the average gray level of the region grown thus far at any iterative step in the procedure. One possibility is to append a new point to the region if (a) its gray level does not differ by more than a specified constant, $k$, from $s$, and (b) the point is connected (see Section 2.5.2) to the region grown thus far.*

(b) If Project 10-03 was not assigned, write a program that, given an image patch, computes the mean and variance of the pixels in the patch.

(c) Download `original_septagon.bmp` and `defective_weld.bmp`. Select a small patch in the object region and compute the mean and variance. Let the mean be the starting value of s. Use a multiple of the standard deviation as the value of $k$.

(d) Segment the image by region growing.

### Technical Discussion

[Updating]

### Experiment

[Updating]
