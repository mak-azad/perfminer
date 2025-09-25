"""
Updated log monitoring and process management script for the latest miner implementation.

This script periodically connects to each remote host listed in the `sshhosts` file, inspects
the most recently updated log in the miner's log directory and determines whether the miner
has stalled. If the last log entry is older than a configurable time threshold, the script
updates a corresponding state file to mark a repository as processed and terminates the
running miner process. The new implementation derives all relevant paths relative to the
configured root directory and supports different state file formats.

Changes from the previous version:
  - Uses `os.path.join` and `os.path.expanduser` to construct absolute paths rather than
    relying on hard‑coded string concatenation. This makes it easier to relocate the miner
    repository without editing the script.
  - Reads the log directory relative to the miner root directory; you can customise
    `ROOT_DIR` and `SCRIPT_NAME` at the top of the file.
  - When updating the CSV state file, the script calls a Python helper script in the same
    repository (`update_state.py`) rather than referencing a specific absolute path.
  - Minor cleanup of imports and error handling.
"""

import os
import time
import socket
import paramiko
from datetime import datetime

###############################################################################
# Configuration
#
# Adjust these values to match your miner repository layout. `ROOT_DIR` should
# point to the root directory of your miner repository on the remote host.
# `SCRIPT_NAME` is the relative path to the running miner script that you want
# to monitor and kill when it stalls. `LOG_SUBDIR` is the relative path from
# `ROOT_DIR` to the directory where your miner writes its log files. All
# path variables are joined with `os.path.join` to build correct absolute
# paths on the remote host.
###############################################################################

ROOT_DIR = os.path.expanduser("~/perfminer")
SCRIPT_NAME = os.path.join("analyzer", "repo_analyzer.py")  # update as needed
LOG_SUBDIR = os.path.join("analyzer", "logs")

# The time threshold (in minutes) after which a miner process is considered
# stalled and should be killed.
TIME_THRESHOLD_MINUTES = 25

# The file containing hostnames and IP addresses of remote nodes. Each line
# should consist of a hostname and its IP address separated by whitespace.
HOSTS_FILE = "sshhosts_hostname"

###############################################################################
# Helper functions
###############################################################################

def get_ssh_client(host: str) -> paramiko.SSHClient:
    """Create and return an SSH client connected to the given host."""
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host)
    return client


def get_latest_log_entry(client: paramiko.SSHClient) -> str:
    """Return the last line of the most recently updated log file on the remote host."""
    remote_log_dir = os.path.join(ROOT_DIR, LOG_SUBDIR)
    # Build a shell command that finds the newest file in the log directory and
    # extracts its last line. Using `tail -n 1` ensures we only fetch one line.
    cmd = (
        f"cd {remote_log_dir} && "
        f"latest=$(ls -t 2>/dev/null | head -n 1) && "
        f"[ -n \"$latest\" ] && tail -n 1 \"$latest\" || echo ''"
    )
    stdin, stdout, stderr = client.exec_command(cmd)
    latest_log = stdout.read().decode().strip()
    return latest_log


def get_current_time(client: paramiko.SSHClient) -> datetime:
    """Return the current time on the remote host as a `datetime` object."""
    stdin, stdout, _ = client.exec_command("date +'%Y-%m-%d %H:%M:%S'")
    current_time_str = stdout.read().decode().strip()
    return datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S")


def kill_miner_process(client: paramiko.SSHClient) -> None:
    """Kill the running miner process on the remote host."""
    script_path = os.path.join(ROOT_DIR, SCRIPT_NAME)
    # `pgrep -f` matches the entire command line; quoting ensures special
    # characters (like spaces) in the script path are handled correctly.
    find_cmd = f"pgrep -f '{script_path}'"
    stdin, stdout, _ = client.exec_command(find_cmd)
    pids = stdout.read().decode().strip().split()
    for pid in pids:
        print(f"Killing process {pid} on remote host")
        client.exec_command(f"kill -9 {pid}")
    if not pids:
        print(f"No process found for {script_path}")


def update_state_csv(client: paramiko.SSHClient) -> None:
    """
    Invoke the `update_state.py` script inside the miner repository on the remote host.

    This helper assumes that `update_state.py` resides in the root of the miner
    repository (`ROOT_DIR`) and that your Python environment is correctly set
    up to run it. Modify the `python_cmd` variable if you need to activate a
    virtual environment or use a specific interpreter.
    """
    script_path = os.path.join(ROOT_DIR, "update_state.py")
    # If you need to activate an environment, adjust the command below.
    python_cmd = f"python {script_path}"
    client.exec_command(python_cmd)


def check_logs_for_host(host: str) -> None:
    """Check the log on a single remote host and take action if stalled."""
    try:
        client = get_ssh_client(host)
        print(f"Checking logs for host: {host}")

        latest_log_line = get_latest_log_entry(client)
        if not latest_log_line:
            print(f"No log entry found for host: {host}")
            client.close()
            return

        # Extract timestamp from the log line. Assumes the timestamp is the first
        # two whitespace‑separated fields of the log line. Replace this parsing
        # logic if your log format differs.
        parts = latest_log_line.replace(",", ".").split()
        log_time_str = " ".join(parts[:2])
        log_time = datetime.strptime(log_time_str, "%Y-%m-%d %H:%M:%S.%f")

        current_time = get_current_time(client)
        time_diff_minutes = (current_time - log_time).total_seconds() / 60.0
        print(f"Latest log time: {log_time}, current time: {current_time}, "
              f"difference: {time_diff_minutes:.2f} minutes")

        if time_diff_minutes > TIME_THRESHOLD_MINUTES:
            print(f"Time difference exceeds threshold ({TIME_THRESHOLD_MINUTES} min). "
                  f"Updating state and killing miner on {host}.")
            update_state_csv(client)
            kill_miner_process(client)
        else:
            print(f"Miner on {host} is within the threshold.")

        client.close()
    except Exception as exc:
        print(f"Error checking logs on host {host}: {exc}")


def main() -> None:
    try:
        # Read hosts file and filter out empty lines
        with open(HOSTS_FILE, 'r') as file:
            hosts = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Error: The hosts file '{HOSTS_FILE}' is missing.")
        return

    if not hosts:
        print("Error: The hosts file is empty.")
        return

    print("Hosts file content:")
    print("\n".join(hosts))

    # Loop forever with a delay between iterations
    while True:
        for host in hosts:
            check_logs_for_host(host)
        # Wait before checking again; adjust sleep duration as needed
        time.sleep(300)  # 5 minutes


if __name__ == "__main__":
    main()