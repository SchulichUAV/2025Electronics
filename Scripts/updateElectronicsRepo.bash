#!/bin/bash

# Check if arguments are provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <Flight Computer Hostname>"
    exit 1
fi

# Flight computer hostname
FLIGHT_COMPUTER_USERNAME_AND_HOSTNAME="$1"  

echo "$(dirname "${BASH_SOURCE[0]}")"

echo "Flight Computer Hostname: $FLIGHT_COMPUTER_USERNAME_AND_HOSTNAME"

cd ../.. 

scp -r 2025Electronics $FLIGHT_COMPUTER_USERNAME_AND_HOSTNAME:~/SUAV

# If else block to determine success or failure of SCP transfer
if [$? -eq 0]; then 
    echo "Success: Files copied successfully."

else 
    echo "Error: File transfer failed."
fi
