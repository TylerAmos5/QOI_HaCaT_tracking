import numpy as np
from PIL import Image
import os
from tifffile import imsave

data = np.load('/Users/sestockman/Desktop/Liu_images/nuclei/r02c09f07p01-ch2sk1fk1fl1_seg.npy', allow_pickle=True)
print(data)

#imsave('/Users/sestockman/Desktop/Liu_images/nuclei/segmentation_tiff_format/r02c09f07p01-ch2sk1fk1fl1_seg.tiff', data)

# # Function to process .npy files and convert them to .tiff
# def npy_to_tiff(input_folder, output_folder):
#     # Make sure the output folder exists
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)

#     # Loop through all files in the input folder
#     for filename in os.listdir(input_folder):
#         if filename.endswith(".npy"):
#             # Full path to the .npy file
#             npy_path = os.path.join(input_folder, filename)
            
#             # Load the NumPy array from the file with allow_pickle=True
#             data = np.load(npy_path, allow_pickle=True)
            
#             # Check the data type and convert if necessary
#             if data.dtype == np.object:
#                 # Assuming the object array contains numeric data, convert to a compatible type
#                 data = data.astype(np.float32)
            
#             # Convert the array to a PIL image
#             image = Image.fromarray(data)
            
#             # Create the corresponding .tiff filename
#             tiff_filename = filename.replace('.npy', '.tiff')
#             tiff_path = os.path.join(output_folder, tiff_filename)
            
#             # Save the image as a .tiff file
#             image.save(tiff_path)
#             print(f"Converted {filename} to {tiff_filename}")

# # Example usage:
# input_folder = '/Users/sestockman/Desktop/Liu_images/nuclei'  # Folder with .npy files
# output_folder = '/Users/sestockman/Desktop/Liu_images/nuclei/segmentation_tiff_format'  # Folder to save .tiff files

# npy_to_tiff(input_folder, output_folder)

