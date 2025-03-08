#!/bin/bash

# Check if both arguments are provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <Flight Computer Hostname>"
    exit 1
fi

# Flight computer hostname
FLIGHT_COMPUTER_USERNAME_AND_HOSTNAME="$1"  
# Get the script's directory (absolute path)
LOCAL_ELECTRONICS_2025_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Using Local Directory: $LOCAL_ELECTRONICS_2025_DIR"
echo "Flight Computer Hostname: $FLIGHT_COMPUTER_USERNAME_AND_HOSTNAME"

cd "$LOCAL_ELECTRONICS_2025_DIR" || { echo "Failed to access $LOCAL_ELECTRONICS_2025_DIR"; exit 1; }

scp -r $LOCAL_ELECTRONICS_2025_DIR $FLIGHT_COMPUTER_USERNAME_AND_HOSTNAME:~/SUAV
