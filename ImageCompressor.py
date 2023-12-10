import cv2
import os
import shutil
import numpy as np

def copy_small_images(input_path, output_path, size_threshold=1.5):
    """
    Copy images from the input folder to the output folder if their size is below the threshold.

    Parameters:
    - input_path (str): Path to the input image file.
    - output_path (str): Path to save the output image file.
    - size_threshold (float): Threshold for image size in megabytes. Images below this size will be copied.
    """
    try:
        # Check the file size
        file_size_mb = os.path.getsize(input_path) / (1024 * 1024)  # Convert to megabytes

        if file_size_mb <= size_threshold:
            shutil.copy(input_path, output_path)
            print(f"Copied small image: {os.path.basename(input_path)}")
    except Exception as e:
        print(f"Error copying small image: {e}")

def reduce_image_quality(input_path, output_path, quality=50, max_width=2048):
    """
    Reduces the quality and resizes an image if its width exceeds a specified limit,
    and saves it to a new file.

    Parameters:
    - input_path (str): Path to the input image file.
    - output_path (str): Path to save the output image file.
    - quality (int): Compression quality (0 to 100). Higher values mean better quality.
    - max_width (int): Maximum width for the image. If the image width exceeds this, it will be resized.
    """
    try:
        # Read the image
        with open(input_path, 'rb') as f:
            img_bytes = f.read()
            image = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_UNCHANGED)

        # Resize if the image width exceeds the specified limit
        if image is not None and image.shape[1] > max_width:
            new_width = max_width
            aspect_ratio = image.shape[1] / float(image.shape[0])
            new_height = int(new_width / aspect_ratio)
            image = cv2.resize(image, (new_width, new_height))

        # Set the compression parameters
        compression_params = [cv2.IMWRITE_JPEG_QUALITY, quality]

        # Save the image with reduced quality
        cv2.imwrite(output_path, image, compression_params)

        print(f"Processed: {os.path.basename(input_path)}")
    except Exception as e:
        print(f"Error processing image: {e}")

def process_images(input_folder, output_folder, size_threshold=1.5, quality=50, max_width=2048):
    """
    Process images in the input folder, copying small images and compressing/larger ones.

    Parameters:
    - input_folder (str): Path to the input folder containing images.
    - output_folder (str): Path to save the processed images.
    - size_threshold (float): Threshold for image size in megabytes. Images above this size will be processed.
    - quality (int): Compression quality (0 to 100) for the output images.
    - max_width (int): Maximum width for the output images.
    """
    try:
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # List all image files in the input folder
        image_files = [f for f in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, f))]

        # Process each image file
        for image_file in image_files:
            input_path = os.path.join(input_folder, image_file)
            output_path = os.path.join(output_folder, image_file)

            # Check if the file is an image
            if not image_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                print(f"Skipping non-image file: {image_file}")
                continue

            # Check the file size and copy small images
            copy_small_images(input_path, output_path, size_threshold)

            # Process larger images
            if os.path.getsize(input_path) / (1024 * 1024) > size_threshold:
                reduce_image_quality(input_path, output_path, quality, max_width)
    except Exception as e:
        print(f"Error processing images: {e}")

# Example usage:

input_folder_path = input("Enter the input folder path: ")
output_folder_path = input("Enter the output folder path: ")
max_width = int(input("Enter the maximum width for images: "))
size_threshold = float(input("Enter the size threshold for images in (MB): "))
output_quality = int(input("Enter the output image quality (0 to 100): "))

process_images(input_folder_path, output_folder_path, size_threshold, output_quality, max_width)
