# Image Batch Processor

This Python script is designed for batch processing a large number of images at once. It allows you to compress images, set a minimum size threshold for compression, resize images, and set a minimum width threshold for resizing. Additionally, you can specify a destination folder to store the processed images.

## Features

- **Batch Compression:**
  - Compress a large number of images at once.
  - Set a minimum size threshold for compression.

- **Batch Resize:**
  - Resize images to a specified dimension.
  - Set a minimum width threshold for resizing.

- **Selective Processing:**
  - Copy images that do not meet the processing criteria to the destination folder without modification.

## Usage

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/your-repository.git
   cd your-repository

2. **Install Dependencies:**
  ```bash
  pip install opencv-python

3. **Run the Script:**
  ```bash
  python image_batch_processor.py

**Example** 
Enter the input folder path: /path/to/input/folder
Enter the output folder path: /path/to/output/folder
Enter the minimum size threshold for compression (MB): 1.5
Enter the minimum width threshold for resizing: 800
