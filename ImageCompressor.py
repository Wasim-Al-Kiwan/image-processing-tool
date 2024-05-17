import cv2
import os
import shutil
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox

def is_image_file(filename):
    return filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))

def get_file_size_mb(filepath):
    return os.path.getsize(filepath) / (1024 * 1024)  # Convert to megabytes

def copy_small_images(input_path, output_folder, file_size_mb, size_threshold):
    if file_size_mb <= size_threshold:
        output_path = os.path.join(output_folder, f"copied_{os.path.basename(input_path)}")
        shutil.copy(input_path, output_path)
        print(f"Copied small image: {os.path.basename(input_path)}")
    else:
        print(f"Skipped copying: {os.path.basename(input_path)} (size: {file_size_mb:.2f} MB)")

def reduce_image_quality(input_path, output_folder, quality, max_width):
    try:
        img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise ValueError("Invalid image file")

        if img.shape[1] > max_width:
            new_width = max_width
            aspect_ratio = img.shape[1] / float(img.shape[0])
            new_height = int(new_width / aspect_ratio)
            img = cv2.resize(img, (new_width, new_height))

        output_path = os.path.join(output_folder, f"compressed_{os.path.basename(input_path)}")
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
        file_size_mb = get_file_size_mb(input_path)
        copy_small_images(input_path, output_folder, file_size_mb, size_threshold)

        if file_size_mb > size_threshold:
            reduce_image_quality(input_path, output_folder, quality, max_width)

def select_input_folder():
    folder = filedialog.askdirectory()
    if folder:
        input_folder_entry.delete(0, tk.END)
        input_folder_entry.insert(0, folder)

def select_output_folder():
    folder = filedialog.askdirectory()
    if folder:
        output_folder_entry.delete(0, tk.END)
        output_folder_entry.insert(0, folder)

def start_processing():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    try:
        max_width = int(max_width_entry.get())
        size_threshold = float(size_threshold_entry.get())
        output_quality = int(output_quality_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for width, threshold, and quality.")
        return

    if not os.path.isdir(input_folder):
        messagebox.showerror("Invalid Input", "The input folder path does not exist or is not a directory.")
        return

    if not os.path.isdir(output_folder):
        try:
            os.makedirs(output_folder)
        except Exception as e:
            messagebox.showerror("Invalid Input", f"Cannot create output folder: {e}")
            return

    try:
        process_images(input_folder, output_folder, size_threshold, output_quality, max_width)
        messagebox.showinfo("Success", "Image processing completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def show_main_page():
    main_frame.tkraise()

def show_contact_page():
    contact_frame.tkraise()

app = tk.Tk()
app.title("Image Processor")
#app.iconbitmap("app_icon.ico")
# Create main frame
main_frame = tk.Frame(app)
main_frame.grid(row=0, column=0, sticky="nsew")

tk.Label(main_frame, text="Input Folder:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
input_folder_entry = tk.Entry(main_frame, width=50)
input_folder_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(main_frame, text="Browse", command=select_input_folder).grid(row=0, column=2, padx=10, pady=5)

tk.Label(main_frame, text="Output Folder:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
output_folder_entry = tk.Entry(main_frame, width=50)
output_folder_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(main_frame, text="Browse", command=select_output_folder).grid(row=1, column=2, padx=10, pady=5)

tk.Label(main_frame, text="Max Width:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
max_width_entry = tk.Entry(main_frame)
max_width_entry.grid(row=2, column=1, padx=10, pady=5)

tk.Label(main_frame, text="Size Threshold (MB):").grid(row=3, column=0, padx=10, pady=5, sticky="e")
size_threshold_entry = tk.Entry(main_frame)
size_threshold_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Label(main_frame, text="Output Quality (0-100):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
output_quality_entry = tk.Entry(main_frame)
output_quality_entry.grid(row=4, column=1, padx=10, pady=5)

tk.Button(main_frame, text="Start Processing", command=start_processing).grid(row=5, column=0, columnspan=3, pady=10)

tk.Button(main_frame, text="Contact Us", command=show_contact_page).grid(row=6, column=0, columnspan=3, pady=10)

# Create contact frame
contact_frame = tk.Frame(app)
contact_frame.grid(row=0, column=0, sticky="nsew")

tk.Label(contact_frame, text="Contact Us", font=("Arial", 16)).grid(row=0, column=0, columnspan=2, padx=10, pady=10)

tk.Label(contact_frame, text="For any technical solution, Mobile application, or website", font=("Arial", 12)).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

tk.Label(contact_frame, text="Email:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
email_entry = tk.Entry(contact_frame, width=30, font=("Arial", 10), bd=0, relief="flat", fg="blue")
email_entry.insert(0, "wasimalkiwan@gmail.com")
email_entry.configure(state='readonly')
email_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

tk.Label(contact_frame, text="Phone:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
phone_entry = tk.Entry(contact_frame, width=30, font=("Arial", 10), bd=0, relief="flat", fg="blue")
phone_entry.insert(0, "+971543503065")
phone_entry.configure(state='readonly')
phone_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

tk.Button(contact_frame, text="Back to Main", command=show_main_page).grid(row=4, column=0, columnspan=2, pady=10)

# Start with main frame
main_frame.tkraise()

app.mainloop()
