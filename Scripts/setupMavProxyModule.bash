#!/bin/bash
set -x
set -v 

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <source_file>"
    exit 1
fi

MAVPROXY_MODULE="$1"
MAVPROXY_MODULES_DEST="$HOME/SUAV/env/lib/python3.12/site-packages/MAVProxy/modules"

if [ ! -f "$MAVPROXY_MODULE" ]; then
    echo "Error: Location for MAVPROXY_MODULE does not exist."
    exit 1
fi


FILENAME=$(basename "$MAVPROXY_MODULE")
DIRNAME=$(dirname "$MAVPROXY_MODULE")
if [[ ! "$FILENAME" =~ ^mavproxy_ ]]; then
    NEW_FILENAME="mavproxy_$FILENAME"
    mv "$MAVPROXY_MODULE" "$DIRNAME/$NEW_FILENAME"
    MAVPROXY_MODULE="$DIRNAME/$NEW_FILENAME"
    echo "Renamed mavproxy module to $NEW_FILENAME"
fi

echo "Copying $MAVPROXY_MODULE to $MAVPROXY_MODULES_DEST"
cp "$MAVPROXY_MODULE" "$MAVPROXY_MODULES_DEST"

if [ $? -eq 0 ]; then
    echo "Success: MAVProxy module setup correctly."
else
    echo "Error: MAVProxy module setup failed."
fi
