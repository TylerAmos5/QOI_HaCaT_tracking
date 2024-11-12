from cellpose import io
import numpy as np
import os

# Define your paths
npy_folder = '/Users/sestockman/Library/CloudStorage/OneDrive-UCB-O365/QOI_2024_HaCaT_Sheets/Data/LIU_IMAGES (with corrected)/nuclei'
png_folder = '/Users/sestockman/Library/CloudStorage/OneDrive-UCB-O365/QOI_2024_HaCaT_Sheets/Data/LIU_IMAGES (with corrected)/png'
os.makedirs(png_folder, exist_ok=True)  # Create the output folder if it doesn't exist

# Load and save each .npy label file
for file_name in os.listdir(npy_folder):
    if file_name.endswith('.npy'):
        label_path = os.path.join(npy_folder, file_name)
        label_dict = np.load(label_path, allow_pickle=True).item()  # Load the dictionary
        
        # Extract the mask data from the dictionary
        masks = label_dict.get('masks')
        
        if masks is not None:
            # Define the image name without .npy extension for saving as PNG
            image_name = os.path.splitext(file_name)[0]
            
            # Save the mask as a PNG
            io.save_masks(None, masks, None, [os.path.join(png_folder, image_name)], png=True)
        else:
            print(f"No 'masks' key found in {file_name}")