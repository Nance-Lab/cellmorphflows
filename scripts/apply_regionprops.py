import os
import numpy as np
import pandas as pd
from skimage.measure import label, regionprops_table

properties_list = ('area', 'bbox_area', 'centroid', 'convex_area', 
                   'eccentricity', 'equivalent_diameter', 'euler_number', 
                   'extent', 'filled_area', 'major_axis_length', 
                   'minor_axis_length', 'orientation', 'perimeter', 'solidity')

def process_npy_files(input_folder, output_csv, properties_list):
    """
    Processes all `.npy` files in the input folder (and subfolders), applies labeling,
    calculates properties, and saves results in a CSV file.

    Parameters:
    - input_folder: Path to the folder containing `.npy` files.
    - output_csv: Path to save the resulting CSV file.
    - properties_list: List of properties to calculate using regionprops_table.
    """
    if not os.path.isdir(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        return

    all_dataframes = []  # List to store individual DataFrames

    # Recursively walk through input folder and process .npy files
    for root, _, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".npy"):
                file_path = os.path.join(root, file)

                try:
                    # Load the binary mask
                    binary_mask = np.load(file_path)

                    # Label connected regions in the binary mask
                    label_image = label(binary_mask)

                    # Measure properties
                    props = regionprops_table(label_image, properties=properties_list)

                    # Create a DataFrame for the current file
                    df = pd.DataFrame(props)
                    df['filename'] = file  # Add filename column
                    all_dataframes.append(df)

                    print(f"Processed: {file_path}")

                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    # Combine all DataFrames into one
    if all_dataframes:
        final_df = pd.concat(all_dataframes, ignore_index=True)

        # Save the final DataFrame as a CSV file
        final_df.to_csv(output_csv, index=False)
        print(f"Processing completed. Results saved in '{output_csv}'.")
    else:
        print("No valid .npy files found in the input folder.")

# Example usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print("Usage: python process_npy_files.py <input_folder> <output_csv> <properties_list>")
        print("Example properties_list: area,perimeter,mean_intensity")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_csv = sys.argv[2]

    process_npy_files(input_folder, output_csv, properties_list)
