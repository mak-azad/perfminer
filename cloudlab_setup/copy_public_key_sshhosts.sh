#!/bin/bash

# Path to the public key you want to distribute
PUBLIC_KEY_PATH="$HOME/.ssh/id_rsa.pub"

# Read each line from the nodes list
while IFS= read -r node
do
    echo "Copying key to akazad@$node"
    # Disable host key checking and append the public key to the authorized_keys on the remote node
    ssh -o StrictHostKeyChecking=no akazad@"$node" "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys" < "$PUBLIC_KEY_PATH"
done < "nodes_list.txt"

echo "Deployment completed."
