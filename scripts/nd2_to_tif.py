from nd2 import ND2File
import tifffile
import os
import sys

if len(sys.argv) != 3:
    print("Usage: python nd2_to_tif.py <input_folder> <output_folder>")
    sys.exit(1)

input_folder = sys.argv[1]
output_folder = sys.argv[2]

# Validate input folder
if not os.path.isdir(input_folder):
    print(f"Error: Input folder '{input_folder}' does not exist.")
    sys.exit(1)

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process all .nd2 files recursively
for root, _, files in os.walk(input_folder):
    for file in files:
        if file.endswith(".nd2"):
            # Construct full input path
            input_path = os.path.join(root, file)

            # Create corresponding output subfolder structure
            relative_path = os.path.relpath(root, input_folder)
            output_subfolder = os.path.join(output_folder, relative_path)
            os.makedirs(output_subfolder, exist_ok=True)

            # Construct output file path
            output_path = os.path.join(output_subfolder, file.replace(".nd2", ".tif"))

            try:
                # Open the .nd2 file
                with ND2File(input_path) as nd2_file:
                    # Extract image data as a NumPy array
                    data = nd2_file.asarray()

                    # Save the image data as .tif
                    tifffile.imwrite(output_path, data, photometric="minisblack")
                    print(f"Converted: {input_path} -> {output_path}")
            except Exception as e:
                print(f"Error converting {input_path}: {e}")

print(f"Conversion completed. TIF files are saved in '{output_folder}'.")


