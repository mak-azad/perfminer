#!/bin/bash

# Path to the public key
PUB_KEY="$HOME/.ssh/id_rsa.pub"

# Path to the sshhosts file
HOSTS_FILE="sshhosts"

# Check if the public key file exists
if [[ ! -f "$PUB_KEY" ]]; then
  echo "Public key file not found: $PUB_KEY"
  exit 1
fi

# Check if the sshhosts file exists
if [[ ! -f "$HOSTS_FILE" ]]; then
  echo "Hosts file not found: $HOSTS_FILE"
  exit 1
fi

# Read the sshhosts file and copy the public key to each host
while IFS= read -r host; do
  echo "Copying key to $host"
  cat "$PUB_KEY" | ssh "$host" 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'
done < "$HOSTS_FILE"

echo "Public key copied to all hosts."
