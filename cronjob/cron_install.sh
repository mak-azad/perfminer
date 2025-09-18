#!/usr/bin/env bash
set -euo pipefail

# Project base and scripts
BASE="/users/akazad/perf_miner"
RUNNER="$BASE/cronjob/run_miner.sh"
LOGDIR="$BASE/cronjob"
LOCKFILE="$BASE/cronjob/run.lock"

# Ensure log dir exists
mkdir -p "$LOGDIR"

# Cron entry: every 5 min, prevent overlaps with flock, write to absolute log path
CRON_JOB="*/5 * * * * /usr/bin/flock -n $LOCKFILE /bin/bash $RUNNER >> $LOGDIR/cron.log 2>&1"

# Install/update idempotently
( crontab -l 2>/dev/null | grep -Fv "$RUNNER" ; echo "$CRON_JOB" ) | crontab -

echo "Installed cron for $RUNNER; logs at $LOGDIR/cron.log"
