import pandas as pd

# Load the CSV file
file_path = 'filtered_repositories_python_undone.csv'  # Update with the actual file path
df = pd.read_csv(file_path)

# Split the dataframe into two equal parts
mid_index = len(df) // 2
df_part1 = df.iloc[:mid_index]
df_part2 = df.iloc[mid_index:]

# Define file paths for the two parts
part1_path = 'python_undone_part1.csv'
part2_path = 'python_undone_part2.csv'

# Save the two parts to separate CSV files
df_part1.to_csv(part1_path, index=False)
df_part2.to_csv(part2_path, index=False)

print(f"Part 1 saved to: {part1_path}")
print(f"Part 2 saved to: {part2_path}")