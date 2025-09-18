#!/bin/bash
set -eux

# Install NFS server
sudo apt-get update -y
sudo apt-get install -y nfs-kernel-server

# Make sure /nfs exists (it’s already mounted to /dev/sdd, but safe to mkdir)
sudo mkdir -p /nfs

# Add export rule (allow all clients in the experiment)
echo "/nfs *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee /etc/exports

# Apply exports
sudo exportfs -ra

# Enable and start NFS service
sudo systemctl enable nfs-server
sudo systemctl restart nfs-server
