#!/usr/bin/env bash
set -euo pipefail

BASE="/users/akazad/perfminer"
RUNNER="$BASE/cronjob/run_miner.sh"
LOGDIR="$BASE/cronjob"
LOCKFILE="$BASE/cronjob/run.lock"

if [[ ! -x "$RUNNER" ]]; then
  echo "ERROR: $RUNNER not found or not executable on $(hostname)" >&2
  exit 1
fi

mkdir -p "$LOGDIR"

# Option A (original): just run the runner
CRON_JOB="*/5 * * * * /usr/bin/flock -n $LOCKFILE /bin/bash $RUNNER >> $LOGDIR/cron.log 2>&1"

# Option B (recommended): add a heartbeat so cron.log always updates
# CRON_JOB="*/5 * * * * echo \"tick \$(date -Is) \$(hostname -s)\" >> $LOGDIR/cron.log; /usr/bin/flock -n $LOCKFILE /bin/bash $RUNNER >> $LOGDIR/cron.log 2>&1"

( crontab -l 2>/dev/null | grep -Fv "$RUNNER" || true; echo "$CRON_JOB" ) | crontab -

echo "Installed cron for $RUNNER; logs at $LOGDIR/cron.log"
