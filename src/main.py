# main.py

import file_IO
from cellpose import models
import numpy as np
import matplotlib.pyplot as plt

# Specify the directory where the tiff files are stored
directory_path = 'path_to_directory'

# Define the channel number (nuclear channel)
channel_number = 2

# Read all tiff files into memory and store them by frame number
tiff_images = file_IO.read_all_tiff_files(directory_path, channel_number)

# Initialize the CellPose model for nuclear segmentation
model = models.Cellpose(model_type='nuclei')

# Find the first frame to segment (smallest frame number)
first_frame_number = min(tiff_images.keys())
first_image = tiff_images[first_frame_number]

# Ensure the image is in the correct format (convert to float32 if necessary)
if first_image.dtype != np.float32:
    first_image = first_image.astype(np.float32)

# Run the CellPose segmentation on the first frame
masks, flows, styles, diams = model.eval(first_image, channels=[0, 0])  # [0, 0] for grayscale

# Optionally: Display the result for the first frame
plt.figure(figsize=(8, 8))
plt.imshow(first_image, cmap='gray')
plt.imshow(masks, alpha=0.5)
plt.title(f'Segmented frame {first_frame_number}')
plt.show()

# Now you have segmented the first frame and visualized it