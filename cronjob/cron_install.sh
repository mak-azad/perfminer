#!/usr/bin/env bash
set -euo pipefail

# Project base and scripts
BASE="/users/akazad/perfminer"
RUNNER="$BASE/cronjob/run_miner.sh"
LOGDIR="$BASE/cronjob"
LOCKFILE="$BASE/cronjob/run.lock"

if [[ ! -x "$RUNNER" ]]; then
  echo "ERROR: $RUNNER not found or not executable on $(hostname)" >&2
  exit 1
fi



# Ensure log dir exists
mkdir -p "$LOGDIR"

# Cron entry: every 5 min, prevent overlaps with flock, write to absolute log path
CRON_JOB="*/5 * * * * /usr/bin/flock -n $LOCKFILE /bin/bash $RUNNER >> $LOGDIR/cron.log 2>&1"

# Install/update idempotently, resilient to empty crontab and grep no-match
( crontab -l 2>/dev/null | grep -Fv "$RUNNER" || true; echo "$CRON_JOB" ) | crontab -

echo "Installed cron for $RUNNER; logs at $LOGDIR/cron.log"