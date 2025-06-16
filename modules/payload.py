from time import sleep
import os
import json
from adafruit_servokit import ServoKit

servo_map = {
    0: 0,
    1: 4,
    2: 8,
    3: 12,
}

def payload_release(kit, servo_num, vehicle_data):
    try:
        kit.servo[servo_map[servo_num]].angle = 180
        print(f"Successfully opened servo: {servo_num}. Lat: {vehicle_data['lat']}, Lon: {vehicle_data['lon']}, Alt: {vehicle_data['alt']}")
        drop_data = {
            "lat": vehicle_data["lat"],
            "lon": vehicle_data["lon"],
            "alt": vehicle_data["alt"],
            "last_time": vehicle_data["last_time"]
        }

        json_path = os.path.join(os.path.dirname(__file__), "drop.json")

        if os.path.exists(json_path):
            with open(json_path, "r") as f:
                data = json.load(f)
        else:
            data = []

        data.append(drop_data)

        with open(json_path, "w") as f:
            json.dump(data, f, indent=4)
        
        sleep(4)
        kit.servo[servo_map[servo_num]].angle = 30
        print(f"Successfully closed servo: {servo_num}")
    except Exception as e:
        print(f"Could not open or close servo. Error: {e}")

def release_all(kit, vehicle_data):
    print(f"Releasing all servos at {vehicle_data['lat']}, {vehicle_data['lon']}, {vehicle_data['alt']}")
    open_all_servos(kit)
    sleep(4)
    print("Closing all servos...")
    close_all_servos(kit)

def close_servo(kit, servo_num):
    try:
        kit.servo[servo_map[servo_num]].angle = 30
        print("Successfully closed servo.")
    except Exception as e:
        print(f"Could not close servo. Error: {e}")

def open_servo(kit, servo_num):
    try:
        kit.servo[servo_map[servo_num]].angle = 180
        print("Successfully opened servo.")
    except Exception as e:
        print(f"Could not open servo. Error: {e}")

def close_all_servos(kit):
    for mapped_servo in servo_map.values():
        kit.servo[mapped_servo].angle = 30
    print("All servos closed successfully.")

def open_all_servos(kit):
    for mapped_servo in servo_map.values():
        kit.servo[mapped_servo].angle = 180
    print("All servos opened successfully.")

def set_servo_state(servo, open):
    if open:
        print(f"Opening servo{servo}. Not automatically closing.")
        servo.angle = 180
    else:
        print(f"Closing servo{servo}.")
        servo.angle = 30