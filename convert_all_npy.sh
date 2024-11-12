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
    cellpose --dir "$NPY_FOLDER" --save_png --savedir "$OUTPUT_FOLDER" --pretrained_model cyto --diameter 30 --flow_threshold 0.4 --cellprob_threshold 0.0 --use_gpu --file "$file_path"
done