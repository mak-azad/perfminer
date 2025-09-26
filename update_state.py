"""
Updated helper script to mark a repository as processed in the state CSV for the
latest miner. This script determines the host's IP address and then updates
the first unprocessed repository entry in a `.state.csv` file within the
miner repository. It supports flexible CSV formats by looking for a status
column named one of `state`, `status`, `processed`, `complete` or `done`.

Changes from the previous version:
  - Dynamically derives the root directory based on the location of this file
    (`update_state.py`). This eliminates the need to hard‑code the miner
    directory.
  - Expects repository state files to use a `.state.csv` extension rather
    than `.csv`. For example, `github_repositories_<ip>.state.csv`.
  - Detects the appropriate status column by inspecting the header row and
    supports multiple synonymous column names. Falls back to the last column
    if no recognised header is found.
  - Includes improved error handling and avoids raising exceptions if the
    state file is missing.
"""

import csv
import os
import socket
import datetime
from typing import Optional
import requests

# Determine the directory containing this script and treat its parent as the
# miner root directory. This allows the script to be relocated along with the
# repository without changes.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(CURRENT_DIR)


def get_ip_from_sshosts(sshosts_path: str) -> Optional[str]:
    """Return the IP address for the current host from the given sshhosts file."""
    hostname = socket.gethostname()
    try:
        with open(sshosts_path, 'r') as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) >= 2:
                    line_hostname, ip_address = parts[0], parts[1]
                    if line_hostname == hostname:
                        return ip_address
    except Exception:
        return None
    return None


def update_first_false_to_true(file_path: str) -> None:
    """
    Update the repository state file when a miner job is prematurely terminated.

    This function reads the state CSV, identifies the row that was actively
    being processed when the miner was killed (indicated by ``status`` equal
    to ``in_progress`` and ``processed`` equal to ``False``), and marks it
    as processed and skipped. Specifically, it sets the ``processed`` value
    to ``True`` and updates the ``status`` to ``skipped``. If a ``finished_at``
    column is present in the header, it records the current timestamp in
    ISO format. Only the first matching row is updated; subsequent rows are
    left untouched.

    If no ``in_progress`` row exists, the function will not modify the file
    and will emit a warning. This conservative behaviour avoids skipping
    repositories unintentionally.
    """
    # Read all rows and header
    rows: list[list[str]] = []
    header: list[str] | None = None
    try:
        with open(file_path, 'r', newline='') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader, None)
            for row in csvreader:
                rows.append(row)
    except FileNotFoundError:
        print(f"State file '{file_path}' not found.")
        return

    if not header:
        print(f"State file '{file_path}' is missing a header row.")
        return

    # Determine indices for important columns
    col_names = [col.strip().lower() for col in header]
    processed_idx = None
    status_idx = None
    finished_idx = None
    for idx, col in enumerate(col_names):
        if col in {"processed", "complete", "done"}:
            processed_idx = idx
        elif col == "status":
            status_idx = idx
        elif col == "finished_at":
            finished_idx = idx

    if processed_idx is None or status_idx is None:
        print(
            f"Cannot update '{file_path}' because required columns 'processed' and 'status' were not found."
        )
        return

    # Identify and update the first in_progress row that is unprocessed
    updated = False
    for row in rows:
        # Ensure row has enough columns
        # Extend shorter rows with empty strings to avoid index errors
        if len(row) < len(header):
            row += [""] * (len(header) - len(row))
        proc_val = row[processed_idx].strip().lower()
        status_val = row[status_idx].strip().lower()
        if (not updated and proc_val in {"false", "0", "no"}) and status_val == "in_progress":
            # Mark as skipped and processed
            row[processed_idx] = "True"
            row[status_idx] = "skipped"
            if finished_idx is not None:
                # Record the timestamp of when it was skipped
                row[finished_idx] = datetime.datetime.now().isoformat()
            updated = True
            break

    if not updated:
        print(f"No in_progress entry found in '{file_path}'.")
        return

    # Write updated rows back to file
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"Marked in_progress repository as skipped in '{file_path}'.")


def get_public_ip(sshhosts_path: str = None) -> str:
    """
    Determine the public IP address of this host. If an sshhosts file is provided
    and contains a mapping for the current hostname, return that IP. Otherwise,
    query an external service as a fallback.
    """
    # First attempt: look up IP in sshhosts file if provided
    if sshhosts_path and os.path.exists(sshhosts_path):
        ip_from_file = get_ip_from_sshosts(sshhosts_path)
        if ip_from_file:
            return ip_from_file

    # Fallback: external API
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        pass
    return "Unknown"


def main() -> None:
    # Determine the host's IP address
    sshhosts_default = os.path.join(ROOT_DIR, 'sshhosts_hostname')
    host_ip = get_public_ip(sshhosts_default)
    # Construct path to the state CSV file. Use `.state.csv` suffix.
    today_str = datetime.date.today().strftime("%m%d%Y")  # unused but kept for possible extension
    state_file_name = f"github_repositories_{host_ip}.state.csv"
    state_file_path = os.path.join(ROOT_DIR, 'analyzer', state_file_name)
    update_first_false_to_true(state_file_path)


if __name__ == "__main__":
    main()
