#!/usr/bin/env bash
set -euo pipefail

# ---- paths ----
BASE="/users/akazad/perf_miner"
LOGDIR="$BASE/cronjob"
mkdir -p "$LOGDIR"

# Your analyzer entrypoint (absolute)
COMMAND="$BASE/analyzer/repo_analyzer.py"

# ---- conda env activation (cron-safe) ----
# Load conda functions, then activate your env.
# shellcheck disable=SC1091
if [ -f /users/akazad/miniforge3/etc/profile.d/conda.sh ]; then
  source /users/akazad/miniforge3/etc/profile.d/conda.sh
  conda activate mytoolenv
  PY="$(command -v python)"
else
  # Fallback: use the env's python directly if conda.sh isn't available
  PY="/users/akazad/miniforge3/envs/mytoolenv/bin/python"
fi

# ---- run only if not already running ----
cd "$BASE"

if /usr/bin/pgrep -f -- "$COMMAND" >/dev/null; then
  echo "$(date -Is) $COMMAND already running" >> "$LOGDIR/run.log"
  exit 0
fi

ts="$(date +%Y%m%d_%H%M%S)"
echo "$(date -Is) starting $COMMAND with $PY" >> "$LOGDIR/run.log"
nohup "$PY" "$COMMAND" >> "$LOGDIR/out_$ts.log" 2>> "$LOGDIR/err_$ts.log" &
echo "$(date -Is) started pid $!; logs: $LOGDIR/out_$ts.log $LOGDIR/err_$ts.log" >> "$LOGDIR/run.log"
