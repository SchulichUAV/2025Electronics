# Buit to sync with GCS2025 in Schulich UAV repository/organization
# Built for Raspberry Pi 5 (Linux OS)

from picamera2 import Picamera2, Preview
from flask import Flask, jsonify, request
from flask_cors import CORS
from math import ceil
import requests
import threading
import socket
import json
import sys
import time
from io import BytesIO
from os import path
import argparse
import RPi.GPIO as GPIO

GCS_URL = None
VEHICLE_PORT = None
ALTITUDE = 25
UDP_PORT = 5005

picam2 = None
vehicle_connection = None

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins" : "*"}}) # Overriding CORS for external access

# Dictionary to maintain vehicle state
vehicle_data = {
    "last_time": 0,
    "lat": 0,
    "lon": 0,
    "rel_alt": 0,
    "alt": 0,
    "roll": 0,
    "pitch": 0,
    "yaw": 0,
    "dlat": 0,
    "dlon": 0,
    "dalt": 0,
    "heading": 0
}

def receive_vehicle_position():  # Actively runs and receives live vehicle data on a separate thread
    '''
    This function is ran on a separate thread to actively retrieve and update the vehicle state. This vehicle state contains GPS and vehicle orientation.
    These are pulled at the time of taking an image in order to geotag images and support target localization.
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("127.0.0.1", UDP_PORT))
    while True:
        data = sock.recvfrom(1024)
        items = data[0].decode()[1:-1].split(",")
        message_time = float(items[0])

        if message_time <= vehicle_data["last_time"]:
            continue

        vehicle_data["last_time"] = message_time
        vehicle_data["lon"] = float(items[1])
        vehicle_data["lat"] = float(items[2])
        vehicle_data["rel_alt"] = float(items[3])
        vehicle_data["alt"] = float(items[4])
        vehicle_data["roll"] = float(items[5])
        vehicle_data["pitch"] = float(items[6])
        vehicle_data["yaw"] = float(items[7])
        vehicle_data["dlat"] = float(items[8])
        vehicle_data["dlon"] = float(items[9])
        vehicle_data["dalt"] = float(items[10])
        vehicle_data["heading"] = float(items[11])

if __name__ == "__main__":

    # Initialize vehicle port and GCS url global variables
    with open('ip.json', 'r') as ips:
        data = json.load(ips)
        VEHICLE_PORT = data["vehicle_port"]
        GCS_URL = data["gcs_url"]
    
    position_thread = threading.Thread(target=receive_vehicle_position, daemon=True)
    position_thread.start()
    time.sleep(1)

    # print(f"Attempting to connect to port: {VEHICLE_PORT}")
    # vehicle_connection = initialize.connect_to_vehicle(VEHICLE_PORT)
    # print("Vehicle connection established.")
    # retVal = initialize.verify_connection(vehicle_connection)
    # print("Vehicle connection verified.")

    # if not retVal:
    #     print("Error. Could not connect and/or verify a valid connection to the vehicle.")
    #     sys.exit(1)

    app.run(debug=True, host='0.0.0.0')
