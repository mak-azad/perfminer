#!/bin/bash

# File containing the list of hosts
hosts_file="t.txt"
# The script generating the log
script_to_kill="miner_github/analyzer/repo_analyzer.py"
# The log directory on the remote hosts
log_dir="~/miner_github/analyzer/logs/"
# Time threshold in minutes
time_threshold=25

# Function to check logs on a single host
check_logs() {
    local host=$1

    # Get the latest log entry
    latest_log=$(ssh $host "cd $log_dir && tail -n 1 \$(ls -t | head -1)")
    
    # Extract the timestamp from the log entry
    log_time=$(echo $latest_log | awk '{print $1 " " $2}' | sed 's/,/./')
    
    # Get the current time on the remote host
    current_time=$(ssh $host "date +'%Y-%m-%d %H:%M:%S'")

    # Convert times to epoch seconds for comparison
    log_time_epoch=$(ssh $host "date -d '$log_time' +%s")
    current_time_epoch=$(ssh $host "date -d '$current_time' +%s")

    # Calculate the time difference in minutes
    time_diff=$(( (current_time_epoch - log_time_epoch) / 60 ))

    echo "Host: $host"
    echo "Current time: $current_time"
    echo "Log time: $log_time"
    echo "Time difference: $time_diff minutes"

    # If the time difference exceeds the threshold, kill the script
    if [ $time_diff -gt $time_threshold ]; then
        echo "Time difference exceeds threshold. Killing the script on $host."
        ssh $host "kill -9 \$(pgrep -f '$script_to_kill')"
    else
        echo "Time difference is within the threshold."
    fi
}

# Periodically check the logs
while true; do
    while read -r host; do
        check_logs $host
    done < $hosts_file

    # Wait for a specified interval before checking again (e.g., 5 minutes)
    sleep 30
done