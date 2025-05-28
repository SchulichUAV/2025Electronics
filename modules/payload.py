from time import sleep
import os
import json
from adafruit_servokit import ServoKit


def payload_release(kit, servo_num, vehicle_data):
    try:
        kit.servo[servo_num].angle = 180
        print(f"Successfully opened servo: {servo_num}. Lat: {vehicle_data['lat']}, Lon: {vehicle_data['lon']}, Alt: {vehicle_data['alt']}")
        drop_data = {
            "lat": vehicle_data["lat"],
            "lon": vehicle_data["lon"],
            "alt": vehicle_data["alt"],
            "last_time": vehicle_data["last_time"]
        }

        # Path to the JSON file in the same directory
        json_path = os.path.join(os.path.dirname(__file__), "drop.json")

        # Load existing data or create new list
        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                data = json.load(f)
        else:
            data = []

        # Append new drop
        data.append(drop_data)

        # Save back to file
        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)
        
        sleep(4)
        kit.servo[servo_num].angle = 30
        print(f"Successfully closed servo: {servo_num}")
    except Exception as e:
        print(f"Could not open or close servo. Error: {e}")

def release_all(kit, vehicle_data):
    """
    Releases all servos in the kit.
    :param kit: The ServoKit instance controlling the servos.
    :param vehicle_data: Dictionary containing vehicle data (e.g., lat, lon, alt).
    """
    print("Releasing all servos...")
    open_all_servos(kit)
    sleep(4)
    print("Closing all servos...")
    close_all_servos(kit)

def close_servo(kit, servo_num):
    try:
        kit.servo[servo_num].angle = 30
        print("Successfully closed servo.")
    except Exception as e:
        print(f"Could not close servo. Error: {e}")

def open_servo(kit, servo_num):
    try:
        kit.servo[servo_num].angle = 180
        print("Successfully opened servo.")
    except Exception as e:
        print(f"Could not open servo. Error: {e}")

def close_all_servos(kit):
    """
    Closes all servos in the kit.
    :param kit: The ServoKit instance controlling the servos.
    """
    for i in range(len(kit.servo)):
        kit.servo[i].angle = 30
    print("All servos closed successfully.")

def open_all_servos(kit):
    """
    Opens all servos in the kit.
    :param kit: The ServoKit instance controlling the servos.
    """
    for i in range(len(kit.servo)):
        kit.servo[i].angle = 180
    print("All servos opened successfully.")

def set_servo_state(servo, open):
    if open:
        print(f"Opening servo{servo}. Not automatically closing.")
        servo.angle = 180
    else:
        print(f"Closing servo{servo}.")
        servo.angle = 30