import cv2
import os
import shutil
import numpy as np

def is_image_file(filename):
    return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))

def get_file_size_mb(filepath):
    return os.path.getsize(filepath) / (1024 * 1024)  # Convert to megabytes

def copy_small_images(input_path, output_path, file_size_mb, size_threshold):
    if file_size_mb <= size_threshold:
        shutil.copy(input_path, output_path)
        print(f"Copied small image: {os.path.basename(input_path)}")
    else:
        print(f"Skipped copying: {os.path.basename(input_path)} (size: {file_size_mb:.2f} MB)")

def reduce_image_quality(input_path, output_path, quality, max_width):
    try:
        img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise ValueError("Invalid image file")

        if img.shape[1] > max_width:
            new_width = max_width
            aspect_ratio = img.shape[1] / float(img.shape[0])
            new_height = int(new_width / aspect_ratio)
            img = cv2.resize(img, (new_width, new_height))

        cv2.imwrite(output_path, img, [cv2.IMWRITE_JPEG_QUALITY, quality])
        print(f"Processed: {os.path.basename(input_path)}")
    except Exception as e:
        print(f"Error processing image: {e} in file: {input_path}")

def process_images(input_folder, output_folder, size_threshold, quality, max_width):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for image_file in os.listdir(input_folder):
        if not is_image_file(image_file):
            print(f"Skipping non-image file: {image_file}")
            continue

        input_path = os.path.join(input_folder, image_file)
        output_path = os.path.join(output_folder, image_file)

        file_size_mb = get_file_size_mb(input_path)
        copy_small_images(input_path, output_path, file_size_mb, size_threshold)

        if file_size_mb > size_threshold:
            reduce_image_quality(input_path, output_path, quality, max_width)

try:
    input_folder_path = input("Enter the input folder path: ")
    output_folder_path = input("Enter the output folder path: ")
    max_width = int(input("Enter the maximum width for images: "))
    size_threshold = float(input("Enter the size threshold for images in MB: "))
    output_quality = int(input("Enter the output image quality (0 to 100): "))

    process_images(input_folder_path, output_folder_path, size_threshold, output_quality, max_width)
except Exception as e:
    print(f"Error: {e}")
