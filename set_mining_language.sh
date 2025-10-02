#!/bin/bash
# Script to set mining language across all cluster nodes

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "Usage: $0 <language>"
    echo "Example: $0 python"
    echo "Example: $0 cpp"
    echo "Example: $0 java"
    exit 1
fi

LANGUAGE="$1"
CONFIG_FILE="perfminer/cronjob/miner.conf"

echo "Setting mining language to: $LANGUAGE"

# Method 1: Update config file on all nodes
if [[ -f "sshhosts" ]]; then
    echo "Updating config file on all nodes..."
    parallel-ssh -h sshhosts -i "echo 'LANGUAGE=$LANGUAGE' > \$HOME/$CONFIG_FILE"
    
    # Verify the update
    echo "Verifying configuration on all nodes..."
    parallel-ssh -h sshhosts -i "cat \$HOME/$CONFIG_FILE"
else
    echo "Warning: sshhosts file not found. Make sure you're in the perfminer directory."
    echo "Updating local config file only..."
    echo "LANGUAGE=$LANGUAGE" > cronjob/miner.conf
fi

echo "Language configuration updated successfully!"
echo ""
echo "Alternative: You can also set the environment variable on all nodes:"
echo "parallel-ssh -h sshhosts -i 'echo \"export PERFMINER_LANGUAGE=$LANGUAGE\" >> ~/.bashrc'"