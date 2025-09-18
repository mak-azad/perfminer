#!/bin/bash

# Define the remote directory where the archive files are stored
remote_directory="/users/akazad/"
local_directory="/home/akazad/dataset_cpp_new_pcminer"

# Create local directory if it doesn't exist
mkdir -p "$local_directory"

# Read the IP addresses and hostnames from the sshhosts_hostname file and copy the archive files
while read -r node_ip node_hostname; do
    echo "Copying from $node_ip ($node_hostname)..."
    
    # Convert hostname to lowercase
    node_hostname_lower=$(echo "$node_hostname" | tr '[:upper:]' '[:lower:]')

    # Use the lowercase hostname in the file name pattern for the tar.gz archives
    remote_file="${remote_directory}results_${node_hostname_lower}.tar.gz"

    # Print the exact command being executed for debugging
    echo "Running: scp akazad@${node_ip}:${remote_file} ${local_directory}"
    
    # Attempt to copy the file from the remote node
    scp akazad@"$node_ip":"$remote_file" "$local_directory"
    
    if [ $? -eq 0 ]; then
        echo "Successfully copied $(basename "$remote_file") from $node_ip ($node_hostname)"
    else
        echo "Failed to copy $(basename "$remote_file") from $node_ip ($node_hostname)" >&2
    fi
done < sshhosts_hostname