# Laboratory Projects for Digital Image Processing (Second Edition)

> Copyright © 2002 Prentice Hall &emsp; Copyright © 2025 Fu Tszkok

## Description

In order to better assist students and colleagues dedicated to learning digital image processing, this project repository will provide experimental descriptions and corresponding code implementation results for related experiments in digital image processing. This project repository is built upon the laboratory projects of the classic textbook "Digital Image Processing" by Rafael C. Gonzalez and Richard E. Woods, second edition. Here, we first want to express our deepest respect to *Professor Lai Jianhuang* from Sun Yat-sen University, for personally teaching us this challenging course. At the same time, we also want to thank our teaching assistant *Ye Biaohua* for providing valuable guidance and assistance with our laboratory projects codes. Despite this, we are fully aware that there is still room for improvement and enhancement in some projects within the repository. Therefore, we sincerely welcome any valuable opinions and suggestions from students and colleagues to help us continuously improve and enhance the quality of the projects.

All projects in this repository can be completed with the assistance of relevant image processing libraries. For example, the projects in this repository are implemented using Python, with tools such as the `Numpy` library and `OpenCV` library aiding in their completion. However, relying solely on "ready-made" examples as the only approach to implementing an entire project is discouraged.

We encourage students and colleagues to independently develop basic frameworks based on the principles of various algorithms and then use libraries to assist in completing more challenging parts within the framework. A good example is implementing a two-dimensional Fast Fourier Transform (2D FFT). A recommended approach is to utilize the function for directly computing 2D FFTs provided by the `Numpy` library, but also to write custom functions for tasks such as centering the transform, multiplying it by a filter function, and obtaining the spectrum.

## Copyright Statement

All original code in this repository is licensed under the **[GNU Affero General Public License v3](LICENSE)**, with additional usage restrictions specified in the **[Supplementary Terms](ADDITIONAL_TERMS.md)**. All original images in this repository are protected under the copyright of the original author, the original book and [**their original providers**](https://www.imageprocessingplace.com/root_files_V3/image_databases.htm). Users must expressly comply with the following conditions:

* **Commercial Use Restriction**
  Any form of commercial use, integration, or distribution requires prior written permission.
* **Academic Citation Requirement**When referenced in research or teaching, proper attribution must include:
  * Original author credit
  * Link to this repository
* **Academic Integrity Clause**
  Prohibits submitting this code (or derivatives) as personal academic work without explicit authorization.

The full legal text is available in the aforementioned license documents. Usage of this repository constitutes acceptance of these terms. The usage copyright for all source code files of this project are formally granted to the **Digital Image Processing Research Group, School of Computer Science and Engineering, Sun Yat-sen University**. This license covers all related research, teaching, and internal testing activities of the said research group.

## Environment

To run the code in this experiment repository, you need to set up the required environment. Although configuring a Conda environment is not particularly difficult, this repository provides a pre-defined environment setup stored in the `environment.yml` file located in the root directory.

To configure the environment, ensure that you have Anaconda or Miniconda installed. After installing the environment, switch to the current directory in the command line (cmd) and run the following command:

```shell
conda env create -f environment.yml
```

If there are no issues, the environment should be created successfully. You can then activate the environment by running the following command in the command line:

```shell
conda activate YatDIP
```

If you are using PyCharm, VSCode, or other IDEs, you can configure the environment directly within the IDE and run the relevant programs from there.

## Project list

The description and solution for the following experimental projects will be mentioned in the `Descirption.md` file within the project folder. Some projects are designated as "**Multiple uses**" because their results are used in subsequent projects. These projects should be given assignment priority. The label *[MULTIPLE USES]* indicates that all or part of a project's results will be used in subsequent projects, the same as "Multiple uses" designation. Some projects are still under continuous updates, please pay attention to the instructions in the Remark section.


| Project No. | Title                                                   |   Comments   |  Remark  |
| :----------: | :------------------------------------------------------ | :-----------: | :------: |
|  Proj 00-00  | Suggested format for submitting project reports         |              | Finished |
|  Proj 02-01  | Image Printing Program Based on Halftoning              |              | Finished |
|  Proj 02-02  | Reducing the Number of Gray Levels in an Image          |              | Finished |
|  Proj 02-03  | Zooming and Shrinking Images by Pixel Replication       |              | Finished |
|  Proj 02-04  | Zooming and Shrinking Images by Bilinear Interpolation  | Multiple uses | Finished |
|  Proj 03-01  | Image Enhancement Using Intensity Transformations       |              | Finished |
|  Proj 03-02  | Histogram Equalization                                  | Multiple uses | Finished |
|  Proj 03-03  | Arithmetic Operations                                   | Multiple uses | Finished |
|  Proj 03-04  | Spatial Filtering                                       | Multiple uses | Finished |
|  Proj 03-05  | Enhancement Using the Laplacian                         |              | Finished |
|  Proj 03-06  | Unsharp Masking                                         |              | Finished |
|  Proj 04-01  | Two-Dimensional Fast Fourier Transform                  | Multiple uses | Finished |
|  Proj 04-02  | Fourier Spectrum and Average Value                      |              | Finished |
|  Proj 04-03  | Lowpass Filtering                                       |              | Finished |
|  Proj 04-04  | Highpass Filtering Using a Lowpass Image                |              | Finished |
|  Proj 04-05  | Correlation in the Frequency Domain                     |              | Finished |
|  Proj 05-01  | Noise Generators                                        | Multiple uses | Finished |
|  Proj 05-02  | Noise Reduction Using a Median Filter                   |              | Finished |
|  Proj 05-03  | Periodic Noise Reduction Using a Notch Filter           |              | Finished |
|  Proj 05-04  | Parametric Wiener Filter                                |              | Finished |
|  Proj 06-01  | Web-Safe Colors                                         |              | Finished |
|  Proj 06-02  | Pseudo-Color Image Processing                           |              | Finished |
|  Proj 06-03  | Color Image Enhancement by Histogram Processing         |              | Finished |
|  Proj 06-04  | Color Image Segmentation                                |              | Finished |
| Proj 06-plus | Face Recognition Based On Color Space                   |              | Finished |
|  Proj 07-01  | One-Dimensional Discrete Wavelet Transforms             | Multiple uses |   Todo   |
|  Proj 07-02  | Two-dimensional Discrete Wavelet Transforms             | Multiple uses |   Todo   |
|  Proj 07-03  | Wavelet Transform Modifications                         |              |   Todo   |
|  Proj 07-04  | Image De-Noising                                        |              |   Todo   |
|  Proj 08-01  | Objective Fidelity Criteria                             | Multiple uses |   Todo   |
|  Proj 08-02  | Image Entropy                                           |              |   Todo   |
|  Proj 08-03  | Transform Coding                                        |              |   Todo   |
|  Proj 08-04  | Wavelet Coding                                          |              |   Todo   |
|  Proj 09-01  | Morphological and Other Set Operations                  | Multiple uses | Finished |
|  Proj 09-02  | Boundary Extraction                                     | Multiple uses | Finished |
|  Proj 09-03  | Connected Components                                    | Multiple uses | Finished |
|  Proj 09-04  | Morphological Solution to Problem 9.27                  |              | Finished |
|  Proj 10-01  | Edge Detection Combined with Smoothing and Thresholding |              | Finished |
|  Proj 10-02  | Global Thresholding                                     | Multiple uses | Finished |
|  Proj 10-03  | Optimum Thresholding                                    |              | Finished |
| Proj 10-03-2 | Optimum Thresholding Based on Otsu                      |              | Finished |
|  Proj 10-04  | Region Growing                                          |              | Finished |
|  Proj 11-01  | Skeletons                                               |              | Finished |
|  Proj 11-02  | Fourier Descriptors                                     | Multiple uses | Finished |
|  Proj 11-03  | Texture                                                 |              | Finished |
|  Proj 11-04  | Principal Components                                    |              | Finished |
|  Proj 12-01  | Generating Pattern Classes                              | Multiple uses |   Todo   |
|  Proj 12-02  | Minimum Distance Classifier                             |              |   Todo   |
|  Proj 12-03  | Bayes Classifier                                        |              |   Todo   |
|  Proj 12-04  | Perceptron Classifier                                   |              |   Todo   |

All project files are stored in the `projects` folder. Experimental images are stored in the `images` folder, while the `figures` folder is specifically for display images needed in the description files. Please be sure to comply with copyright agreements, as most experimental images are protected.

## Contact & Authorization

For technical inquiries, academic collaboration, or commercial licensing, contact the copyright holder via:

* **Academic Email**: `futk@mail2.sysu.edu.cn`
* **Project Discussions**: [Github Issues](https://github.com/Billiefu/Projects_DIP2E/issues)
* **Project Website**: [Projects](https://www.imageprocessingplace.com/root_files_V3/projects.htm)
