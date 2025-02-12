import shutil, os

from glob import glob

import numpy as np
import pandas as pd
from skimage import io
import matplotlib.pyplot as plt
from PIL import Image
from numpy.linalg import inv
from sklearn.model_selection import train_test_split
from skimage.segmentation import clear_border

def split_files(input_folder, output_folder):
    """
    
    """
    if not os.path.isdir(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        return

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Walk through all files and subfolders
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".npy"):
                # Full input path
                input_path = os.path.join(root, file)

                # Create corresponding output subfolder
                relative_path = os.path.relpath(root, input_folder)
                output_subfolder = os.path.join(output_folder, relative_path)
                os.makedirs(output_subfolder, exist_ok=True)

                # Full output path
                output_path_1 = os.path.join(output_subfolder, file.replace(".npy", "_quad1.npy"))
                output_path_2 = os.path.join(output_subfolder, file.replace(".npy", "_quad2.npy"))
                output_path_3 = os.path.join(output_subfolder, file.replace(".npy", "_quad3.npy"))
                output_path_4 = os.path.join(output_subfolder, file.replace(".npy", "_quad4.npy"))

                try:
                    file_to_split = np.load(input_path)
                    quada, quadb = np.array_split(file_to_split, 2)
                    quad1, quad2 = np.array_split(quada, 2, axis=1)
                    quad3, quad4 = np.array_split(quadb, 2, axis=1)
                    
                    quad1 = clear_border(quad1)
                    quad2 = clear_border(quad2)
                    quad3 = clear_border(quad3)
                    quad4 = clear_border(quad4)

                    
                    np.save(output_path_1, quad1)
                    np.save(output_path_2, quad2)
                    np.save(output_path_3, quad3)
                    np.save(output_path_4, quad4)
                
                except Exception as e:
                    print(f"Error processing {input_path}: {e}")

# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python split_files.py <input_folder> <output_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    split_files(input_folder, output_folder)
