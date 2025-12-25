# Image-Change-Detection-Algorithm
## 📋 Objective
The goal of this project is to detect and highlight differences between distinct "before" and "after" images of the same scene. The script processes perfectly aligned image pairs to identify changes (such as missing or added objects) and annotates them with bounding boxes.

## ⚙️ Features
* **Automated Pairing:** Automatically identifies and pairs images based on naming conventions.
* **Computer Vision Pipeline:** Utilizes OpenCV for:
    * Gaussian Blurring (to reduce noise).
    * Absolute Difference calculation.
    * Thresholding and Morphological operations (dilation/erosion).
    * Contour detection.
* **Adaptive Sensitivity:** Includes a "Strict Mode" that automatically adjusts blur and threshold parameters for known noisy or problematic images (e.g., `7.jpg`, `17.jpg`).
* **Visual Annotation:** Draws bounding boxes around detected changes on the "After" image.

## 📂 Folder Structure & Naming Convention
The script relies on a specific directory structure and file naming convention to function correctly.

### Directory Layout
```text
├── Change Detection Algorithm.py  # Main script
├── input-images/                  # Source folder for image pairs
└── task_2_output/                 # Generated output folder
File Naming
Before Image: X.jpg

After Image: X~2.jpg

Annotated Output: X~3.jpg

🚀 Getting Started
Prerequisites
Ensure you have Python installed. You will need to install the following dependencies:

Bash

pip install opencv-python numpy
Usage
Place your image pairs in a folder named input-images in the same directory as the script. Ensure they follow the X.jpg and X~2.jpg naming convention.

Run the script:

Bash

python "Change Detection Algorithm.py"
The script will create a folder named task_2_output. Inside, you will find:

The original "Before" image (copied).

The processed "After" image (X~3.jpg) with bounding boxes highlighting the detected changes.

🔧 Configuration
The script contains a hardcoded list of PROBLEM_IMAGES. If specific images require different sensitivity levels (e.g., higher thresholds for lighting changes), add their filenames to this list within the code:

Python

PROBLEM_IMAGES = [
    "7.jpg", 
    "17.jpg" 
]
📝 Algorithm Overview
Load: Reads image pairs from the input directory.

Pre-process: Applies Gaussian blur to smooth details and minimize false positives from minor noise.

Compare: Computes the absolute difference between the "Before" and "After" arrays.

Filter: Applies binary thresholding and morphological opening to isolate significant changes.

Detect: Finds contours in the difference mask.

Annotate: Draws bounding boxes around contours that meet the minimum area requirement.
