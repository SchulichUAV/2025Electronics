# Buit to sync with GCS2025 in Schulich UAV repository/organization
# Built for Raspberry Pi 5 (Linux OS)

from picamera2 import Picamera2, Preview
from flask import Flask, jsonify, request, Response
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

import modules.AutopilotDevelopment.General.Operations.initialize as initialize
import modules.AutopilotDevelopment.General.Operations.mode as autopilot_mode
import modules.AutopilotDevelopment.Plane.Operations.system_state as system_state

GCS_URL = "http://192.168.1.64:80"
VEHICLE_PORT = "udp:127.0.0.1:5006"
DELAY = 0.25

picam2 = None
vehicle_connection = None
image_number = 0
is_camera_on = False
image_number = 0

app = Flask(__name__)
# Overriding CORS for external access
CORS(app, supports_credentials=True)

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
    "heading": 0,
    "num_satellites": 0,
    "position_uncertainty": 0,
    "alt_uncertainty": 0,
    "speed_uncertainty": 0,
    "heading_uncertainty": 0
}

@app.route('/set_flight_mode', methods=["POST"])
def set_flight_mode():
# Ardupilot docs (for flight modes): https://ardupilot.org/copter/docs/parameters.html
    data = request.get_json(force=True)
    try:
        mode_id = int(data['mode_id'])
        print(mode_id)
        print(autopilot_mode.set_mode(vehicle_connection, mode_id))
    except Exception as e:
        return jsonify({'error': "Invalid operation."}), 400

    return jsonify({'message': 'Mode set successfully'}), 200

@app.route("/toggle_camera", methods=["POST"])
def toggle_camera():
    global picam2
    global image_number
    global is_camera_on

    try:
        json_data = request.json
        is_camera_on = json_data["is_camera_on"]
        print("SUCCESS")
    except Exception as e:
        print("Could not interpret `is_camera_on` value from API request.")
        print(e)
    print("Parsed camera on")
    if picam2 is None:
        print("picam2 is None")
        picam2 = Picamera2()
        camera_config = picam2.create_still_configuration()
        picam2.configure(camera_config)
        picam2.start_preview(Preview.NULL)
        picam2.start()
        time.sleep(1)
    else:
        print("picam2 is not none! starting picam.")
        picam2.start()
    print("mapped picam2 properly")
    while is_camera_on:
        print("looping over camera on")
        image_number += 1
        delay_time_remaining = DELAY - take_picture(image_number, picam2)
        if delay_time_remaining > 0:
            time.sleep(delay_time_remaining)
    print("stopping picam")
    picam2.stop()
    return { "message": "Success!"}, 200

def take_picture(image_number, picam2):
    print(f"Beginning capturing capture{image_number}.jpg")
    start_time = time.time()

    # Capture image into a temporary BytesIO object
    image_stream = BytesIO()
    image = picam2.capture_image('main')
    image.save(image_stream, format='JPEG')
    image_stream.seek(0)

    # Serialize vehicle data into a JSON string
    vehicle_data_json = json.dumps(vehicle_data)

    # Send image to GCS
    headers = {} # API Request headers

    files = {
        'file': (f'capture{image_number}.jpg', image_stream, 'image/jpg'),
    }
    response = requests.request("POST", f"{GCS_URL}/submit", headers=headers, files=files)

    # Send JSON to GCS (note that these need to be sent in a separate API request due to body datatype)
    json_stream = BytesIO(vehicle_data_json.encode('utf-8'))
    json_files = {
        'file': (f'capture{image_number}.json', json_stream, 'application/json'),
    }
    response = requests.request("POST", f"{GCS_URL}/submit", headers=headers, files=json_files)

    return time.time() - start_time

@app.route("/heartbeat-validate")
def heartbeat_validate():
    # this is being updated by the thread
    return vehicle_data

def receive_vehicle_position():  # Actively runs and receives live vehicle data on a separate thread
    '''
    This function is ran on a second thread to actively retrieve and update the vehicle state. This vehicle state contains GPS and vehicle orientation.
    These are pulled at the time of taking an image in order to geotag images and support target localization.
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind(("127.0.0.1", 5005))
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
        vehicle_data["num_satellites"] = float(items[12])
        vehicle_data["position_uncertainty"] = float(items[13])
        vehicle_data["alt_uncertainty"] = float(items[14])
        vehicle_data["speed_uncertainty"] = float(items[15])
        vehicle_data["heading_uncertainty"] = float(items[16])


if __name__ == "__main__":
    position_thread = threading.Thread(target=receive_vehicle_position, daemon=True)
    position_thread.start()
    time.sleep(1)

    print(f"Attempting to connect to port: {VEHICLE_PORT}")
    vehicle_connection = initialize.connect_to_vehicle(VEHICLE_PORT)
    print("Vehicle connection established.")
    retVal = initialize.verify_connection(vehicle_connection)
    print("Vehicle connection verified.")

    if not retVal:
        print("Error. Could not connect and/or verify a valid connection to the vehicle.")
        sys.exit(1)

    app.run(debug=False, host='0.0.0.0', port=5000)