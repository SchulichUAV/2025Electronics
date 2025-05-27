from time import sleep
from adafruit_servokit import ServoKit


def payload_release(kit, servo_num, vehicle_data):
    try:
        kit.servo[servo_num].angle = 30
        print(f"Successfully opened servo: {servo_num}")
        print(f"drop lat: {vehicle_data['lat']}, lon: {vehicle_data['lon']}, alt: {vehicle_data['alt']}")
        sleep(3)
        kit.servo[servo_num].angle = 180
        print(f"Successfully closed servo: {servo_num}")
    except Exception as e:
        print(f"Could not open or close servo. Error: {e}")

def set_servo_state(servo, open):
    if open:
        print(f"Opening servo{servo}. Not automatically closing.")
        servo.angle = 180
    else:
        print(f"Closing servo{servo}.")
        servo.angle = 30