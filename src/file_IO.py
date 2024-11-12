# tiff_io.py

import os
import re
import pandas as pd
import tifffile as tiff


def read_all_tiff_files_to_dataframe(directory_path):
    """
    Read all tiff files in the directory and subdirectories and store their paths and extracted information in a DataFrame.
    
    Parameters:
    - directory_path (str): Path to the directory containing tiff files.
    
    Returns:
    - A pandas DataFrame containing file paths, relative paths, file names, group IDs, and extracted information.
    """
    # Create a regex pattern to match the file name structure
    file_pattern = re.compile(r'r(\d{2})c(\d{2})f(\d{2})p(\d{2})-ch(\d{1})sk(\d{1,3})fk(\d{1})fl(\d{1})\.tiff')
    
    # List to store file information
    file_info_list = []
    
    # Dictionary to keep track of group IDs for each unique combination
    group_id_dict = {}
    group_counter = 1
    
    # Iterate through the directory to find all matching .tiff files
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            match = file_pattern.match(file)
            if file.endswith(".tiff") and match:
                # Extract the relevant parts from the filename
                row = int(match.group(1))
                column = int(match.group(2))
                field = int(match.group(3))
                unknown = int(match.group(4)) # should always be 1
                channel = int(match.group(5))
                frame = int(match.group(6)) # time point
                fk = int(match.group(7)) # should always be 1
                fl = int(match.group(8)) # should always be 1
                
                # Full path of the tiff file
                file_path = os.path.join(root, file)

                # Compute the relative path of the directory containing the file
                relative_dir_path = os.path.relpath(root, directory_path)
                
                # Create a unique key for the combination (excluding frame)
                unique_key = (relative_dir_path, row, column, field, channel)
                
                # Assign a group ID based on the unique combination
                if unique_key not in group_id_dict:
                    group_id_dict[unique_key] = f"{group_counter:02}"
                    group_counter += 1
                group_id = group_id_dict[unique_key]
                
                # Store the file information in a dictionary
                file_info = {
                    'file_path': file_path,
                    'relative_path': relative_dir_path,
                    'file_name': file,
                    'group': group_id,
                    'row': row,
                    'column': column,
                    'field': field,
                    'unknown': unknown,
                    'channel': channel,
                    'frame': frame,
                    'fk': fk,
                    'fl': fl
                }
                # Append the dictionary to the list
                file_info_list.append(file_info)
    
    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(file_info_list)
    
    return df



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

