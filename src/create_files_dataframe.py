import os
import file_IO
import matplotlib.pyplot as plt


# Example usage
directory_path = '/Volumes/almc-cell-migration'

# Read all tiff files into a DataFrame
tiff_files_df = file_IO.read_all_tiff_files_to_dataframe(directory_path)

# Display the DataFrame
# print(tiff_files_df)
# print(tiff_files_df.info())
# print(tiff_files_df.head())

output_path = '/Users/sestockman/Library/CloudStorage/OneDrive-UCB-O365/QOI_2024_HaCaT_Sheets/Data'

# Write the DataFrame to a CSV file
output_csv_path = os.path.join(output_path, 'tiff_files_info.csv')
tiff_files_df.to_csv(output_csv_path, index=False)

print(f"DataFrame written to CSV at: {output_csv_path}")

# Find the number of rows per group
group_counts = tiff_files_df.groupby('group').size().reset_index(name='counts')
# Sort group counts by highest count
group_counts = group_counts.sort_values(by='counts', ascending=False)
# Display the group counts
print(group_counts.head(20))



# Create a histogram of the counts
plt.figure(figsize=(10, 6))
plt.hist(group_counts['counts'], bins=50, edgecolor='black')
plt.title('Histogram of Group Counts')
plt.xlabel('Counts')
plt.ylabel('Frequency')
plt.ylim(0, 10)  # Set y-axis limit
plt.grid(True)
plt.show()


# Filter groups with counts > 80
high_count_groups = group_counts[group_counts['counts'] > 80]['group']

# Filter rows in tiff_files_df that match these groups
filtered_tiff_files_df = tiff_files_df[tiff_files_df['group'].isin(high_count_groups)]

# Display the filtered DataFrame
print(filtered_tiff_files_df)

# Optionally, write the filtered DataFrame to a CSV file
filtered_csv_path = os.path.join(output_path, 'filtered_tiff_files_info.csv')
filtered_tiff_files_df.to_csv(filtered_csv_path, index=False)

print(f"Filtered DataFrame written to CSV at: {filtered_csv_path}")