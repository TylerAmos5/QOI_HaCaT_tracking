#!/bin/bash

# Define your paths
NPY_FOLDER="/Users/sestockman/Library/CloudStorage/OneDrive-UCB-O365/QOI_2024_HaCaT_Sheets/Data/LIU_IMAGES (with corrected)/nuclei"
OUTPUT_FOLDER="/Users/sestockman/Library/CloudStorage/OneDrive-UCB-O365/QOI_2024_HaCaT_Sheets/Data/LIU_IMAGES (with corrected)/output"

# Create the output folder if it doesn't exist
mkdir -p "$OUTPUT_FOLDER"

# Process each .npy file in the NPY_FOLDER
for file_path in "$NPY_FOLDER"/*.npy; do
    file_name=$(basename "$file_path")
    output_name="${file_name%.npy}"
    
    # Run cellpose with the --save_png flag
    cellpose --dir "$NPY_FOLDER" --pretrained_model nuclei --chan 0 --diameter 17 --save_png --savedir "$OUTPUT_FOLDER" --file "$file_path" --verbose
done