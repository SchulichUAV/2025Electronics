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
import modules.payload as payload

GCS_URL = "http://192.168.1.64:80"
VEHICLE_PORT = "udp:127.0.0.1:5006"
DELAY = 0.25

picam2 = None
vehicle_connection = None
is_camera_on = False
image_number = 0

servo1 = None
servo2 = None
servo3 = None
servo4 = None

app = Flask(__name__)
CORS(app, supports_credentials=True)

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
    try:
        json_data = request.json
        mode_id = int(json_data['mode_id'])
        # TODO: Need to determine if we are plane or copter mode when starting the server
        # TODO: Retrieve mode_id mapping and print the mode name (mode mappings stored in AutopilotDevelopment/General/Operations/mode.py)
        print(mode_id)
        print(autopilot_mode.set_mode(vehicle_connection, mode_id)) # TODO: Need to use set_mode from plane.py or copter.py depending on current vehicle
    except Exception as e:
        return jsonify({'error': "Invalid operation."}), 400

    return jsonify({'message': 'Mode set successfully'}), 200

@app.route('/payload_manual_control', methods=["POST"])
def payload_manual_control():
    try:
        json_data = request.json
        payload_id = int(json_data['payload_id'])
        payload_open = bool(json_data['payload_open'])
    except Exception as e:
        print("Could not interpret value from API request.")
    try:
        if payload_id == 1:
            payload.set_servo_state(servo1, payload_open)
        elif payload_id == 2:
            payload.set_servo_state(servo2, payload_open)
        elif payload_id == 3:
            payload.set_servo_state(servo3, payload_open)
        elif payload_id == 4:
            payload.set_servo_state(servo4, payload_open)
    except Exception as e:
        print("Could not set servo state.")
        return jsonify({'error': "Invalid operation."}), 400
    
    return jsonify({'servo_status': payload_open, 'message': 'Payload trigger successful'}), 200

@app.route('/payload_release', methods=["POST"])
def payload_release():
    try:
        json_data = request.json
        payload_id = json_data['bay']
    except Exception as e:
        print("Could not interpret value from API request.")

    if (servo1 == None or servo2 == None or servo3 == None or servo4 == None):
        print("ERROR A SERVO IS NONE")

    try:
        if payload_id == 1:
            payload.payload_release(servo1)
        elif payload_id == 2:
            payload.payload_release(servo2)
        elif payload_id == 3:
            payload.payload_release(servo3)
        elif payload_id == 4:
            payload.payload_release(servo4)
    except Exception as e:
        print("Could not release payload.")
        return jsonify({'error': "Invalid operation."}), 400
    
    return jsonify({'message': 'Payload release successful'}), 200


camera_thread = None
stop_camera_thread = threading.Event()

@app.route("/toggle_camera", methods=["POST"])
def toggle_camera():
    # global picam2
    global image_number
    global is_camera_on
    global camera_thread
    global stop_camera_thread

    try:
        json_data = request.json
        is_camera_on = json_data["is_camera_on"]
        image_number = json_data["image_count"]
        print("SUCCESS")
   
    except Exception as e:
        print("Could not interpret `is_camera_on` value from API request.")
        print(e)

    if is_camera_on:
        if camera_thread is None or not camera_thread.is_alive():
            stop_camera_thread.clear()
            camera_thread = threading.Thread(target=continuously_capture_images)
            camera_thread.start()
            print("Starting camera")
    else:
        print("Stopping Camera")
        stop_camera_thread.set()

    return { "message": "Success!"}, 200

def continuously_capture_images():
    global is_camera_on
    global picam2
    global image_number

    if picam2 is None:
        print("Initializing camera...")
        picam2 = Picamera2()
        camera_config = picam2.create_still_configuration()
        picam2.configure(camera_config)
        picam2.start_preview(Preview.NULL)
        time.sleep(1)
    else:
        print("picam2 is not none! starting picam.")
    
    picam2.start()

    try:
        while is_camera_on and not stop_camera_thread.is_set():
            image_number += 1
            delay_time_remaining = DELAY - take_picture(image_number, picam2)
            if delay_time_remaining > 0:
                time.sleep(delay_time_remaining)
    except Exception as e:
        print("Error in camera thread:", e)
    finally:
        print("Stopping camera thread...")
        picam2.stop()

def take_picture(image_number, picam2):
    print(f"Beginning capturing capture{image_number}.jpg")
    start_time = time.time()

    image_stream = BytesIO()
    image = picam2.capture_image('main')
    image.save(image_stream, format='JPEG')
    image_stream.seek(0)

    vehicle_data_json = json.dumps(vehicle_data)
    headers = {} 

    file_name = f'{image_number:05d}'

    image_file = {
        'file': (f'{file_name}.jpg', image_stream, 'image/jpg'),
    }
    response = requests.request("POST", f"{GCS_URL}/submit", headers=headers, files=image_file)

    json_stream = BytesIO(vehicle_data_json.encode('utf-8'))
    json_file = {
        'file': (f'{file_name}.json', json_stream, 'application/json'),
    }
    response = requests.request("POST", f"{GCS_URL}/submit", headers=headers, files=json_file)

    return time.time() - start_time

@app.route("/heartbeat-validate")
def heartbeat_validate():
    # vehicle_data is being continuously updated by a separate thread
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
    servo1, servo2, servo3, servo4 = payload.configure_servos()
    print("Servos configured.")

    # TODO: Need to take a parameter off of the command line to determine if we are a plane or copter

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