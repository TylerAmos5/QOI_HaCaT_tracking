# tiff_io.py

import os
import re
import tifffile as tiff

# Function to read all tiff files in a directory and store them by frame number
def read_all_tiff_files(directory_path, channel_number=2):
    """
    Read all tiff files in the directory corresponding to the specified channel and store them by frame number (sk value).
    
    Parameters:
    - directory_path (str): Path to the directory containing tiff files.
    - channel_number (int): Channel number to filter for, defaults to 2.
    
    Returns:
    - A dictionary mapping frame numbers (sk values) to the corresponding image data.
    """
    # Create a regex pattern to match the file name structure and the specified channel
    file_pattern = re.compile(r'r\d{2}c\d{2}f\d{2}p\d{2}-ch' + str(channel_number) + r'sk(\d{1,3})fk\d{1}fl\d{1}\.tiff')
    
    # Dictionary to store images by their frame number (sk value)
    tiff_images = {}
    
    # Iterate through the directory to find all matching .tiff files
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            match = file_pattern.match(file)
            if file.endswith(".tiff") and match:
                # Extract the frame number from the filename (sk tag)
                frame_number = int(match.group(1))
                # Full path of the tiff file
                file_path = os.path.join(root, file)
                # Read the tiff file
                image_data = tiff.imread(file_path)
                # Store the image data in the dictionary, keyed by frame number
                tiff_images[frame_number] = image_data
    
    return tiff_images

# Function to retrieve a specific frame from pre-loaded images
def get_image_by_frame(tiff_images, target_frame):
    """
    Retrieve a specific frame (sk value) from pre-loaded images.
    
    Parameters:
    - tiff_images (dict): Dictionary of pre-loaded images, keyed by frame number.
    - target_frame (int): The frame number (sk value) you want to access.
    
    Returns:
    - The image data for the requested frame, or None if not found.
    """
    return tiff_images.get(target_frame, None)