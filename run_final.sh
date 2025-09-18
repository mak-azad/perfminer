#!/bin/bash
# Initialize Conda for script use

source /home/ubuntu/miniforge3/etc/profile.d/conda.sh

# Create Conda environments
/home/ubuntu/miniforge3/bin/conda create -n mytoolenv python=3.10 -y

# Activate the environment
# Note: For script use, prefer this method over `conda activate`
source miniforge3/bin/activate mytoolenv

echo "Testing mistral...."
sleep 5
python3 miner_github/test_mistral.py

#echo "Testing cloud storage.."
#python3 miner_github/test_oci_store2.py 
echo "Running the miner...."
sleep 5
python3 miner_github/analyzer/repo_analyzer.py

echo "Script execution completed at slave"