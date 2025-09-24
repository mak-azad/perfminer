#!/usr/bin/env bash
set -euo pipefail

# ---- paths ----
BASE="/users/akazad/perfminer"
LOGDIR="$BASE/cronjob"
mkdir -p "$LOGDIR"

# Your analyzer entrypoint (absolute)
COMMAND="$BASE/analyzer/repo_analyzer.py"
LANGUAGE="cpp"

# ---- conda env activation (cron-safe) ----
if [ -f /users/akazad/miniforge3/etc/profile.d/conda.sh ]; then
  source /users/akazad/miniforge3/etc/profile.d/conda.sh
  conda activate mytoolenv
  PY="$(command -v python)"
else
  PY="/users/akazad/miniforge3/envs/mytoolenv/bin/python"
fi

# ---- PIDFILE guard ----
cd "$BASE"
PIDFILE="$LOGDIR/analyzer.pid"

if [[ -f "$PIDFILE" ]] && kill -0 "$(cat "$PIDFILE")" 2>/dev/null; then
  echo "$(date -Is) analyzer already running (pid $(cat "$PIDFILE"))" >> "$LOGDIR/run.log"
  exit 0
fi

ts="$(date +%Y%m%d_%H%M%S)"
echo "$(date -Is) starting $COMMAND with $PY" >> "$LOGDIR/run.log"

nohup "$PY" "$COMMAND" --language "$LANGUAGE" \
  >> "$LOGDIR/out_$ts.log" 2>> "$LOGDIR/err_$ts.log" &

echo $! > "$PIDFILE"
echo "$(date -Is) started pid $!; logs: $LOGDIR/out_$ts.log $LOGDIR/err_$ts.log" >> "$LOGDIR/run.log"
