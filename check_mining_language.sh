#!/bin/bash
# Script to check current mining language configuration across all nodes

set -euo pipefail

echo "Checking mining language configuration across cluster..."
echo "=================================================="

if [[ -f "sshhosts" ]]; then
    echo "Config file contents on each node:"
    parallel-ssh -h sshhosts -i -t 10 "hostname && echo 'Config:' && cat \$HOME/perfminer/cronjob/miner.conf 2>/dev/null || echo 'No config file found'"
    
    echo ""
    echo "Environment variable (if set):"
    parallel-ssh -h sshhosts -i -t 10 "hostname && echo 'PERFMINER_LANGUAGE=' \$PERFMINER_LANGUAGE"
    
    echo ""
    echo "Effective language (what the script will use):"
    parallel-ssh -h sshhosts -i -t 10 "hostname && cd perfminer/cronjob && source miner.conf 2>/dev/null; echo 'Language:' \${PERFMINER_LANGUAGE:-\${LANGUAGE:-cpp}}"
else
    echo "Warning: sshhosts file not found. Checking local configuration only..."
    echo "Local config:"
    cat cronjob/miner.conf 2>/dev/null || echo "No local config file found"
    echo "Environment: PERFMINER_LANGUAGE=${PERFMINER_LANGUAGE:-not set}"
fi