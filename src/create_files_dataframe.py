import os
import file_IO



# Example usage
directory_path = '/Volumes/almc-cell-migration'

# Read all tiff files into a DataFrame
tiff_files_df = file_IO.read_all_tiff_files_to_dataframe(directory_path)

# Display the DataFrame
print(tiff_files_df)
print(tiff_files_df.info())
print(tiff_files_df.head())

output_path = '/Users/sestockman/Library/CloudStorage/OneDrive-UCB-O365/QOI_2024_HaCaT_Sheets/Data'

# Write the DataFrame to a CSV file
output_csv_path = os.path.join(output_path, 'tiff_files_info.csv')
tiff_files_df.to_csv(output_csv_path, index=False)

print(f"DataFrame written to CSV at: {output_csv_path}")

# Find the number of rows per group
group_counts = tiff_files_df.groupby('group').size().reset_index(name='counts')

# Display the group counts
print(group_counts)