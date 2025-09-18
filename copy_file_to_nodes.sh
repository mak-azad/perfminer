#!/bin/bash

# Define the file you want to copy
file_to_copy="/home/akazad/perf_miner/test/test_model.py"
remote_directory="/users/akazad/"

# Read the IP addresses from the sshhosts file and copy the file to each node
while read -r node_ip; do
    echo "Copying to $node_ip..."
    scp "$file_to_copy" akazad@"$node_ip":"$remote_directory"
    if [ $? -eq 0 ]; then
        echo "Successfully copied to $node_ip"
    else
        echo "Failed to copy to $node_ip" >&2
    fi
done < sshhosts