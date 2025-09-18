#!/bin/bash

# Directory containing your .jsonl files
input_directory="."

# Output file to combine all .jsonl files into
output_file="combined.jsonl"

# Log file to keep track of processed files
log_file="processed_files.log"

# Ensure the output file is empty before starting
> "$output_file"

# Ensure the log file is empty before starting
> "$log_file"

echo "Starting the combination process..."
# Initialize counter
processed_files_count=0
# Loop through each .jsonl file in the directory
for file in "$input_directory"/*.jsonl; do
    # Extract the absolute path of the file to avoid ambiguity
    absolute_file_path=$(realpath "$file")

    # Check if the file has already been processed
    if grep -Fxq "$absolute_file_path" "$log_file"; then
        echo "Skipping already processed file: $file"
        continue
    fi

    # Check if the file is not empty
    if [ -s "$file" ]; then
        # Append the content of the file to the output file
        echo "Adding file: $file"
        cat "$file" >> "$output_file"
        # Log the file as processed
        echo "$absolute_file_path" >> "$log_file"
         # Increment the processed files count
        ((processed_files_count++))
    else
        echo "Ignoring empty file: $file"
    fi
done

echo "Combination process completed.Processed files: $processed_files_count."
