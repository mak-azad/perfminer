#!/bin/bash

# Path to the file containing the list of VM hostnames or IPs
HOSTS_FILE="sshhosts"

# File to check for on the remote hosts
CHECK_FILE="/users/akazad/miner_github/analyzer/script_complete.txt"

# Time to wait between checks (in seconds), taken from the first command line argument
# If no argument is provided, default to 30 seconds
#SLEEP_DURATION=${1:-30} # Example: 300 seconds = 5 minutes
# Hard-coded sleep duration in seconds
SLEEP_DURATION=300  # 5 minutes
while : ; do
    echo "Checking for $CHECK_FILE on all hosts..."

    # Execute the check and potentially remove crontab if the file exists
    parallel-ssh -i -h "$HOSTS_FILE" -t 10 "if [ -f $CHECK_FILE ]; then crontab -r; echo '$HOST: File exists and crontab cleared'; else echo '$HOST: File not found'; fi"

    echo "Waiting for $SLEEP_DURATION seconds before re-checking..."
    sleep $SLEEP_DURATION
done
