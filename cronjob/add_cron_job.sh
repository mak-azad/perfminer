#!/bin/bash

# Job to add
CRON_JOB="*/5 * * * * /bin/bash /users/akazad/perf_miner/cronjob/run_miner.sh > cron.log 2>&1"

# Check if the cron job already exists
crontab -l > current_crontab
if ! grep -Fxq "$CRON_JOB" current_crontab; then
  # Add the cron job if it doesn't exist
  (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
fi
