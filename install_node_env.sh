#!/bin/bash
# Initialize Conda for script use

hostname=$(hostname)
echo "This script is running on host: $hostname"

source /users/akazad/miniforge3/etc/profile.d/conda.sh

# Create Conda environments
/users/akazad/miniforge3/bin/conda create -n mytoolenv python=3.10 -y

# Activate the environment
# Note: For script use, prefer this method over `conda activate`
source miniforge3/bin/activate mytoolenv

# Follow-up commands that require the Conda environment can go here
echo "Installing Python packages (pydriller, pygit2, pandas) on all hosts..."
sleep 5
pip3 install pydriller pygit2 pandas nltk
# echo "Installing OCI"
# pip3 install oci
#echo "Installing ML related libs..."
sleep 5
echo "Installing pytorch.."
pip install torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu121
echo "torch installation complete, checking .."
sleep 3
python3 -c "import torch; print(torch.__version__)"
sleep 5
python3 -c "import torch; print(torch.cuda.is_available())"
sleep 10
echo "Installing transformers.."
pip3 install transformers
pip3 install accelerate
echo "Now test the model at node: $hostname"
sleep 3
python3 perf_miner/test_model.py
echo "Script execution completed at node: $hostname"