import shutil, os, sys, json

from glob import glob

import numpy as np
import pandas as pd
from skimage import io
import matplotlib.pyplot as plt
from PIL import Image
from numpy.linalg import inv
from sklearn.model_selection import train_test_split
from skimage.segmentation import clear_border
import skimage
import tifffile as tiff
import vampire
from os.path import isfile, join


#--------- Validate passed Arguments -----------

# Check the number of arguments
if len(sys.argv) < 2:
    print("Usage: python example.py <arg1> <arg2> ...")
    sys.exit(1)

# Access the arguments
print("Script name:", sys.argv[0])
print("Arguments:", sys.argv[1:])

# Example of processing arguments
for i, arg in enumerate(sys.argv[1:], start=1):
    print(f"Argument {i}: {arg}")

# ------- process .npy files -------

if len(sys.argv) != 2:
    print("Usage: python script.py <root_directory>")
    sys.exit(1)

# Get the root directory from the command line
root_directory = sys.argv[1]

# Validate the root directory
if not os.path.isdir(root_directory):
    print(f"Error: The directory '{root_directory}' does not exist.")
    sys.exit(1)

# Directory to save the output TIFF files
output_dir = os.path.join(root_directory, "converted_tiffs")
os.makedirs(output_dir, exist_ok=True)

# Walk through the directory tree
for dirpath, dirnames, filenames in os.walk(root_directory):
    for file in filenames:
        if file.endswith(".npy"):
            # Construct the full path to the .npy file
            npy_path = os.path.join(dirpath, file)
            
            try:
                # Load the .npy file
                image_data = skimage.measure.label(np.load(npy_path))

                # Normalize to uint8 if needed
                # Handle boolean arrays
                if image_data.dtype == np.bool_:
                    # Convert boolean to uint8 (True -> 255, False -> 0)
                    image_data = (image_data * 255).astype(np.uint8)
                else:
                    # Normalize and scale image data to uint8 if it's not already
                    if image_data.dtype != np.uint8:
                        image_data = (
                            255 * (image_data - image_data.min()) / (image_data.ptp() + 1e-8)
                        ).astype(np.uint8)
                        
                # Construct the output TIFF file path
                relative_path = os.path.relpath(dirpath, root_directory)
                tiff_dir = os.path.join(output_dir, relative_path)
                os.makedirs(tiff_dir, exist_ok=True)
                tiff_path = os.path.join(tiff_dir, file.replace(".npy", ".tif"))

                # Save as TIFF
                #Image.fromarray(image_data).save(tiff_path)
                print(f"Converted: {npy_path} -> {tiff_path}")
                io.imsave(tiff_path, image_data)

            except Exception as e:
                print(f"Error processing '{npy_path}': {e}")

print(f"All .npy files have been converted and saved to '{output_dir}'.")

