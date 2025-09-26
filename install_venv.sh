#!/bin/bash
set -euo pipefail
VENV="$HOME/venvs/mytoolenv"
REQ="$HOME/perfminer/requirements.txt"
PYBIN="$(command -v python3 || true)"
[ -n "$PYBIN" ] || { echo "python3 not found"; exit 1; }

mkdir -p "$(dirname "$VENV")"

ensure_user_pip() {
  if ! "$PYBIN" -m pip -V >/dev/null 2>&1; then
    echo "[bootstrap] pip missing; trying ensurepip..."
    if ! "$PYBIN" -m ensurepip --upgrade >/dev/null 2>&1; then
      echo "[bootstrap] ensurepip unavailable; downloading get-pip.py"
      curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
      "$PYBIN" /tmp/get-pip.py --user
    fi
  fi
  "$PYBIN" -m pip -V >/dev/null
}

create_with_virtualenv() {
  echo "[venv] creating with virtualenv"
  "$PYBIN" -m pip install --user --upgrade virtualenv >/dev/null
  "$PYBIN" -m virtualenv "$VENV"
}

# Clean incomplete venvs
[ -x "$VENV/bin/python" ] || rm -rf "$VENV"

ensure_user_pip
create_with_virtualenv

# Upgrade basics inside venv
"$VENV/bin/python" -m pip install --upgrade pip setuptools wheel

# Install deps
[ -f "$REQ" ] || { echo "requirements.txt not found at $REQ"; exit 1; }
"$VENV/bin/pip" install -r "$REQ"

# Smoke test
"$VENV/bin/python" - <<'PY'
import sys, codecs
print("Python:", sys.version.split()[0], "UTF-8:", codecs.lookup("utf-8").name)
import pip
print("pip:", pip.__version__)
PY

echo "[venv] ready at $VENV"
