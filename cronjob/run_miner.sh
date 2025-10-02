#!/usr/bin/env bash
set -euo pipefail

# Cron-safe locale
export LANG=C.UTF-8
export LC_ALL=C.UTF-8

BASE="/users/akazad/perfminer"
LOGDIR="$BASE/cronjob"
mkdir -p "$LOGDIR"

# Entry + args
COMMAND="$BASE/analyzer/repo_analyzer.py"

# Load language from config file if it exists, then environment variable, then default
if [[ -f "$BASE/cronjob/miner.conf" ]]; then
  source "$BASE/cronjob/miner.conf"
fi
LANGUAGE="${PERFMINER_LANGUAGE:-${LANGUAGE:-cpp}}"

# venv paths
VENV="$HOME/venvs/mytoolenv"
PY="$VENV/bin/python"
INSTALLER="$BASE/install_venv.sh"

# log a heartbeat to cron.log via cron_install’s redirection
echo "$(date -Is) run_miner invoked on $(hostname -s)"

# ensure venv exists (self-heal)
if [[ ! -x "$PY" ]]; then
  echo "$(date -Is) [run] venv missing; bootstrapping via $INSTALLER" >> "$LOGDIR/run.log"
  if [[ -x "$INSTALLER" ]]; then
    "$INSTALLER" >> "$LOGDIR/run.log" 2>&1 || {
      echo "$(date -Is) [run] venv bootstrap FAILED" >> "$LOGDIR/run.log"
      exit 1
    }
  else
    echo "$(date -Is) [run] installer not found: $INSTALLER" >> "$LOGDIR/run.log"
    exit 1
  fi
fi

# PID guard (and stale cleanup)
cd "$BASE"
PIDFILE="$LOGDIR/analyzer.pid"
if [[ -f "$PIDFILE" ]]; then
  PID="$(cat "$PIDFILE" 2>/dev/null || true)"
  if [[ -n "${PID:-}" ]] && kill -0 "$PID" 2>/dev/null; then
    echo "$(date -Is) analyzer already running (pid $PID)" >> "$LOGDIR/run.log"
    exit 0
  else
    rm -f "$PIDFILE"
  fi
fi

ts="$(date +%Y%m%d_%H%M%S)"
echo "$(date -Is) starting $COMMAND with $PY" >> "$LOGDIR/run.log"

# launch miner (per-run logs)
nohup "$PY" "$COMMAND" --language "$LANGUAGE" \
  >> "$LOGDIR/out_$ts.log" 2>> "$LOGDIR/err_$ts.log" &

echo $! > "$PIDFILE"
echo "$(date -Is) started pid $!; logs: $LOGDIR/out_$ts.log $LOGDIR/err_$ts.log" >> "$LOGDIR/run.log"
